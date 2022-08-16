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

aws s3 cp script/input_s3.json s3://"$PREFIX_LOW"-serverlessstack-"$REGION"-"${ACCOUNT:0:5}"/batch/input_s3.json --profile $PROFILE_NAME