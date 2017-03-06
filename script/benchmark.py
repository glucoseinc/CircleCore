from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint
import subprocess

import boto3
import click


class Benchmarker:
    def __init__(self, qty, until, instance_type, margin, github_user, github_pass):
        self.qty = qty
        self.until = until
        self.instance_type = instance_type
        self.margin = margin
        self.github_user = github_user
        self.github_pass = github_pass
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
        instances = self.client.describe_spot_fleet_instances(SpotFleetRequestId=fleet_id)['ActiveInstances']
        instance_ids = [instance['InstanceId'] for instance in instances]
        self.instances = self.client.describe_instances(InstanceIds=instance_ids)['Reservations'][0]['Instances']

    def provision(self):
        instance_ips = [instance['NetworkInterfaces'][0]['Association']['PublicIp'] for instance in self.instances]

        with open('/tmp/hosts', 'w') as hosts:
            hosts.write('\n'.join(instance_ips) + '''
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
            str(Path.cwd().parent.joinpath('ansible', 'playbook.yaml'))
        ]).check_returncode()

    def execute(self):
        self.create_spot_instances()
        self.provision()
        # self.register_shared_links()
        # self.run_crcr()


@click.command()
@click.option('--qty', type=click.INT, default=1)
@click.option(
    '--until',  # UTC
    default=(datetime.now().replace(hour=21, minute=0, second=0, microsecond=0) - timedelta(hours=9)).isoformat() + 'Z'
)
@click.option('--instance-type', default='m3.medium')
@click.option('--margin', default=0.01)
@click.option('--github_user', required=True)
@click.option('--github_pass', required=True)
def main(**kwargs):
    Benchmarker(**kwargs).execute()


if __name__ == '__main__':
    main()
