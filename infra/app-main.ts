#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ServerlessStack } from './stack/serverless-stack';

import { loadConfig } from '../lib/utils/config-loaders';

let appConfig: any = loadConfig('config/app-config-demo.json');
const stackProps: cdk.StackProps = { 
    env: {
        account: appConfig.Project.Account,
        region: appConfig.Project.Region
    }
};
const projectPrefix = `${appConfig.Project.Name}${appConfig.Project.Stage}`

const app = new cdk.App();

new ServerlessStack(app, `${projectPrefix}-ServerlessStack`, stackProps);