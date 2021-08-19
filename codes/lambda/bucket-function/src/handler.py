import os
import json

import boto3
from botocore.exceptions import ClientError

_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def get_list(s3, bucket_name, bucket_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=bucket_key)
        print("CONTENT TYPE: " + response['ContentType'])

        body = response['Body']
        list = json.load(body)['books']

        return list
    except ClientError as e:
        print('error: get_list', e)
        return None


def put_ddb(table, item):
    try:
        response = table.put_item(Item=item)
    except ClientError as e:
        print('Error: put_ddb', e)


def handle(event, context):
    # print('event====>', json.dumps(event))

    s3 = get_client('s3')
    dynamodb = get_resource('dynamodb')
    table = dynamodb.Table(_table_name)

    for record in event['Records']:
        # print('record====>', record)
        bucket_name = record['s3']['bucket']['name']
        bucket_key = record['s3']['object']['key']

        list = get_list(s3, bucket_name, bucket_key)
        if list is not None:
            for item in list:
                print('put item===>', item)
                put_ddb(table, item)
