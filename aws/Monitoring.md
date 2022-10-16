# CloudWatch, EventBridge, X-Ray, CloudTrail

Many AWS users don't enable monitoring. Most users only care if your app is working, not slow.

Monitoring helps with:
- Preventing issues before they happen? 
- How our app is performing
- Could you do it with a lower cost
- Patterns that occur when scaling

CloudWatch
- Metrics
- Logs
- Events
- Alarms

X-Ray:
- Troubleshooting app performance and errors
- Tracing of microservices

CloudTrail
- Auditing changes to your resources
- Monitoring of APIs

# CloudWatch Metrics

There are metrics from every service in AWS. A **metric** is a variable to monitor. [List of Metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html):

- CPUUtilization
- DiskReadOps
- DiskWriteOps
- EBSReadOps
- NetworkIn

Metrics belong to namespaces and have up to 10 dimensions (attributes), like instance ID, environment. Metrics also have timestamps. Metrics can be displayed on a CloudWatch dashboard.

- EC2 instances get metrics "every 5 minutes"
- You can pay for every minute using detailed monitoring.
- Those monitors can help you scale faster for things like ASGs 
- Free tier allows 10 detailed monitoring.
- EC2 memory must be pushed via a custom metric

# CloudWatch Custom Metrics

Push your own metrics via API `PutMetricData`, including dimensions. Examples

- Memory
- Disk Space
- Num logged in users

Dimensions logged may be the instance ID or environment.

You also set the StorageResolution or how often the metric is sent:
- Standard: 1 minute
- High: 1/5/10/30 seconds (costs more)

You can send metric data from 2 weeks in the past to 2 hours in the future. Make sure you have the EC2 instance time synched (NTP)

AWS CLI command `put-metric-data` is used to push the data. [CLI documentation](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-data.html).

By JSON:

```shell
aws cloudwatch put-metric-data --namespace "Usage Metrics" --metric-data file://metric.json
```

```json
[
  {
    "MetricName": "New Posts",
    "Timestamp": "Wednesday, June 12, 2013 8:28:20 PM",
    "Value": 0.50,
    "Unit": "Count"
  }
]
```

By Command:

```
aws cloudwatch put-metric-data --metric-name Buffers --namespace MyNameSpace --unit Bytes --value 231434333 --dimensions InstanceID=1-23456789,InstanceType=m1.small
```

# CloudWatch Logs

Central area for logging.

- Log Groups: Top-level grouping of logs, like an application
- Log Stream: Subgroups within the log group for components of the application
- Logs can expire (no default expiration)
- Log Retention policy is defined at the Log Groups level
- Logs can be exported
  - S3
  - Kinesis Data Streams
  - Kinesis Data Firehose
  - Lambda
  - ElasticSearch

## Sources

- SDK
- CloudWatch Logs Agent
- CloudWatch Unified Agent
- ElasticBeanstalk
- ECS - container logs
- Lambda - function logs
- VPC Flow Logs - VPC logs
- API Gateway
- CloudTrail via a filter
- Route53 - DNS queries

## Filtering and Insights

Filter expresions can be used to find things like IP Address or "ERROR".

Filters can be used to trigger CloudWatch alarms

CloudWatch Logs Insights allows you to query logs and add them to dashboards

## S3 Export

It takes log data 12 hours to be exportable using the **CreateExportTask**

Log Subscriptions are used for more real-time exports

## Log Subscriptions

You create a Subscription filter that can sent it to:

- Lambda Function to Amazon ElasticSearch
- Kinesis Data Firehose to Amazon ElasticSearch (real-time) or S3 (near real-time)
- Kinesis Data Streams to Firehose, Kinesis Data Analytics, EC2 or Lambda
- Lambda

## Log Aggregation

Multiple Subscription Filters even external to the accounts can be sent to the same Kinesis Data Streams, aggregate them into Kinesis Data Firehose

# CloudWatch Logs for EC2

Need to start the CloudWatch Logs Agent on each EC2 instance to push logs to CloudWatch. No logs are sent by default.

- Make sure IAM perms to CloudWatch are set for the instance
- Agent can be install on-prem too.

Two different agents:

- Logs Agent - older, only sends to CloudWatch Logs
- Unified Agent - Collects other metrics like RAM, num processes

## Unified Agent 

It is unified because it can send both metrics and logs. Centralized config for SSM Parameter store.

Metrics you can collect
- CPU
- Disk - free, used, total
- Disk I/O - reads, writes, iops
- RAM - free, total
- Netstat
- Processes - total, running, dead
- Swap Space - free, used

Without the unified agent you only get disk, CPU, and network.

# CloudWatch Logs Metric Filter

Filters can be used for metrics, just like logs. Filter expresions can be used to find things like IP Address or "ERROR".

Filters can be used to trigger CloudWatch alarms.

Filters don't use old data to filter, only for events after the filter was created.

# CloudWatch Alarms

Metrics trigger notifications based on various ways (percent, min/max, sampling). There are 3 alarm states:

- OK
- INSUFFICIENT_DATA
- ALARM

Alarms also have periods of how long in seconds a metric should be evaluated.

High resolution custom metric period examples:

- 10 seconds
- 30 seconds
- multiples of 60 seconds

Alarms cam be created via CloudWatch Logs Metrics Filters

You can test alarm via set-alarm-state to the CLI:

```shell
aws cloudwatch set-alarm-state --alarm-name "myalarm" --state-value ALARM --state-reason "testing purposes"
```


## Alarm Targets

- EC2 Instances: Start, Stop, Reboot, Recover the instance
- ASG: scale up or down
- Amazon Simple Notification Service (SNS) for general purpose

## Instance Recovery

Two types of status checks:
- Instance: Check the VM
- System: Check the hardware (eg file system)

A recovery will get the same:
- Private subnet
- Public subnet
- Elastic IP
- metadata
- placement

# CloudWatch Events

Intercept events from AWS services:

- EC2 Instance Start
- EC2 Instance Stop
- EC2 Instance Terminate
- CodeBuild Failure
- etc

Intercept any API call with CloudTrail as well.

You can also schedule events with a Lambda function similar to Cron.

The way it works is a JSON payload is generated from the event and sent to the target. Targets can be pretty much anything:

- Lambda
- Batch
- ECS task
- SQS, SNS, Kinesis
- CodePipeline
- CodeBuild
- SSM
- EC2 Actions

CloudWatch Events may soon disappear as it is to be replaced by Amazon EventBridge

# EventBridge

Next version of CloudWatch Events. Same **default event bus** that are generated by AWS services, but includes a **Partner Event Bus** for other eventing like:

- ZenDesk
- DataDog
- Segment
- Auth0

And also a **custom event bus** for events from your application.

Event Buses:
- Accessed in other AWS accounts
- Allow archiving all or a subset that are sent to an event bus
- You can "replay" archived events to troubleshoot

EventBridge also uses rules to process events just like CloudWatch Events

## Schema Registry

EventBridge looks at events and can figure out the event schema. The Schema Registry allows you to figure out in code how the data is structured so you can create code to process it. The schemas can then be versioned.

## Resource Policy

You manage who can access the event bus. For example, if you want to let an other account be the central event bus for aggregating all of your events.

## Comparing EventBridge to CloudWatch Events

- EventBridge extends CloudWatch Events
- Same service API. Same service infrastructure architecture
- Event Buses are only in EventBridge
- Schema Registries are only in EventBridge

# X-Ray

What if you only have a problem in production?

One scenario is you:

- Test locally
- Add logging statements
- Re-deploy

Logging formats differ across apps and services. And it gets even worse debugging distributed services.

X-Ray solves these problems.

## What is X-Ray?

Provides a visual analysis of your apps.

- Troubleshoot performance
- Bottlenecks
- Understand the app dependencies
- Error and exceptions
- Pinpoint service problem
- Understand how requests behave
- Is SLA being met
- Where is the network the big bottleneck
- Which users can be impacted

Compatible with

- Lambda
- Beanstalk
- ECS
- ELB
- API Gateway
- EC2 instances
- On-prem servers

## X-Ray Concepts

Trace - 1 to many segments that cover end-to-end
Segments - Grouping of traces based on service
Subsegment - Sub grouping of segments for more granular data
Sampling - How often to get a trace. More samples, more cost
Annotations - Key Value pairs for trace indexing and filtering
Metadata - Key Value, but not indexable or searchable

X-Ray Daemon through the use of IAM allow for a centralized account for tracing.

## Tracing

X-Ray uses tracing to follow a request.

- Individual components in your architecture adds its own trace.
- Traces are made of segments and optionally sub-segments
- Traces can be annotate for extra metadata about 
- IAM is used for authorization
- KMS for encryption

## Enabling X-Ray

Your code has to import the X-Ray SDK. Supported languages:

- Java
- Python
- Golang
- Node.js
- .NET

Example SDK for Python:

https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python.html

Very little to add to the code, but by default you get:

- Calls to AWS services
- HTTP requests
- DB calls
- SQS (Queue)

On the compute you run (including on-prem), you have to install a daemon/agent to intercept the UDP packets. Lambda already run the daemon, except EC2 instances.

For Linux you just `curl` install an RPM.

For Beanstalk you have to either enable through console or use the `.ebextensions\xray-daemon.config` configuration options

```yaml
option_settings:
  aws:elasticbeanstalk:xray:
    XRayEnabled: true
```

## How It Works

X-Ray aggregates all of the data from the different service daemons and creates a service map from the traces, segments, subsegments.

## Troubleshooting

EC2:
- Check EC2 IAM Role
- Check to make sure the X-Ray Daemon is running
- Check X-Ray SDK is imported

EC2:
- Check EC2 IAM Role (AWSXRayWriteOnlyAccess)
- Check X-Ray SDK is imported

## Instrumentation

Measure performance, diagnose errors, write trace information. X-Ray SDK turns this on but you add app code with:

- interceptors
- filters
- handlers
- middleware

## Sampling Rules

Rules control how much data you want to trace. Changeable without changing your code.

Default Rule - Record the first request every second (reservoir) and 5% of additional requests (rate). 

Create your own rule and you can customize the reservoir and rate. Examples

- Reservoir of 10, Rate of 0.10 = Record requests every 10 seconds and 10% of the additional traces (lose some of the traces)
- Reservoir of 1, Rate of 1 - Record requests every 1 second and 100% of the additional traces (debugging and expensive)

## X-Ray APIs

Write APIs
- **PutTraceSegments** uploads segments info to X-Ray
- **PutTelemetryRecords** uploads telemetry info like SegmentsReceivedCount, SegmentsRejected, BackendConnectionErrors
- **GetSamplingRules** retrieves all of the sampling rules for what and how often it sends
- **GetSamplingTargets** is an advanced API
- **GetSamplingStatisticSummaries** is an advanced API

Read APIs
- **GetServiceGraph** retrieves the main graph of the traces
- **BatchGetTraces** retrieves traces by an ID
- **GetTraceSummaries** retrieve annotations and IDs for traces during a certain time frame. Subset of **BatchGetTraces**
- **GetTraceGraph** retrieves service graph by trace IDs

## X-Ray With Beanstalk

X-Ray Daemon is included with almost all platforms except Multicontainer Docker.

As stated above, for Beanstalk you have to either enable through console or use the `.ebextensions\xray-daemon.config` configuration options:

```yaml
option_settings:
  aws:elasticbeanstalk:xray:
    XRayEnabled: true
```

IAM Profile for Xray and App code enablement is still necessary.

## X-Ray with ECS

Use case 1:
On the ECS cluster you can create with EC2 instances, you can run the X-Ray Daemon container on each. The app containers will need to be able to reference the daemon.

Use case 2:
On the ECS cluster you can create with EC2 instances, you can run the daemon container as a sidecar image to all app containers. (More overhead)

Use case 3:
On Fargate you dont control the EC2 instances so you must use the sidecar model with each app container.

# CloudTrail

CloudTrail provides a history of events for your AWS Account supporting:

- Governance
- Compliance
- Auditing

It is on by default. Every event/API is logged from:

- SDK
- CLI
- Console
- AWS Services

Logs are exportable to CloudWatch Logs or S3.

Use case: if something is added or removed from your account, look at CloudTrail first.

## Events

Events are only stored for 90 days, so to keep them longer you need to use S3 and then use Athena to analyze.

**Management Events** are operation in your AWS acounts. Examples:
- AttachRolePolicy - Configuring Security
- CreateSubnet - Configuring rules
- CreateTrail - Create a CloudTrail

You can separate management events by read and write events. Write events are more likely to case problems

**Data Events** are object level events. They are not logged by default because they are high level volume of created data. For example:
- S3 Bucket activity (GetObject, PutObject API)
- Lambda invocations (Invoke API)

**CloudTrail Insights Events** are a way for AWS to try to detect unusual activity. You have to pay for this. Examples:
- Hitting service limits
- Large bursts of IAM actions
- Gaps in maintenance activity

Insights analyzed normal managment and then detects for unusual patterns

# CloudTrail versus CloudWatch versus X-Ray

CloudTrail - Auditing AWS Calls
CloudWatch - Metrics, Logs, and Alarms for application/cloud resources
X-Ray - Tracing and requires an app code component