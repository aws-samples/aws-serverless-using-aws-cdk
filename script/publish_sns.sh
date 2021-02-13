#!/bin/sh

# Configuration File Path
CONFIG_INFRA=config/app-config.json

ACCOUNT=$(cat $CONFIG_INFRA | jq -r '.Project.Account') #ex> 123456789123
REGION=$(cat $CONFIG_INFRA | jq -r '.Project.Region') #ex> us-east-1
PROFILE_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Profile') #ex> cdk-demo
PROJECT_NAME=$(cat $CONFIG_INFRA | jq -r '.Project.Name') #ex> ServerlessCdk
PROJECT_STAGE=$(cat $CONFIG_INFRA | jq -r '.Project.Stage') #ex> Demo
PROJECT_PREFIX=$PROJECT_NAME$PROJECT_STAGE #ex> ServerlessCdkDemo

aws sns publish --topic-arn arn:aws:sns:"$REGION":"$ACCOUNT":"$PROJECT_PREFIX"-ServerlessStack-api-async-topic --profile $PROFILE_NAME --message file://script/input_sns.json