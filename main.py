import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Specify the Snapshot ID
    snapshot_id = 'snap-1234567890abcdef0'
    availability_zone = 'us-west-2a'
    
    # Create a new EBS volume
    response = ec2.create_volume(
        SnapshotId=snapshot_id,
        AvailabilityZone=availability_zone,
        VolumeType='gp2',  # Adjust as needed
    )
    
    volume_id = response['VolumeId']
    
    # Wait for the volume to become available
    waiter = ec2.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])
    
    # Attach the volume to the EC2 instance
    instance_id = 'i-1234567890abcdef0'
    ec2.attach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device='/dev/sdf'  # Adjust as needed
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('EBS volume successfully attached!')
    }
