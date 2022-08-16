#!/bin/sh

# Configuration File Path
CONFIG_INFRA=config/app-config-demo.json

PROFILE_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Profile') #ex> cdk-demo

echo ==--------ConfigInfo---------==
echo $CONFIG_INFRA
echo $PROFILE_NAME
echo .
echo .

echo ==--------CDKVersionCheck---------==
alias cdk-local="./node_modules/.bin/cdk"
cdk --version
cdk-local --version
echo .
echo .

echo ==--------ListStacks---------==
cdk-local list
echo .
echo .

echo ==--------DeployStacksStepByStep---------==
cdk-local deploy *-ServerlessStack --require-approval never --profile $PROFILE_NAME --outputs-file script/cdk-output.json
echo .
echo .
