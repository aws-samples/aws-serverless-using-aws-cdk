import os
import json
import boto3

_profile = None
_table_name = os.environ.get('TABLE_NAME', 'ServerlessCdkDemo-ServerlessStack-ddb-table')


def set_profile(profile):
    global _profile
    _profile = profile


def get_resource(service, profile):
    if profile is None:
        return boto3.Session().resource(service)
    else:
        return boto3.Session(profile_name=profile).resource(service)


def get_list():
    dynamodb = get_resource('dynamodb', _profile)
    table = dynamodb.Table(_table_name)
    
    response = table.scan(
    )

    return response['Items']


def handle(event, context):
    print('====>', json.dumps(event))

    if event['httpMethod'] == 'GET':
        books = get_list()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(books)
        }
