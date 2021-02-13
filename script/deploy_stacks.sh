#!/bin/sh

# Configuration File Path
CONFIG_INFRA=config/app-config.json

PROFILE_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Profile') #ex> cdk-demo

echo ==--------ConfigInfo---------==
echo $CONFIG_INFRA
echo $PROFILE_NAME
echo .
echo .

echo ==--------ListStacks---------==
cdk list
echo .
echo .

echo ==--------DeployStacksStepByStep---------==
cdk deploy *-ServerlessStack --require-approval never --profile $PROFILE_NAME --outputs-file script/cdk-output.json
echo .
echo .
