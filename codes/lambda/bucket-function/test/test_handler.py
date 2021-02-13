import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+'/src')
import handler

handler.set_profile('cdk-demo')

with open('event.json') as f:
    event = json.load(f)
    handler.handle(event, None)
