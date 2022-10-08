# CodeCommit, CodeBuild, CodePipeline, CodeDeploy

- CodeCommit - Store code in repos (Github)
- CodePipeline - Automation Pipelining
- CodeBuild - Build and Test (Jenkins)
- CodeDeploy - Deploy to EC2
- CodeStar - Manage dev activities
- CodeArtifact - Store built packages (Artifactory)
- CodeGuru - Code reviews with Machine Learning (ML)

# CodeCommit

Uses Git for version control of code. Useful for collaboration, backups, and auditing

Characteristics of CodeCommit
- Only Private Git Repositories
- No size limit on a repo
- HA
- Security with IAM
- Integration with Jenkins
- Cross account access
- If you don't see SSH in the configuration for the repo, that's because you are logged in as the root user.
- main is used now instead of master branch

Authentication
- SSH or HTTPS

Authorization
- IAM Policies

Encryption
- AWS KMS automatically encrypts repo
- In transit always because off SSH and HTTPS

Notifications
- You can assign on repo actions that are sent out via SNS target or a chatbot (Slack) target

Triggering
- SNS and Lambda are services you can trigger for repository events (push, create branch, delete branch, etc)

IAM
- There is a place in IAM for creating SSH Keys or HTTP creds for CodeCommit

# CodePipeline

Visual tool to orchestrate your CICD workflow. Here are example stages:

- Source - CodeCommit, ECR, S3, Github
- Build - CodeBuild, Jenkins
- Test - CodeBuild
- Deploy - CodeDeploy, Cloud Formation, ECS, Beanstalk, S3

Pipelines stop if a stage fails and you get info in the console.

You can have serial or parallel action groups in your stages, including a manual action.

S3 is the facilitator of storage of CodePipeline. Inputs and Outputs of stages are read/write from S3

CloudWatch Events (EventBridge) creates events for failed pipelines or canceled stages.

If a pipeline can't do something, check IAM perms. CloudTrail is also useful if what fails is an AWS action. One of the first things you do when you create a pipeline is create or ask for a IAM service role.

Source Stage
- Set a provider (CodeCommit, ECR, S3, Github)
- Choose repo/branch
- Use CloudWatch Events

Build Stage
- Set a provider (CodeBuild, Jenkins)

Deploy Stage
- Set a provider (CloudFormation, CodeDeploy, Beanstalk, ECS, S3)

# CodeBuild

Build instructions (buildspec.yml) at the root of the repo.

- Ouput logs is in S3 or CloudWatch Logs
- Build Stats in CloudWatch Metrics
- Notifications or failures in CloudWatch Events
- Failure Thresholds can trigger CloudWatch Alarms

Supported Build Environments
- Python
- Java
- Go
- Ruby
- PHP
- .NET Core
- Node.js
- Docker for anything else

CodeBuild container loads source and `buildspec.yml`. The container is a Docker image. 
- Optionally you can cache items to an S3 bucket.
- Artifacts go to an S3 bucket
- Logs can go to an S3 bucket or CloudWatch Logs

## buildspec.yml

- Must be at the root of your code repo
- There is an `env:` section for environment variables
  - `variables:` section is for plain text
  - `parameter-store:` is from SSM Parameter Store
  - `secrets-manager:` is from AWS  Secrets Manager
- `phases:` section has 4 phases
  - `install:` to install dependencies
  - `pre_build:` for pre-commands before the build
  - `build:` actual build commands like `mvn install`
  - `post_build:` cleanup or post processing artifacts (create zips)
- `artifacts:` section is what to upload to S3 (encrypted with KMS key)
- `cache:` files to cache for next time like that Maven `.m2` folder

## CodeBuild Agent

Use an agent for doing local builds when you can't figure out a problem in the cloud. Requires Docker

## Build Within VPC

By default, CodeBuild runs outside of your VPC, but you can specify the following if you want to let your build access your resources (integration tests, load balancer access, etc):

- VPC
- Subnet
- Security Group

Then your build can access EC2, RDS, ALB, etc

# CodeDeploy

Deploy the app automatically in a non-managed way. You can deploy with third party tools:

- Ansible
- Terraform

You can deploy to EC2 instances OR on-prem instances. They must have the CodeDeploy agent.

## Workflow

- Source code is in S3 or Github.
- Requires `appspec.yml`
- CodeDeploy Agent(s) query CodeDeploy looking for changes
- Instructions are run from `appspec.yml`
- Agent(s) report success or failure

## Attributes of a Deployment

- Application - unique name
- Deployment Platform - EC2/On-prem, Lambda, ECS
- Deployment Configuration - Rules for success or failure
- Deployment Group - Tagged EC2 instances (dev, test, prod)
- Deployment Type
  - In-place - EC2/OnPrem Deploy
  - Blue-Green - EC2, Lambda, ECS (not on-prem)
- IAM Instance Profile - Permissions to access S3/Github source code
- Application Revision - Code + revision of `appspec.yml`
- Service Role - IAM Role for the deployment (EC2, ECS, Lambda)
- Target Revision - The revision to deploy to a Deployment Group

## appspec.yml

- `files:` - list of source and destination for the deploy
- `hooks:` - instructions for the deploy of a new version (timeouts are optional). Each instruction specifies scripts or zips to expand. Instruction order:
   - ApplicationStop
   - DownloadBundle
   - BeforeInstall
   - Install
   - AfterInstall
   - ApplicationStart
   - ValidateService

## Deployment Configurations

Configurations
- One At A Time - If one instance fails then the deployment fails
- Half At A Time - 50% of the EC2 Instances
- All At Once - 100% of the instances. Good for development
- Custom - You chose the minimum (eg 75%)

Failures
- EC2 instances stay in a "Failed" state
- New deployments will go to the "Failed" instances first
- Rolling back will go back to an old deployment

Deployment Groups
- Tagged EC2 Instances
- Directly to a Auto Scaling Group
- Mix of ASG and Tags

## Setting Up A CodeDeploy Workflow

Setup IAM first
- Service Role - AWSCodeDeployRole for accessing AWS resources from Code Deploy
- Source Code Role - Pulling your code from an S3 bucket

### Create Deployment Application

- Set Application Name
- Platform
  - EC2
  - Lambda
  - ECS

### Create Deployment Group (EC2 Instances)

- Create an EC2 Instance
- Select Service Role above for IAM Role
- Configure a security group for HTTP/HTTPS
- Install CodeDeploy Agent on to EC2 Instance

```shell
# Installing CodeDeploy Agent
sudo yum update
sudo yum install ruby

# Download the agent (replace the region)
wget https://aws-codedeploy-eu-west-3.s3.eu-west-3.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status
```

- Tag EC2 (eg `Environment: Dev` )
- Create the Deployment Group giving it a name
  - Set the deployment type to in-place 
  - Set the environment type (EC2, ASG, on-prem)
  - Select the EC2 instances by Tag in previous step

- Deployment Confiuration - All At Once for Dev

### Create Deployment

- Select Deployment Group
- Where your app is stored (S3 or Github)
- S3 location must be a `.zip` or tarball
- Click Create Deployment

## CodeDeploy for ASG

Two options for deployment:
- In-place - Updates existing and creates new
- Blue Green - Creates a new ASG where you can choose how long to keep the old ASG. It must be using a application load balancer

## CodeDeploy Rollbacks

Deployments can rolled back be automatically (deployment fails, CloudWatch alarm) or manually. If it is rolled back , it is a new deployment with a new revision, not the old revision.

You can also disable rollbacks

# CodeStar

Integrated service for:

- Github
- CodeCommit
- CodePipeline
- CodeBuild
- CodeDeploy
- CloudFormation
- CloudWatch

Need to create an IAM role. Use CloudFormation for the project for infrastructure.

You quickly create all of the framework for a CICD project that uses EC2, Lambda, or Beanstalk.

Integrates with issue tracking systems:

- Github Issues
- Jira

Integrates with Cloud9 web IDE.

One Dashboard to rule them all. When you delete the project you can choose to delete all of the resource via that CloudFormation Stack

# CodeArtifact

Dependency Manager (Artifactory, Nexus) that is secure and scalable. Works with:

- Maven
- Gradle
- npm
- yarn
- pip
- NuGet

CodeBuild and other developers can retrieve dependencies from the service.

- Artifacts live within the VPC
- Create domains that contain 1-many repos
- You setup proxies to external public artifact repos like npm or maven central

# CodeGuru

Machine Learning service for code review and application performance recommendations.

- CodeGuru Reviewer - Built-in code reviews using a static analyzer (dev)
- CodeGuru Profiler - Performance recommendations at runtime (prod)

## CodeGuru Reviewer

Static Analyzer for:

- Critical Issues
- Security vulnerabilities
- Resource leeks
- Input validation

ML models came from analyzing 1000s of repos. Only supports Java and Python. But integrates with Github, CodeCommit, and Bitbucket.

## CodeGuru Profiler

Runtime behavior

- CPU capacity
- Decrease compute costs
- Heap summaries
- Anomaly detection
- Apps running in AWS or on-prem
- Almost no overhead

