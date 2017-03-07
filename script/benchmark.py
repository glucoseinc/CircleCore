from collections import namedtuple
from datetime import datetime, timedelta
from os.path import expanduser
from pathlib import Path
from pprint import pprint
import re
import subprocess
from time import sleep

import boto3
import click
import paramiko


class Benchmarker:
    def __init__(self, qty, until, instance_type, margin, github_user, github_pass, master_ip):
        self.qty = qty
        self.until = until
        self.instance_type = instance_type
        self.margin = margin
        self.github_user = github_user
        self.github_pass = github_pass
        self.master_ip = master_ip

        self.client = boto3.client('ec2')

    def calc_bid(self):
        history = self.client.describe_spot_price_history(
            StartTime=datetime.now(),
            AvailabilityZone='ap-northeast-1b',
            InstanceTypes=[self.instance_type]
        )['SpotPriceHistory']
        min_bid = sorted(history, key=lambda item: item['Timestamp'])[-1]['SpotPrice']
        return '{:.4f}'.format(float(min_bid) + self.margin)

    def create_spot_fleet(self):
        spot_price = self.calc_bid()
        req = {
            'TargetCapacity': self.qty,
            'Type': 'request',
            'IamFleetRole': 'arn:aws:iam::157507247180:role/aws-ec2-spot-fleet-role',
            'AllocationStrategy': 'lowestPrice',
            'LaunchSpecifications': [{
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeSize': 8,
                        'DeleteOnTermination': True,
                        'SnapshotId': 'snap-afedf820',
                        'VolumeType': 'gp2'
                    },
                    'DeviceName': '/dev/xvda'
                }],
                'NetworkInterfaces': [{
                    'AssociatePublicIpAddress': True,
                    'DeleteOnTermination': True,
                    'SubnetId': 'subnet-01783d77',
                    'Groups': ['sg-a9c9b7ce'],
                    'DeviceIndex': 0
                }],
                'InstanceType': self.instance_type,
                'ImageId': 'ami-0c11b26d',
                'KeyName': 'kyudai-benchmark',
                'SpotPrice': spot_price
            }],
            'TerminateInstancesWithExpiration': True,
            'SpotPrice': spot_price,
            'ValidUntil': self.until
        }
        pprint(req)
        click.confirm('Are you sure to send this request?', abort=True)
        res = self.client.request_spot_fleet(DryRun=False, SpotFleetRequestConfig=req)
        pprint(res)
        return res['SpotFleetRequestId']

    def create_spot_instances(self):
        fleet_id = self.create_spot_fleet()

        while True:  # Wait until instances wake up
            running_instances = \
                self.client.describe_spot_fleet_instances(SpotFleetRequestId=fleet_id)['ActiveInstances']
            if len(running_instances) == self.qty:
                break
            else:
                sleep(10)

        instance_ids = [instance['InstanceId'] for instance in running_instances]
        instances = self.client.describe_instances(InstanceIds=instance_ids)['Reservations'][0]['Instances']
        self.instance_ips = [instance['NetworkInterfaces'][0]['Association']['PublicIp'] for instance in instances]

    def provision(self):
        with open('/tmp/hosts', 'w') as hosts:
            hosts.write('\n'.join(self.instance_ips) + '''
[all:vars]
ansible_ssh_user = ec2-user
ansible_ssh_private_key_file = ~/.ssh/kyudai-benchmark.pem
            ''')

        subprocess.run([
            'ansible-playbook',
            '--extra-vars',
            'github_user={} github_pass={}'.format(self.github_user, self.github_pass),
            '-i',
            '/tmp/hosts',
            str(Path(__file__).parent.parent.joinpath('ansible', 'playbook.yaml'))
        ]).check_returncode()

    def connect_crcr(self, ip):
        conn = paramiko.SSHClient()
        conn.load_system_host_keys()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(ip, username='ec2-user', key_filename=expanduser('~/.ssh/kyudai-benchmark.pem'))
        return conn

    def exec_command(self, conn, command):
        return conn.exec_command('\n'.join([
            'cd /home/ec2-user/CircleCore',
            'export LD_LIBRARY_PATH=/usr/local/lib64',
            command
        ]))

    def register_shared_links(self):
        master = self.connect_crcr(self.master_ip)
        self.exec_command(master, 'rm cc_dev/metadata.sqlite')

        for i, slave_ip in enumerate(self.instance_ips, start=1):
            slave = self.connect_crcr(slave_ip)
            self.exec_command(slave, 'rm cc_dev/metadata.sqlite')

            _, stdout, _ = self.exec_command(slave, 'crcr env')
            stdout = stdout.read().decode('utf-8')
            slave_uuid = re.search(r'^Circle Core: .*\(([0-9A-Fa-f-]+)\)$', stdout, re.MULTILINE).group(1)

            _, stdout, _ = self.exec_command(
                master,
                'crcr replication_link add --name benchmark{} --cc {} --all-boxes'.format(i, slave_uuid)
            )
            stdout = stdout.read().decode('utf-8')
            link_uuid = re.search(r'^Replication Link "([0-9A-Fa-f-]+)" is added\.$', stdout, re.MULTILINE).group(1)

            self.exec_command(
                slave,
                'crcr replication_master add --endpoint ws://{}:8080/replication/{}'.format(self.master_ip, link_uuid)
            )

    def run_crcr(self):
        master = self.connect_crcr(self.master_ip)

        _, stdout, _ = self.exec_command(master, 'crcr schema add --name counterbot count:int body:string')
        stdout = stdout.read().decode('utf-8')
        schema_uuid = re.search(r'^Schema "([0-9A-Fa-f-]+)" is added\.$', stdout, re.MULTILINE).group(1)

        _, stdout, _ = self.exec_command(master, 'crcr module add --name counterbot')
        stdout = stdout.read().decode('utf-8')
        module_uuid = re.search(r'^Module "([0-9A-Fa-f-]+)" is added\.$', stdout, re.MULTILINE).group(1)

        _, stdout, _ = self.exec_command(master,
            'crcr box add --name counterbot --schema {} --module {}'.format(schema_uuid, module_uuid)
        )
        stdout = stdout.read().decode('utf-8')
        box_uuid = re.search(r'^MessageBox "([0-9A-Fa-f-]+)" is added\.$', stdout, re.MULTILINE).group(1)

        _, bot_stdout, bot_stderr = self.exec_command(master,
            'python3 sample/sensor_counter.py --to ipc:///tmp/crcr_request.ipc --box-id {}'.format(box_uuid)
        )
        _, master_stdout, master_stderr = self.exec_command(master, 'crcr run')

        for slave_ip in self.instance_ips:
            slave = self.connect_crcr(slave_ip)
            _, slave_stdout, slave_stderr = self.exec_command(slave, 'crcr run')

        for line in slave_stdout.readlines():
            print(line)

    def execute(self):
        self.create_spot_instances()
        self.provision()
        self.register_shared_links()
        self.run_crcr()


@click.command()
@click.option('--qty', type=click.INT, default=1)
@click.option(
    '--until',  # UTC
    default=(datetime.now().replace(hour=21, minute=0, second=0, microsecond=0) - timedelta(hours=9)).isoformat() + 'Z'
)
@click.option('--instance-type', default='m3.medium')
@click.option('--margin', default=0.01)
@click.option('--github-user', required=True)
@click.option('--github-pass', required=True)
@click.option('--master-ip', default='54.249.123.46')
def main(**kwargs):
    Benchmarker(**kwargs).execute()


if __name__ == '__main__':
    main()
