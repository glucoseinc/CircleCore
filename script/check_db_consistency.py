from pathlib import Path
from itertools import chain
import subprocess
import click
import boto3


@click.command()
@click.option('--fleet-id', type=click.STRING)
def main(fleet_id):
    client = boto3.client('ec2')
    running_instances = client.describe_spot_fleet_instances(SpotFleetRequestId=fleet_id)['ActiveInstances']
    instance_ids = [instance['InstanceId'] for instance in running_instances]
    instances = chain.from_iterable(
        reserve['Instances']
        for reserve in client.describe_instances(InstanceIds=instance_ids)['Reservations']
    )

    for instance in instances:
        instance_ip = instance['NetworkInterfaces'][0]['Association']['PublicIp']

        with open(str(Path(__file__).parent.joinpath('{}.sql'.format(instance_ip))), 'w') as f:
            subprocess.run("mysql --host "+instance_ip+" -u root -Be 'SELECT * FROM ' \
                $(mysql --host "+instance_ip+" -u root -Ee 'USE crcr_dev; SHOW TABLES' \
                | awk '/^[^\*]/ { print $2; exit }') \
                ",
                shell=True,
                check=True,
                stdout=f
            )


if __name__ == '__main__':
    main()
