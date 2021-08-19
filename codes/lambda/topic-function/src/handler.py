import os
import json

import boto3
from botocore.exceptions import ClientError

_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def put_ddb(table, item):
    try:
        response = table.put_item(Item=item)
    except ClientError as e:
        print('Error: put_ddb', e)


def handle(event, context):
    # print('event====>', json.dumps(event))

    dynamodb = get_resource('dynamodb')
    table = dynamodb.Table(_table_name)

    for record in event['Records']:
        msg = json.loads(record['Sns']['Message'])
        print('put item===>', msg)
        put_ddb(table, msg)