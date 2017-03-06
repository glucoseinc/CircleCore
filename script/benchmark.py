from datetime import datetime, timedelta
from pprint import pprint

import boto3
import click


def fetch_spot_price(client, instance_type):
    history = client.describe_spot_price_history(
        StartTime=datetime.now(),
        AvailabilityZone='ap-northeast-1b',
        InstanceTypes=[instance_type]
    )['SpotPriceHistory']
    return sorted(history, key=lambda item: item['Timestamp'])[-1]['SpotPrice']


@click.command()
@click.option('--qty', type=click.INT, default=1)
@click.option(
    '--until',  # UTC
    default=(datetime.now().replace(hour=21, minute=0, second=0, microsecond=0) - timedelta(hours=9)).isoformat() + 'Z'
)
@click.option('--instance-type', default='m3.medium')
@click.option('--margin', default=0.01)
def main(qty, until, instance_type, margin):
    client = boto3.client('ec2')
    spot_price = str(float(fetch_spot_price(client, instance_type)) + margin)
    req = {
        'TargetCapacity': qty,
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
            'InstanceType': instance_type,
            'ImageId': 'ami-0c11b26d',
            'KeyName': 'kyudai-benchmark',
            'SpotPrice': spot_price
        }],
        'TerminateInstancesWithExpiration': True,
        'SpotPrice': spot_price,
        'ValidUntil': until
    }
    pprint(req)
    click.confirm('Are you sure to send this request?', abort=True)
    res = client.request_spot_fleet(DryRun=False, SpotFleetRequestConfig=req)
    pprint(res)


if __name__ == '__main__':
    main()
