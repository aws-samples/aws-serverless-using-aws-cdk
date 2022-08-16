#!/bin/sh

# Configuration File Path
CONFIG_INFRA=config/app-config-demo.json

ACCOUNT=$(cat $CONFIG_INFRA | jq -r '.Project.Account') #ex> 123456789123
REGION=$(cat $CONFIG_INFRA | jq -r '.Project.Region') #ex> us-east-2
PROFILE_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Profile') #ex> cdk-demo
PROJECT_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Name') #ex> ServerlessCdk
PROJECT_STAGE=$(cat $CONFIG_INFRA | jq -r '.Project.Stage') #ex> Demo
PROJECT_PREFIX=$PROJECT_NAME$PROJECT_STAGE #ex> ServerlessCdkDemo
PREFIX_LOW=$(echo $PROJECT_PREFIX | tr '[:upper:]' '[:lower:]')

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

echo ==--------DestroyStacksStepByStep---------==
cdk-local destroy *-ServerlessStack --force --profile $PROFILE_NAME
echo .
echo .

echo ==--------DeleteResourcesManually---------==
aws s3 rb s3://${PREFIX_LOW}-serverlessstack-${REGION}-${ACCOUNT:0:5} --force --profile $PROFILE_NAME
aws dynamodb delete-table --table-name ${PROJECT_PREFIX}-ServerlessStack-ddb-table --profile $PROFILE_NAME
echo .
echo .
