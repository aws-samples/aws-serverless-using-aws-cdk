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

echo ==--------DestroyStacksStepByStep---------==
cdk destroy *-ServerlessStack --force --profile $PROFILE_NAME
echo .
echo .
