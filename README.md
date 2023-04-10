# AWS Serverless using AWS CDK

This repository describes how to implement basic patterns of [AWS Serverless](https://aws.amazon.com/serverless) using [AWS CDK](https://aws.amazon.com/cdk). AWS CDK is a great tool for serverless applications because it helps you manage multiple serverless resources in one place.

Korean practice guide and demo is provided through the following video: [AWS DevAxConnect - AWS Serverless service development with AWS CDK](https://www.twitch.tv/videos/1070023684?collection=4wZXJvncHRaoEg).

This project was implemented based on [AWS CDK Project Template for DevOps](https://github.com/aws-samples/aws-cdk-project-template-for-devops) for more fluent DevOps application.

Other "Using AWS CDK" series can be found in:

- [AWS ECS DevOps Using AWS CDK](https://github.com/aws-samples/aws-ecs-devops-using-aws-cdk)
- [Amazon SageMaker Model Serving using AWS CDK](https://github.com/aws-samples/amazon-sagemaker-model-serving-using-aws-cdk)
- [AWS IoT Greengrass Ver2 using AWS CDK](https://github.com/aws-samples/aws-iot-greengrass-v2-using-aws-cdk)

## Contents

1. [**Repository structure**](#repository-structure)

2. [**Solution coverage**](#solution-coverage)
  
3. [**Solution architecture**](#solution-architecture)

4. [**Quick Guide**](#quick-guide)

5. [**About CDK-Project**](#about-cdk-project)

6. [**How to deploy**](#how-to-deploy)

    - [**Prerequisites**](#prerequisites)
    - [**How to set up**](#how-to-set-up)
    - [**How to provision**](#how-to-provision)

7. [**How to test**](#how-to-test)

8. [**How to clean up**](#how-to-clean-up)

9. [**Security**](#security)

10.  [**License**](#license)

## **Repository structure**

Because this repository is basically a CDK-Project which is based on typescript, the project structure follows the basic CDK-Project form. This porject provide one stack and 3 lambdas. Before depoy this project, `config/app-config-demo.json` should be filled in according to your AWS Account.

![ProjectStructure](docs/asset/project.png)

## **Solution coverage**

This repository introduces the common patterns of AWS Serverless.

- pattern 1: Amazon SNS -> Amazon Lambda -> Amazon DynamoDB
- pattern 2: Amazon S3 -> Amazon Lambda -> Amazon DynamoDB
- pattern 3: Amazon API Gateway -> Amazon Lambda -> Amazon DynamoDB

## **Solution architecture**

Specifically, it is implemented assuming that we are developing a ***book catalog service*** for easy understanding.

- flow 1: Async Single Request(Request to save one book)
- flow 2: Async Batch Request(Request to save a large of books)
- flow 3: Sync Single Request(Request for a list of books)

![SolutionArchitecture](docs/asset/architecture.png)

AWS services used are as follows:

- [Amazon Lambda](https://aws.amazon.com/lambda): a serverless computing which run code without thinking about servers
- [Amazon Simple Notification Service(SNS)](https://aws.amazon.com/sns): a fully managed messaging service for both application-to-application (A2A) and application-to-person (A2P) communication
- [Amazon Simple Storage Service(S3)](https://aws.amazon.com/s3): object storage built to store and retrieve any amount of data from anywhere
- [Amazon API Gateway](https://aws.amazon.com/api-gateway): a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb): a fast and flexible NoSQL database service for any scale

## **Quick Guide**

Just execute the following commands step by step for quick practice.

```bash
vim config/app-config-demo.json # change Account/Region
sh script/deploy_stacks.sh      # deploy a stack
sh script/request_api.sh        # invoke APIGateway(empty book list)
sh script/publish_sns.sh        # add a book through SNS
sh script/request_api.sh        # invoke APIGateway(a book in list)
sh script/upload_s3.sh          # add 3 books through S3
sh script/request_api.sh        # invoke APIGateway(4 books in list)
sh script/destroy_stacks.sh     # destroy stacks
```

## **About CDK-Project**

To efficiently define and provision serverless resources, [AWS Cloud Development Kit(CDK)](https://aws.amazon.com/cdk) which is an open source software development framework to define your cloud application resources using familiar programming languages is utilized .

![AWSCDKIntro](docs/asset/aws_cdk_intro.png)

Because this solusion is implemented in CDK, we can deploy these cloud resources using CDK CLI. Among the various languages supported, this solution used typescript. Because the types of `typescript` are very strict, with the help of auto-completion, typescrip offers a very nice combination with AWS CDK.

### **CDK specific file**

The `cdk.json` file tells the CDK Toolkit how to execute your app.

### **CDK Commands**

And the more useful CDK commands are

- `cdk list`        list up CloudFormation Stacks
- `cdk deploy`      deploy this stack to your default AWS account/region
- `cdk diff`        compare deployed stack with current state
- `cdk synth`       emits the synthesized CloudFormation template
- `cdk destroy`     remove resources

## **How to deploy**

***Caution***: This solution contains not-free tier AWS services. So be careful about the possible costs. Fortunately, serverless services minimize cost if not used.

### **Prerequisites**

First of all, AWS Account and IAM User is required. And then the following must be installed.

- AWS CLI: aws configure --profile [profile name]
- Node.js: node --version
- AWS CDK: cdk --version
- [jq](https://stedolan.github.io/jq/): jq --version

Please refer to the kind guide in [CDK Workshop](https://cdkworkshop.com/15-prerequisites.html).

### **How to set up**

First of all, enter your project basic configuration in the follwoing document: `config/app-config-demo.json`. Fill in your project's "Name", "Stage", "Account", "Region", "Profile(AWS CLI Credentials)" in "Project" according to your environments.

```json
{
    "Project": {
        "Name": "ServerlessCdk",
        "Stage": "Demo",
        "Account": "75157*******",
        "Region": "us-east-2",
        "Profile": "cdk-demo"
    }
}
```

If you don't know AWS Account/Region, execute the following commands to catch your AWS-Account.

```bash
aws sts get-caller-identity --profile [your-profile-name]
...
...
{
    "Account": "[account-number]", 
    "UserId": "[account-id]", 
    "Arn": "arn:aws:iam::75157*******:user/[iam-user-id]"
}
```

And then execute the following command to set up CDK-Project. For details, please check `setup_initial.sh` file.

```bash
sh ./script/setup_initial.sh  
```

### **How to provision**

Let's check stack included in this CDK-Project before provisining. Execute the following command. The prefix "***ServerlessCdkDemo***" can be different according to your setting(Project Name/Stage).

```bash
cdk list
...
...
ServerlessCdkDemo-ServerlessStack
```

Now, everything is ready, let's provision a stack using AWS CDK. Execute the following command which will deploy the stack and create a `cdk-output.json` file in `script` directory, which includes deployment result outouts. For details, please check `deploy_stacks.sh` file.

```bash
sh script/deploy_stacks.sh
```

## **How to test**

For ***Async Single Request***, execute the following command, which will publish SNS message(script/input_sns.json) and finally the lambda functions will be executed to save one book into DynamoDB.

```bash
sh script/publish_sns.sh
...
...
{
    "MessageId": "e78906f5-4544-5e19-9191-5e9ea2a859bd"
}
```

After executing this command, please check your DynamoDB. You can find a new item in that.

For ***Async Batch Request***, execute the following command, which will upload a json file(script/input_s3.json) into S3 and finally the lambda functions will be executed to save a large of books into DynamoDB.

```bash
sh script/upload_s3.sh
...
...
upload: script/input_s3.json to s3://serverlesscdkdemo-serverlessstack-us-east-2-75157/batch/input_s3.json
```

After executing this command, please check your DynamoDB. You can find the multiple items in that.

For ***Sync Single Request***, execute the following command, which will send http-get request and finally the lambda functions will be executed to get a list of books in DynamoDB.

```bash
sh script/request_api.sh
...
...
{
  "status": "success",
  "books": [
    {
      "isbn": "isbn-01",
      "src": "sns",
      "title": "book-01"
    },
    {
      "isbn": "isbn-03",
      "src": "s3",
      "title": "book-03"
    },
    {
      "isbn": "isbn-02",
      "src": "s3",
      "title": "book-02"
    },
    {
      "isbn": "isbn-04",
      "src": "s3",
      "title": "book-04"
    }
  ]
}
```

## **How to clean up**

Execute the following command, which will destroy all resources including S3 Buckets and DynamoDB Tables. For details, please check `destroy_stacks.sh` file.

```bash
sh script/destroy_stacks.sh
```

## **Security**

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## **License**

This library is licensed under the MIT-0 License. See the LICENSE file.
