import * as cdk from '@aws-cdk/core';
import * as sns from '@aws-cdk/aws-sns';
import * as lambda from '@aws-cdk/aws-lambda';
import * as ddb from '@aws-cdk/aws-dynamodb';
import * as lambdaEvent from '@aws-cdk/aws-lambda-event-sources';
import * as api from '@aws-cdk/aws-apigateway';
import * as s3 from '@aws-cdk/aws-s3';

export class ServerlessStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const table = this.createDdbTable();
        
        const topic = this.createSnsTopic();
        const topicFunction = this.createLambdaFunctionTopic(table, topic);

        const restFunction = this.createLambdaFunctionRest(table);
        const rest = this.createApiRest(restFunction);

        const bucket = this.createS3Bucket();
        const bucketFunction = this.createLambdaFunctionBucket(table, bucket);
    }

    private createDdbTable(): ddb.Table {
        return new ddb.Table(this, 'ddb-table', {
            tableName: `${this.stackName}-ddb-table`,
            partitionKey: {
                name: 'isbn',
                type: ddb.AttributeType.STRING
            },
            removalPolicy: cdk.RemovalPolicy.DESTROY // not recommended for prod-stage
        });
    }

    private createSnsTopic(): sns.Topic {
        return new sns.Topic(this, 'api-async-topic', {
            displayName: `${this.stackName}-api-async-topic`,
            topicName: `${this.stackName}-api-async-topic`,
        });
    }

    private createLambdaFunctionTopic(table: ddb.Table, topic: sns.Topic): lambda.Function {
        const path = 'codes/lambda/topic-function/src';

        const func = new lambda.Function(this, 'topic-function', {
            functionName: `${this.stackName}-topic-function`,
            runtime: lambda.Runtime.PYTHON_3_6,
            handler: 'handler.handle',
            code: lambda.Code.fromAsset(path),
            environment: {
                "TABLE_NAME": table.tableName
            }
        });

        func.addEventSource(new lambdaEvent.SnsEventSource(topic, {

        }));

        table.grantWriteData(func);

        return func;
    }

    private createApiRest(apiFunction: lambda.Function) {
        const rest = new api.LambdaRestApi(this, 'rest-api', {
            restApiName: `${this.stackName}-APIs`,
            handler: apiFunction,
            proxy: false,
            deployOptions: {
                loggingLevel: api.MethodLoggingLevel.INFO
            }
        });

        const resourceName = 'books';
        const books = rest.root.addResource(resourceName);
        books.addMethod('GET');

        new cdk.CfnOutput(this, 'api-endpoint', {
            value: `https://${rest.restApiId}.execute-api.${this.region}.amazonaws.com/prod/${resourceName}`,
            exportName: 'APIGatewayEndpoint'
        })

        return rest;
    }

    private createLambdaFunctionRest(table: ddb.Table): lambda.Function {
        const path = 'codes/lambda/rest-function/src';

        const func = new lambda.Function(this, 'rest-function', {
            functionName: `${this.stackName}-rest-function`,
            runtime: lambda.Runtime.PYTHON_3_6,
            handler: 'handler.handle',
            code: lambda.Code.fromAsset(path),
            environment: {
                "TABLE_NAME": table.tableName
            }
        });

        table.grantReadData(func);

        return func;
    }

    private createS3Bucket(): s3.Bucket {
        const bucketName = `${this.stackName}-${this.region}-${this.account.substring(0, 5)}`.toLowerCase();
        
        return new s3.Bucket(this, 'bucket', {
            bucketName,
            removalPolicy: cdk.RemovalPolicy.DESTROY // not recommended for prod-stage
        });
    }

    private createLambdaFunctionBucket(table: ddb.Table, bucket: s3.Bucket): lambda.Function {
        const path = 'codes/lambda/bucket-function/src';

        const func = new lambda.Function(this, 'bucket-function', {
            functionName: `${this.stackName}-bucket-function`,
            runtime: lambda.Runtime.PYTHON_3_6,
            handler: 'handler.handle',
            code: lambda.Code.fromAsset(path),
            environment: {
                "TABLE_NAME": table.tableName
            },
            timeout: cdk.Duration.minutes(15)
        });

        func.addEventSource(new lambdaEvent.S3EventSource(bucket, {
            events: [s3.EventType.OBJECT_CREATED_PUT],
            filters: [{prefix: 'batch'}]
        }));

        table.grantWriteData(func);
        bucket.grantRead(func);

        return func;
    }
}
