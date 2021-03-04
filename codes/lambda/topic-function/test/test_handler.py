import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+'/src')
import handler

os.environ['AWS_PROFILE'] = 'cdk-demo'

def test_handle():
    print('test_handle')
    with open('event.json') as f:
        event = json.load(f)
        handler.handle(event, None)

test_handle()