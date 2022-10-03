# Elastic Beanstalk

Web Apps typically have the same architecture:

- Route 53 for DNS
- Load Balancer in the Front
- Scaling group in the middle
- Database later in the rear

Beanstalk is a managed service that provides a consistent way to deploy above, including monitoring, instance config, and others

Beanstalk if free, but you pay for the architectural bits (ALB, EC2, RDS, etc)

# Components

- Application - Collection of environment, versions, config
- App Version
- Environment
  - Resources that define the app version
  - Tiers: Web servers versus worker tier
  - Dev, Test, Prod per application for example

Language support
- Golang
- Java
- .Net
- Node JS
- PHP
- Python
- Ruby
- Packer
- Docker

Or create your own language support.

Once you create your application you can go edit configuration like
- EC2 Instances
- Load Balancer
- Monitoring
- Network
- Database

# Deployment Modes

2 Modes
- Single Instance - No ELB, elastic IP
- High Availability (HA) with Load Balancer

Single Instances are good for dev, HA for prod.

# Deployment Updates

- All at once - fast, but there is downtime
- Rolling - update a few at a time
- Rolling with additional batches - Create new instances with new updates 
- Immutable - Create new instances, get the environment up, then change out ALL instances when ready

## All at once

4 instances. Stop all instances. Create new instances with new version. 

- No additional cost.
- Good for dev environments
- Fast iterations

## Rolling

4 instances. Stop 2 instances. Update the code, then roll on to the next 2.

- Running both versions at the same time
- No additional cost.


## Rolling with additional batches

4 instances. Add 2 more instances with code. Stop 2 instances, update the code.

- Running both versions at the same time
- Some additional cost.
- Good for prod

## Immutable

Create a new ASG with instances. Then terminate 

- Zero downtime
- High cost, double capacity
- Long deployment
- Quick Rollback
- Great for prod
- Most costly

## Blue / Green

- Not really a Beanstalk feature
- New staging environment
- Validate the staging area
- Roll back if there are problems.
- Route 53 + weighted policies to swithc to staging

## Traffic Splitting

AKA Canary Testing

- Deploy to new ASG with same capacity
- Send a small percentage to new ASG
- Do check, look for failures and roll back the Route 53
- No App Downtime

# EB CLI

EB CLI - An additional CLI outside of the `aws` CLI. Useful for automating workflows for CI/CD

Command Examples:
- eb create
- eb status
- eb health
- eb events
- eb logs
- eb open
- eb deploy
- eb config

# Deployment Process

- Include dependency description (eg requirements for Python)
- Package your code as a .zip file
- Upload the zip as a new app version
- Deploy using the Console or CLI

Behind the scenes the zip file is stored in an S3 bucket, dependencies will resolve and the application will start.

# Lifecycle Policies

EB can only store 1000 app versions. Use a lifecycle policy to phase out old app versions based on time or how many. 

- Current versions are not deleted.
- Option to not delete the source zip in S3.

# Extensions

Anything described in the Console can be specified in the `.ebextensions/` dir in the zip file.

- Must be YAML or JSON format
- Extensions must end with `.config`
- `option_settings` key in `environment-variables.config` can mod default settings
- Ability to specify resources such as RDS, ElastiCache, etc
- Any resources that get added are deleted if the environment disappears.

# Beanstalk and CloudFormation

Beanstalk uses CloudFormation under the hood. CloudFormation is a declarative way to create and setup AWS services.

Benefits
- Makes Beanstalk extensible
- Define AWS resources in your `.ebextensions/` 

# Cloning

Easy to clone the exact environment with the same configuration. All AWS resources/config is the same. After cloning you can change settings.

# Migrations

Load Balancers can't be changed once the Beanstalk is created. You have to 

- Create a new beanstalk
- change the beanstalk to a different load balancer
- Deploy app
- Update DNS or swap the URL

There is no easy way to decouple an RDS database from one environment to another. 

- Go to RDS and protect the database from being deleted
- Create a new environment without RDS and point your app to the db.
- Perform a Swap URL and the RDS will sill be attach
- A Beanstalk delete will fail, go to CloudFormation to manually delete

# Beanstalk with Docker

Docker is a deployment mechanism in Beanstalk.
- Deploy a `Dockerfile`
- Deploy a `Dockerrun.aws.json` that points to a b uilt image
- Single container deploys **don't** use ECS
- Multi container deploys create ECS clusters, EC2 instances, load balancer
- Multi container deploys must use the `Dockerrun.aws.json` which creates the ECS task definition.

# Advanced Concepts

## How do you do HTTPS?

1. Load it on the load balancer
2. File in the zip: `.ebextensions/securelistene-alb.config`

You can use AWS Cert Manager. And must configure port 443 in the security group. 

It is also advisable to redirect HTTP to HTTPS.
- On EC2 Instances
- On load balancer with rule

Health checks should be re-directed

## Worker Environment

Push long background tasks to a Worker Environment
- Video processing
- Compression
- Periodic tasks are defined in `cron.yaml`

Often Web Tier sends messages to a SQS Queue on a Worker Environment since there is no UI.

# Custom Platform for Code

The only time this makes sense is when you can't use Docker.

From scratch:
- OS
- Software dependencies
- Scripts that Beanstalk runs (platform specific)
- Requires AMI in `Platform.yaml`.
- Build the platform with Packer

Custom Images - change existing Beanstack Image platforms
Custom Platform - entirely new

