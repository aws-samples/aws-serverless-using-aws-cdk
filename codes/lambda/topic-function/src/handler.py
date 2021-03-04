import os
import json
import boto3

_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.Session().resource(service)


def put_ddb(msg):
    dynamodb = get_resource('dynamodb')
    table = dynamodb.Table(_table_name)
    
    response = table.put_item(
       Item=msg
    )


def handle(event, context):
    # print('====>', json.dumps(event))

    for record in event['Records']:
        msgs = json.loads(record['Sns']['Message'])
        for msg in msgs:
            print('===>', msg)
            put_ddb(msg)