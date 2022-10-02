# Elastic Container Service (ECS) and Elastic Container Registry (ECR)

There are 4 different ways to do container management in AWS:

- Elastic Container Service (ECS) - Proprietary platform
- Elastic Kubernetes Service (EKS) - Kubernets
- AWS Fargate - Serverless, works with ECA and EKS
- Elastic Container Registry (ECR) - registry for images

# Elastic Container Service (ECS)

Launches ECS Tasks on ECS Clusters.

ECS Launch Type
- User must provision and maintain the EC2 instance
- Each EC2 instance must run the ECS agent in the cluster
- Then AWS is in charge of stopping/starting containers

Fargate Launch Type
- Serverless
- Create Task definitions and than AWS runs ECS Task on the CPU/RAM you need
- To scale up, just increase the number of tasks.

# IAM Roles for ECS

EC2 Instance Profile
- Used by the ECS Agent
- Makes API calls to ECS
- Send container logs to CloudWatch
- Pull docker images from ECR
- Reference secrets in Secrets Manager or SSM Parameter Store

ECS Task Role
- EC2 and Fargate Launch Roles
- Task roles are defined in the task definition.
- Different container tasks may need different custom roles

# Load Balancers and ECS

Add an ALB in front of cluster. NLB is only recommended for high throughput. ELB is supported but not recommended

# Data Volumes

Use EFS to network mount onto ECS tasks

- Compatible with both EC2 and Fargate
- Any AZ can access the same data
- Fargate + EFS = Serverless
- NOTE: S3 can't be used as a data volume

# Auto Scaling

Simple to manually increase, but use AWS Application Auto Scaling to do it automatically. Three main scaling factors:
- CPU Utilization
- RAM Utilization
- Request Count/Target

You can also scale by
- CloudWatch Metrics
- CloudWatch Alarms
- Schedules

ECS Autoscaling is not the same as EC2 Autoscaling.

## EC2 Autoscaling

Ways to autoscale EC2
- Auto Scaling Group (ASG) based on CPU Utilization
- ECS Cluster Capacity Provider (pairs with a ASG) - easier to manage

# Rolling Updates

When updating a service, rolling updates provide a mechanism to control how many tasks can be started or stopped. Min and Max percentages decide how to update.

Min 50%, Max 100% = 4 tasks, 2 will stop, update, then the other 2 will stop and update.
Min 100%, Max 150% = 4 tasks, 2 will update (now 6), then 2 will stop and update because at 100%, then the last 2 will stop. Left with 4

# Solutions Architecture

EventBridge can have a rule to run ECS tasks. 

Example 1: Event Driven Activity with EventBridge
- User uploades object to bucket
- EventBridge gets an event that the upload happens
- Rule to run an ECS task
- ECS task gets the object and adds info to a database like DynamoDB

Example 2: Scheduled Task
- EventBridge runs on a schedule
- Kicks off a Rule on an ECS Task
- ECS Task does batch processing of an S3 bucket

Example 3: Event Queue with SQS Queue
- ECS Tasks poll from SQS Queue
- More items in the queue you can scale up the tasks

# Task Definitions

Task Definitions are JSON manifest files on how to spin up docker images. The UI helps build the JSON.

Definition contains:
- Image name
- Ports for container and host (EC2)
- Memory and CPU
- Environment variables
- Network information
- IAM Role
- Logging (CloudWatch)

It is like docker compose, you can define up to 10 images in a definition file.

## EC2 Instance Types
- if you don't specify a host port in the definition, you get a random port via Dynamic Host Port Mapping.
- The ALB gets the port automatically from the ECS service.
- Security group for the EC2 intances must allow any port so the ALB can access it.

## Fargate Instance Types
- Each task gets a unique private IP
- Only define the container port since there is no host port
- ALB only has to allow 80/443 for HTTP

## IAM Roles

Roles are assigned at the task definition level and passed off to the services via inheritance.

## Environment Variables

- Hardcoded in the task definition
- SSM Parameter Store (API keys)
- Secrets Manager (passwords)
- Load through S3 bucket 

## Data Volumes

How do you share data volumes between containers?

- EC2 Tasks - Right on the EC2 instance
- Fargate - Tied directly to the containers (ephemeral)

Above is only for ephemeral usage between multiple containers or when a container is processing the data  to other locations (sidecar pattern)

# Tasks Placement (EC2 Only)

The method ECS determines of where to put a new container on the cluster, based on CPU, memory, available port. And how to scale the cluster in if containers terminate.

Define:
- Task placement strategy
- Task placement constraint

## Task placement strategy

Identify the EC2 instances that have enough CPU/memory/port from the definition.
 - Binpack - least available CPU or memory minimizing cost (packing the containers)
 - Random - Placed in random order (not optimal)
 - Spread - Spread across the cluster based on a value (eg AZ)

 ## Task placement constraints

 - distinctInstance - Tasks are on different instances
 - memberOf - place tasks that will satisfy an expression using a cluster query language (place containers only on t2 instance types)

# Elastic Container Registry (ECR)

You can create private repositories for storage of container images, but there is also a public one too:

https://gallery.ecr.aws

- Backed by S3
- Fully integrated with ECS
- Access is controlled by IAM
- Registry supports
  - vulnerability scanning
  - versioning
  - image tags
  - image lifecycle

  ## Login

  Use AWS CLI to login:

  ```
  aws ecr get-login-password --region region | docker login --username AWS --pasword-stdin ecr-fqdn
  ```

  Then you can `docker pull` and `docker push` using the ecr FQDN.

  If you can't pull or push then you have IAM perm problems.

  # Elastic Kubernetes Service (EKS)

  Managed Kubernetes (K8s) on AWS. K8s is an open-source system for deploying, scaling, and managing containers.

  Competitor to ECS, which is not open-source. You can use EC2 or Fargate for serverless containers.

  Use EKS instead of ECS if you already are on Kubernetes as it is cloud agnostics.

  - Managed Node Groups - AWS manages nodes for you, part of an ASG
  - Self Managed Nodes - You have to create them yourself and then register
  - AWS Fargate mode - No nodes are managed

## Data Volumes

You need to specify a StorageClass in K8s which uses a Container Storage Interface driver. Then you can use
- EBS
- EFS 
- FSx for Lustre
- FSx for NetApp ONTAP

  