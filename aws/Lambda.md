# AWS Lambda

## Serverless

Serverless computing. It is not that there aren't servers, simply that you don't manage them.

Serverless Services

- AWS Lambda
- DynamoDB
- AWS Cognito
- AWS API Gateway
- S3
- SNS and SQS
- Kinesis Data Firehose
- Aurora Serverless
- Step Functions
- Fargate

# Why Lambda ?

EC2 Instances:
- Virtual Services
- Limited by Hardware Constraints
- Continuously Running
- Scaling is not trivial

Lambda
- Virtual functions
- Execution times are short (< 15 minutes)
- Automated scaling
- On-demand
- Integated with AWS suite of services
- Many different programming languages 
- CloudWatch monitoring
- Increase your RAM usage (<= 10 GB of RAM)
- Increasing RAM increases CPU and network

Lambda Pricing
- Cost is number of requests and compute time
- Free tier is 1M requests and 400K GB of compute time
