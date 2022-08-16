#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { ServerlessStack } from './stack/serverless-stack';

import appConfig from './../config/app-config-demo.json';

const stackPrefix = `${appConfig.Project.Name}${appConfig.Project.Stage}`
const stackProps: cdk.StackProps = { 
    env: {
        account: appConfig.Project.Account,
        region: appConfig.Project.Region
    }
};

const app = new cdk.App();

new ServerlessStack(app, `${stackPrefix}-ServerlessStack`, stackProps);