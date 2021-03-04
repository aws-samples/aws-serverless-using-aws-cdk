import os
import json
import boto3

_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def get_list():
    dynamodb = get_resource('dynamodb')
    table = dynamodb.Table(_table_name)
    
    response = table.scan(
    )

    return response['Items']


def handle(event, context):
    # print('====>', json.dumps(event))

    if event['httpMethod'] == 'GET':
        books = get_list()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(books)
        }
