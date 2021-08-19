import os
import json

import boto3
from botocore.exceptions import ClientError

_table = None
_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def get_table(table_name: str):
    global _table
    if _table is None:
        dynamodb = get_resource('dynamodb')
        _table = dynamodb.Table(table_name)
    return _table


def get_list(table):
    try:
        response = table.scan()
        return response['Items']
    except ClientError as e:
        print('Error: ddb scan', e)
        return None


def create_response_body(books) -> str:
    if books is not None:
        body = {
            'status': 'success',
            'books': books
        }
    else:
        body = {
            'status': 'fail'
        }

    return json.dumps(body)


def handle(event, context):
    # print('event====>', json.dumps(event))

    table = get_table(_table_name)

    if event['httpMethod'] == 'GET':
        books = get_list(table)
        body_str = create_response_body(books)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body_str
        }
