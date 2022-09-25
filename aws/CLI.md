# AWS Command Line Interface (CLI)

Default region is us-east-1 if not specifed

# Dry Run

There is a dry-run option (`--dry-run`) to most CLI commands

You do this because some commands could be expensive. Dry Run tests to make sure you have all of the permissions.

# STS to Decode AWS CLI errors

The CLI returns error codes that are long strings and you use the STS command-line to decode them.

```shell
aws sts decode-authorization-message --encoded-message <encoded string from error>
```

# AWS EC2 Instance Metadata

Allow EC2 instances to learn about themselves by using this API:

http://169.254.169.254/latest/meta-data

- You can get the IAM Role name, but you **cannot** get the IAM policy 

# CLI Profiles

The .aws directory has a config and credentials file

- The config file defines profiles and defaults for the profile.
- The credentials files lists in an ini fashion creds per profile.

# MFA with CLI

You have to create a temporary session for MFA.

Must use STS GetSessionToken API

```
aws sts get-session-token --serial-number <arn of MFA device> --token-code code-from-token --duration-seconds 3600
```

You get a JSON result with the access key and session token along with an expiration timestamp.

# AWS Quotas on API calls

There is a rate limit for API calls
- DescribeInstances for EC2 is 100 calls/second
- GetObject on S3 is 5500 per second per prefix

As well as services:
- 1152 vCPU for standard instances
- Open a ticket with AWS to increase
- There is also a service quota API

If you get a ThrottlingException you can use Exponential Backoff
- Retry mechanism already in the AWS SDK API calls
- If using the API yourself, you must implement your own.
- The symptom is you start getting 5xx server errors
- Don't implement on 4xx errors

Exponential Backoff
Retry seconds: 1 then 2 then 4 then 8 seconds

# CLI Provider Order

The CLI uses this order for where it gets creds or environment:

1. Command-line options --region, --output, and --profile
2. Environment: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
3. CLI credentials file: ~/.aws/credentials
4. CLI config file: ~/.aws/config
5. Containers (ECS tasks)
6. EC2 Instance Profiles

Use IAM Roles as much as possible with internal EC2

Never store creds in code

# Signing AWS API requests

- access key and secret key are required for signing
- CLI and SDK sign for you automatically
- S3 doesn't require signing

If you are going to use your own APIs you need to use AWS HTTP requests using Signature v4 (aka SigV4)

