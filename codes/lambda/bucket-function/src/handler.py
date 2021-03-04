import os
import json
import boto3
from botocore.exceptions import ClientError

_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def put_ddb(msg):
    dynamodb = get_resource('dynamodb')
    table = dynamodb.Table(_table_name)
    
    try:
        response = table.put_item(Item=msg)
    except ClientError as e:
        print('Error: table.put_item', e)


def handle(event, context):
    # print('====>', json.dumps(event))

    s3 = get_client('s3')

    for record in event['Records']:
        print('record====>', record)
        bucket_name = record['s3']['bucket']['name']
        bucket_key = record['s3']['object']['key']

        try:
            file_path = '/tmp/input.json'

            s3.download_file(bucket_name, bucket_key, file_path)

            with open(file_path) as f:
                list = json.load(f)
                print('===>list', list)

                for item in list:
                    print('===>', item)
                    put_ddb(item)
        except Exception as e:
            print('error: s3.download_file', e)
