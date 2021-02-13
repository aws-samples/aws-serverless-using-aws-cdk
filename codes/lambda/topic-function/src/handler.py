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


def put_ddb(msg):
    dynamodb = get_resource('dynamodb', _profile)
    table = dynamodb.Table(_table_name)
    
    response = table.put_item(
       Item=msg
    )


def handle(event, context):
    # print('====>', json.dumps(event))
    # pass

    for record in event['Records']:
        msgs = json.loads(record['Sns']['Message'])
        for msg in msgs:
            print('===>', msg)
            put_ddb(msg)