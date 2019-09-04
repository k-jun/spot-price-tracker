
import os
import base64
import boto3
import time
import json
from datetime import date
from datetime import datetime

REGION = os.environ['REGION']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
BUCKET_NAME = 'spot-instance-price-tracker'

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')


def error_handling(e):
    data = {
        'error': str(e)
    }
    response = {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }
    return response

def success_handing(body):
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }
    return response

def create_bucket(event, context):
    try:
        response = s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'},
        )
        return success_handing({'message': 'success'})
    except Exception as e:
        return error_handling(e)

def price_register(event, context):
    try:
        start = time.time()
        region_az_list = []
        regions = ec2_client.describe_regions()
        for reg in regions['Regions']:
            reg_name = reg['RegionName']
            start = time.time()
            local_ec2_client = boto3.client('ec2', region_name=reg_name)
            response = local_ec2_client.describe_availability_zones()
            az = []
            for zone in response['AvailabilityZones']:
                az.append(zone['ZoneName'])
            region_az_list.append({'Region': reg_name, 'AZ': az})
        region_az_list = [{'Region': 'eu-north-1', 'AZ': ['eu-north-1a', 'eu-north-1b', 'eu-north-1c']}, {'Region': 'ap-south-1', 'AZ': ['ap-south-1a', 'ap-south-1b', 'ap-south-1c']}, {'Region': 'eu-west-3', 'AZ': ['eu-west-3a', 'eu-west-3b', 'eu-west-3c']}, {'Region': 'eu-west-2', 'AZ': ['eu-west-2a', 'eu-west-2b', 'eu-west-2c']}, {'Region': 'eu-west-1', 'AZ': ['eu-west-1a', 'eu-west-1b', 'eu-west-1c']}, {'Region': 'ap-northeast-2', 'AZ': ['ap-northeast-2a', 'ap-northeast-2b', 'ap-northeast-2c']}, {'Region': 'ap-northeast-1', 'AZ': ['ap-northeast-1a', 'ap-northeast-1c', 'ap-northeast-1d']}, {'Region': 'sa-east-1', 'AZ': ['sa-east-1a', 'sa-east-1c']}, {'Region': 'ca-central-1', 'AZ': ['ca-central-1a', 'ca-central-1b']}, {'Region': 'ap-southeast-1', 'AZ': ['ap-southeast-1a', 'ap-southeast-1b', 'ap-southeast-1c']}, {'Region': 'ap-southeast-2', 'AZ': ['ap-southeast-2a', 'ap-southeast-2b', 'ap-southeast-2c']}, {'Region': 'eu-central-1', 'AZ': ['eu-central-1a', 'eu-central-1b', 'eu-central-1c']}, {'Region': 'us-east-1', 'AZ': ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f']}, {'Region': 'us-east-2', 'AZ': ['us-east-2a', 'us-east-2b', 'us-east-2c']}, {'Region': 'us-west-1', 'AZ': ['us-west-1a', 'us-west-1c']}, {'Region': 'us-west-2', 'AZ': ['us-west-2a', 'us-west-2b', 'us-west-2c', 'us-west-2d']}]
        data = []

        for region_az in region_az_list:
            region = region_az['Region']
            az = region_az['AZ']
            print("AZ: ", az)
            for AZ in az:
                local_ec2_client = boto3.client(
                    'ec2', region_name=region)
                prices = local_ec2_client.describe_spot_price_history(
                    AvailabilityZone=AZ,
                    InstanceTypes=['t1.micro', 't2.nano', 't2.micro', 't2.small', 't2.medium','t2.large','t2.xlarge','t2.2xlarge','t3.nano','t3.micro','t3.small','t3.medium','t3.large','t3.xlarge','t3.2xlarge','t3a.nano','t3a.micro','t3a.small','t3a.medium','t3a.large','t3a.xlarge','t3a.2xlarge','m1.small','m1.medium','m1.large','m1.xlarge','m3.medium','m3.large','m3.xlarge','m3.2xlarge','m4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge','m4.16xlarge','m2.xlarge','m2.2xlarge','m2.4xlarge','cr1.8xlarge','r3.large','r3.xlarge','r3.2xlarge','r3.4xlarge','r3.8xlarge','r4.large','r4.xlarge','r4.2xlarge','r4.4xlarge','r4.8xlarge','r4.16xlarge','r5.large','r5.xlarge','r5.2xlarge','r5.4xlarge','r5.8xlarge','r5.12xlarge','r5.16xlarge','r5.24xlarge','r5.metal','r5a.large','r5a.xlarge','r5a.2xlarge','r5a.4xlarge','r5a.8xlarge','r5a.12xlarge','r5a.16xlarge','r5a.24xlarge','r5d.large','r5d.xlarge','r5d.2xlarge','r5d.4xlarge','r5d.8xlarge','r5d.12xlarge','r5d.16xlarge','r5d.24xlarge','r5d.metal','r5ad.large','r5ad.xlarge','r5ad.2xlarge','r5ad.4xlarge','r5ad.8xlarge','r5ad.12xlarge','r5ad.16xlarge','r5ad.24xlarge','x1.16xlarge','x1.32xlarge','x1e.xlarge','x1e.2xlarge','x1e.4xlarge','x1e.8xlarge','x1e.16xlarge','x1e.32xlarge','i2.xlarge','i2.2xlarge','i2.4xlarge','i2.8xlarge','i3.large','i3.xlarge','i3.2xlarge','i3.4xlarge','i3.8xlarge','i3.16xlarge','i3.metal','i3en.large','i3en.xlarge','i3en.2xlarge','i3en.3xlarge','i3en.6xlarge','i3en.12xlarge','i3en.24xlarge','i3en.metal','hi1.4xlarge','hs1.8xlarge','c1.medium','c1.xlarge','c3.large','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge','c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge','c5.large','c5.xlarge','c5.2xlarge','c5.4xlarge','c5.9xlarge','c5.12xlarge','c5.18xlarge','c5.24xlarge','c5.metal','c5d.large','c5d.xlarge','c5d.2xlarge','c5d.4xlarge','c5d.9xlarge','c5d.18xlarge','c5n.large','c5n.xlarge','c5n.2xlarge','c5n.4xlarge','c5n.9xlarge','c5n.18xlarge','cc1.4xlarge','cc2.8xlarge','g2.2xlarge','g2.8xlarge','g3.4xlarge','g3.8xlarge','g3.16xlarge','g3s.xlarge','cg1.4xlarge','p2.xlarge','p2.8xlarge','p2.16xlarge','p3.2xlarge','p3.8xlarge','p3.16xlarge','p3dn.24xlarge','d2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge','f1.2xlarge','f1.4xlarge','f1.16xlarge','m5.large','m5.xlarge','m5.2xlarge','m5.4xlarge','m5.8xlarge','m5.12xlarge','m5.16xlarge','m5.24xlarge','m5.metal','m5a.large','m5a.xlarge','m5a.2xlarge','m5a.4xlarge','m5a.8xlarge','m5a.12xlarge','m5a.16xlarge','m5a.24xlarge','m5d.large','m5d.xlarge','m5d.2xlarge','m5d.4xlarge','m5d.8xlarge','m5d.12xlarge','m5d.16xlarge','m5d.24xlarge','m5d.metal','m5ad.large','m5ad.xlarge','m5ad.2xlarge','m5ad.4xlarge','m5ad.8xlarge','m5ad.12xlarge','m5ad.16xlarge','m5ad.24xlarge','h1.2xlarge','h1.4xlarge','h1.8xlarge','h1.16xlarge','z1d.large','z1d.xlarge','z1d.2xlarge','z1d.3xlarge','z1d.6xlarge','z1d.12xlarge','z1d.metal','u-6tb1.metal','u-9tb1.metal','u-12tb1.metal','a1.medium','a1.large','a1.xlarge','a1.2xlarge','a1.4xlarge'],
                    StartTime=datetime(2019, 9, 2),
                    EndTime=datetime(2019, 9, 3),
                    ProductDescriptions=['Linux/UNIX (Amazon VPC)'],
                )
                for i in prices['SpotPriceHistory']:
                    time_stump = i['Timestamp'].strftime("%Y-%m-%d %H:%M")
                    instance_type = i['InstanceType']
                    price = i['SpotPrice']
                    data.append({
                        'instance_type': instance_type,
                        'time_stump': time_stump,
                        'region': region,
                        'zone': AZ,
                        'price': price,
                    })
        
        # jsonでs3にupload
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Body=json.dumps(data),
            Key="2019-09-02.json"
        )
        return success_handing({'message': 'success'})
    except Exception as e:
        return error_handling(e)
