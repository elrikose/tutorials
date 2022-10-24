# SQS, SNS, Kinesis

Applications will almost always need to communicate with other applications or services.

Synchronous Communication - direct channel between two apps
Asynchronous Communication - events are queued

Synchronous communication can cause problems if there is overwhelming demand. For example if requests jump by an order of magnitude (10x, 100x, etc). To handle this kind of use case you **decouple** your application from your messaging platform:

- Simple Queuing Service (SQS) - uses queues, producer, subscriber model
- Simple Notification Service (SNS) - uses publish/subscribe model
- Kinesis - real time streaming, big data

# Amazon Simple Queuing Service (SQS)

Producer/Consumer model where the messages are processed through a queue.

There can be many producers and consumers with a queue in between.

Two queue types:

- Standard queue
- FIFO

## Standard Queue

- Oldest service > 10 years old
- Decouples applications
- Messages must be read by consumer within 4 days (default). Maximum 14 days or they are deleted.
- Unlimited number of messages
- Unlimited throughput
- Very low latency (sub 10ms)
- Max message size of 256 KB.
- Duplicate and out of order messages are possible on the consumer end 

Producer End
- Uses **SendMessage** API from the SDK
- Message persists in queue until consumer deletes it or retention policy is hit.

Example Message
- Order ID
- Customer ID
- Customer Info
- Other data

Consumer End
- Consumer types: EC2, on-prem servers, Lambda
- Consumer polls queue
- Consumer can receive up to 10 messages at a time with **ReceiveMessage**
- Messages are processed (Added to DB, written to file, etc)
- Messages are deleted using **DeleteMessage** API from the SDK.

Consumer Scaling - Since messaging is decoupled, to scale you just add new instances horizontally.
- Perfect for Auto Scaling Groups (ASG)
- Scale based on the CloudWatch metric for queue length **ApproximateNumberOfMessages**
- Alarm can go off to scale the ASG.

## SQS Use Case: Video Processing

Common use case on exam:

- Front End UI Producers accepts the video and calls **SendMessage**
- SQS handles message to an ASG of Consumers
- Consumer video processors **ReceiveMessage** and deal with video and write to S3 bucket

## SQS Security

- HTTPS for communication encryption
- KMS for at rest encryption
- Client-side encryption

IAM  policies can be used to limit access to SQS internal to an account

SQS Access policies can be used for
- cross account access
- access from other AWS services (SNS, S3)
- similar to S3 Bucket policies

## SQS UI

- Create a SQS Queue
- There is a way to send and receive messages right from the UI
- Great way to debug a message send/receive
- You can send anything you want including strings and attributes (tags, metadata)

## SQS Access Policies

Cross Account Policy example to allow sending a message from one account (111122223333) to another (444455556666):

```json
{
   "Version": "2012-10-17",
   "Id": "Queue1_Policy_UUID",
   "Statement": [{
      "Sid":"Queue1_SendMessage",
      "Effect": "Allow",
      "Principal": {
         "AWS": [ 
            "111122223333"
         ]
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-2:444455556666:queue1"
   }]  
}
```

Allow receiving a message from one account (444455556666) to another (111122223333):

```json
{
   "Version": "2012-10-17",
   "Id": "Queue1_Policy_UUID",
   "Statement": [{
      "Sid":"Queue1_Receive",
      "Effect": "Allow",
      "Principal": {
         "AWS": [
            "111122223333"
         ]
      },
      "Action": [
         "sqs:ReceiveMessage"
      ],
      "Resource": "arn:aws:sqs:*:444455556666:queue1"
   }]
}
```

You can allow a bucket event like uploading an object to send a message

```json
{
   "Version": "2012-10-17",
   "Statement": [{
      "Effect": "Allow",
      "Action": "sqs:SendMessage",
      "Principal": {
         "AWS": "*"
      },
      "Resource": "arn:aws:sqs:us-east-2:444455556666:queue1",
      "Condition":{
        "ArnLike": { "asw:SourceArn":"arn:aws:s3:*:*:bucket1" }
      }
   }]  
}
```

## SQS Message Visibility

Once a message is polled by a consumer, it is made invisible to other consumers for a default of 30 seconds. 

Consumers have to:

- delete the message 
- call the **ChangeMessageVisibility** API for more time

Either will put it is put back in the queue as visible.

If the visibility timeout is 

- too long - crashes will take hours to get put back into queue
- too short - you could get duplicates

## SQS Dead Letter Queue

Mechanism to limit how many times a consumer can try to process a message via **MaximumReceives**. 

- Messages can be sent into a Dead Letter Queue (DLQ) after maximum receives.
- Use case is debugging messages that may be malformed or can't be processed
- DLQs can expire messages after a while so set that queue to a retention of 14 days.

Once you fix the consumer or find out why the message wasn't processed, you can "redrive" it back to the source SQS queue.

## Delay Queue

Allow messages to be delayed by consumers up to 15 minutes. Default is 0.

- Default can be set in the queue config
- Override when sending a message via **DelaySeconds** parameter

## Long Polling

Enable in applications to decrease the amount of API calls to SQS. Consumers wait for messages to arrive in none are in the queue.

- Wait time is 1 to 20 seconds. Prefer 20 seconds.
- Enable at the queue level
- Enable at the polling level via **WaitTimeSeconds**

## SQS Extended Client

Java Library that uses an S3 bucket to send large messages over 256 KB. The way it works:

- Large message is written by producer to S3 bucket
- Small metadata message is sent to SQS with pointer to S3 bucket
- Consumer reads message and then gets the rest of the message from S3 bucket

Use case: Message is a video file to process. Videofile is saved to S3. Metadata is sent to app

## Important SQS APIs

- CreateQueue (MessageRententionPeriod)
- DeleteQueue
- PurgeQueue deletes every message
- SendMessage (DelaySeconds)
- ReceiveMessage
- DeleteMessage
- MaxNumberOfMessages to receive at consumer (default 1, max 10)
- ReceiveMessageWaitTimeSeconds for long polling
- ChangeMessageVisibility for message visibility timeout

SendMessage, DeleteMessage, and ChangeMessageVisibility have a batch mode that can reduce your costs by not sending as many items

## FIFO Queues

First In First Out (FIFO) ensures ordering of messages.

Limited throughput over Standard:
- 3000 messages/s with batch mode
- 300 messages/s without batch mode

Messages are processed in order by consumer. Ability to send only 1 message (no dupes)

The queue name in the UI MUST end with `.fifo`. A Deduplication ID is mandatory except when content based deduplication is enable on the queue..

### FIFO Deduplication

The message deduplication ID is the token used for deduplication of sent messages. If a message with a particular message deduplication ID is sent successfully, any messages sent with the same message deduplication ID are accepted successfully but aren't delivered during the 5-minute deduplication interval.

Producers provide message deduplication ID values for each message in the following scenarios:

- Messages sent with identical message bodies that Amazon SQS must treat as unique.
- Messages sent with identical content but different message attributes that Amazon SQS must treat as unique.
- Messages sent with different content (for example, retry counts included in the message body) that Amazon SQS must treat as duplicates.

Two dedup methods
- SHA-256 based de-dupe method of the message body
- Provide a Dedup ID

### FIFO Grouping

If you specify differing group IDs, the messages within a group will be ordered. 

- Parallel processing as you can have multiple consumers
- Ordering across groups is not guaranteed

# Amazon Simple Notification Service (SNS)

Send one message to multiple recipients. SNS uses the Publish/Subscriber (Pub/Sub) model. The service publishes an event and the subscriber receives that event and acts on it.

Publisher sends an event to an SNS Topic. Subscribers get all messages unless they filter it.

Limits
- 12.5 M subscriptions per topic
- 100 K topics

Subscriber Types
- Email
- SMS/Mobile
- HTTPS endpoints
- SQS
- Lambda
- Kinesis Data Firehose

Many AWS services send directly to SNS:
- CloudWatch Alarms
- ASG Notifications
- CloudFormation changes
- AWS Budgets
- Lambda
- S3 Bucket Events
- RDS Events

Workflow on how to use:

- Create a SNS topic
- Create 1 to many subscriptions
- Publish to the topic

Also works via a Direct Publish for mobile push notification

- Create a platform application
- Create an endpoint
- Publish to the endpoint
- Integration with Apple APNS, Google, GCM, etc

## SNS Security

- HTTPS for communication encryption
- KMS for at rest encryption
- Client-side encryption

IAM  policies can be used to limit access to SNS internal to an account

SNS Access policies can be used for
- cross account access
- access from other AWS services (S3)
- similar to S3 Bucket policies

## SNS and SQS Fan Out

It is a common pattern to have an SNS suscriber be multiple SQS queues to fan out messages to different back end services.

Benefits:
- Data persistence
- Delayed processing
- Retries
- Add more SQS subscribers over time

Note: SQS must have an access policy to allow SNS to write.

Use case for Fan Out:
- S3 bucket can only have one event per prefix
- S3 Event -> SNS Topic -> SQS Queues

Storing Events
- Service -> SNS Topic -> Kinesis Data Firehose -> Amazon S3

SNS FIFO Topic
- Used to make sure that notifications are ordered.
- The **only** susbscriber is a SQS FIFO
- Topic name **must** end in `.fifo`
- Producer creates a number of messages and sends to SQS FIFO in order
- Uses Group IDs and Dedup ID.

Message Filtering
- JSON policy to filter notifications
- Subscribers that don't have a filter policy receive all notifications
- JSON policies look at the notification message and if it is of a certain state it can process or ignore.

# Kinesis

Service that can collect, process, and analyze real-time data streams:

- App logs
- Metrics
- IoT telemetry

4 Main Services

- Kinesis Data Streams - capture, process, store data streams
- Kinesis Data Firehose - Store data streams into AWS data stores
- Kinesis Data Analytics - analyze data streams with SQL or Apache Flink
- Kinesis Video Streams - capture, process, store video streams

## Kinesis Data Streams

Data Streams are made up of multiple shards (Shard 1 ... Shard N)

- Producers use AWS SDK to record data to the streams
  - Applications
  - Clients (Mobile/Desktop)
  - SDKs (Kinesis Producer Library)
  - Kinesis Agents
- Data stream producer records contain:
  - Partition Key
  - Data Blob (<= 1 MB)
  - Can be sent at 1 MB/second/shard or 1000 messages/second/shard

- Consumers can be 1-to-many:
  - Applications (Kinesis Consumer Library, AWS SDK)
  - Lambda
  - Kinesis Data Firehose
  - Kinesis Data Analytics
- Data stream consumer records contain:
  - Partition Key
  - Sequence number
  - Data Blob (<= 1 MB)
  - Shared consumer rate: can be received at 2 MB/second for **all** consumers
  - Enhanced consumer rate: can be received at 2 MB/second/shard per consumer

Other Attributes
- 1 day to 365 day data retention
- You can reprocess data
- Kinesis data is immutable. You can't delete it
- Data with the same partition key goes to the same shard in order

Data Capacity (Provisioned)
- Choose number of shards and manually scale them
- You can also scale by API
- You pay per shard hour
- 1 MB/s in (1000 records/s) and 2 MB/s out

Data Capacity (On-demand)
- Newer mechanism
- No need to setup the shards/capacity beforehand
- 4 MB/s in (4000 records/s)
- Scales based on throughput peak over the last 30 days
- Pricing more expensive: Per stream/hr and data in/out per GB of data

Security
- Control access with IAM
- Encryption with HTTPS and KMS 
- Client Side encryption
- VPC Endpoints are available for access with VPC
- CloudTrail for auditing

## Kinesis Producers

Source implementations:
- Simple producer: AWS SDK
- Kinesis Producer Library: C++, Java, batch, retries
- Kinesis agents: application lof files

**PutRecord** API can be used:
- Add a single record
- Batch multiple records to reduce costs and inmprove throughput

Partition Keys can be anything (eg Device IDs)
- Keys are hashed to target a certain shard
- In multi-shard approaches, make sure partition keys are balanced to not target too much to one shard. (hot partition)
- Apps get ProvisionedThroughputExceeded exceptions if they throughput is too much
- Implement exponential backoff to retry PutRecord requests

## Kinesis Consumers

Classic (Shared) Fan-out Consumer - pull
- **GetRecords** API
- Each Consumer on a shard shares the 2 MB/s consumption rate
- If 4 consumers on a shard, they each max at 500 KB/s
- Max 5 GetRecords calls/second
- Latency is about 200 ms
- Throttling: Returns 10 MB (throttles for 5 seconds) or 10K records
- Use Case: low number of consuming application, minimize cost

Enhanced Fan-out Consumer - push
- **SubscribeToShard** API
- Each Consumer on a shard shares the 2 MB/s consumption rate
- The Shard "pushes" the data to the consumer
- Soft limit of 5 consumer applications, but can be increased by quota bump
- Latency is about 70 ms
- Use Case: Multiple applications for same stream, high cost

Lambda can be Consumers
- Call **GetBatch** to save streams to serverless DynamoDB
- Can use both Classic and Enhanced fan-out
- Must be batch reads, configuable batch size and batch window
- Processes up to 10 batches/shard simultaneously

## Kinesis Client Library (KCL)

Java library for reading data streams.

- Each shard is read by 1 KCL app instance max
  - 2 shards = 2 KCL instances maximum
  - 4 shards = 4 KCL instances maximum
- Multiple consumers can read multiple shards, but more ideal to have 1 shard per one KCL app.

App instance needs IAM access to DynamoDB because that is how progress is managed amongs workers and shards.

Library support
- KCL 1.x only supports classic/shared fan-out
- KCL 2.x supports both classic and enhanced fan-out

## Kinesis Shard Splitting

Split a shard to reduce a (hot) shard that is receiving too much data from the producer.

- No automatic scaling in Kinesis Data Streams. Manual only
- Old Shard is closed and data is expired
- New Shards have new names
- You can only split 1 shard into 2.

## Kinesis Shard Merging

Group 2 (cold) shards with low usage to reduce capacity and save money.

- Old Shards are closed and data is expired
- New Shard has a new name
- You can only merge 2 shards into 1.

# Kinesis Data Firehose

Producer / Consumer model like Kinesis. Data can be treansformed by Lambda and that batch written to destinations.
- No administration
- Automatic scaling
- Failed data ends up in a bucket
- Near Real-time processing (full batches over 1 MB, otherwise 60 second latency)
- Pay for throughput data

Receives data also from all Kinesis Data Streams sources including:
- Kinesis Data Stream
- Amazon CloudWatch 
- AWS IoT

AWS Destinations:
- S3
- Amazon Redshift (data warehousing) - intermediate through S3
- Amazon Elasticsearch

3rd Party Destinations
- Datadog
- Splunk
- New Relic
- Mongo DB

Custom Destinations
- HTTP Endpoints

## Kinesis Data Streams versus Firehose

Kinesis Data Streams
- Real-time processing (~200ms)
- Manually manage producers and consumers
- Manualy scale shards (splitting/merging)
- Retain data 1-365 days
- Replay the data

Kinesis Data Firehose
- Fully managed
- autoscaling
- Load data into S3, AWS Service, 3rd Party Services
- Near Real-time (within 60 seconds)
- No data storage or replay ability

## Kinesis Data Analytics

SQL Applications
- Sources: Kinesis Data Streams, Kinesis Data Firehose
- SQL Statements to do the analytics
- S3 data for enriching the data
- Destinations: Kinesis Data Streams, Kinesis Data Firehose
- Automatic scaling
- Cost is data consumption rate
- Use cases:
  - Time based analytics
  - Dashboarding and metrics (real-time)

Apache Flink
- Sources: Kinesis Data Streams and Amazon MSK (Kafka)
- Write app using Java or SQL to process stream
- Useful for advanced querying
- Must create a cluster on AWS
  - Compute resources, autoscaling
  - Backups
- Cannot read from Kinesis Data Firehose

# Kinesis versus SQS FIFO Ordering

Kinesis
- Uses Shards to scale througput
- 1 consumer per shard
- Use the partition key to have something process on the same shard for ordering

SQS FIFO
- Only 1 Queue
- Use the Group ID to group requests to same consumer

# Summarizing Messaging

SQS:
- Consumers "pull" the data from producers
- Data is deleted after being consumed
- As many consumers as you want
- Ordereing is only guaranteed in FIFO Queue
- Delay messages individually

SNS:
- Publish / Subscriber model "push"
- 12.5 M subscribers
- Data is not persisted
- 100K topics
- Fan-out patterns
- FIFO

Kinesis:
- Standard: "pull" data
- Enhanced: "push" data
- Replay data
- Big Data use case
- Ordering at the shard level
- Data expires 1 day to 365
- Provisioned versus on-demand capacity mode