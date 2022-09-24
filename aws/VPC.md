# Virtual Private Cloud (VPC)

Region based private network for cloud resources

Subnets allow you to partition your VPC. Subnets are AZ resources
- Public can access the net
- Private can't access the internet
- Subnets define access to the Internet and other subnets via Route Tables.

## Gateways

Internet Gateways (IGW)
- Public subnets use them to access the Internet

NAT Gateways and NAT Instances (self-managed)
- Private Subnets to access Internet, but can't be accessible from Internet
- NAT Gateway or Instance is created in the public subnet, then it can use the IGW

# Network ACLs (NACL) and Security Groups

NACL
- A firewall that controls traffic to and from subnet
- ALLOW and DENY rules
- Attached at subnet
- Rules are only IP Addresses
- Stateless

Security Groups
- A firewall that controls from an ENI/EC2 instance
- ALLOW rules only
- Rules include IP addresses and SGs.
- Stateful

VPC Flow Logs
- Captures information about IP traffic
  - VPC
  - Subnet
  - ENIs
- Useful for troubleshooting
  - subnets to internet
  - internet to subnets
  - subnets to subnets
- Traffic from all AWS managed services lile
  - ELB
  - ElastiCache
  - RDS
  - ...
- Write the flow logs to S3 or CloudWatch

# VPC Peering

Connect 2 VPCs, privately on the AWS Network and make them act like 1 network.

- They can't have an overlapping CIDR
- 3 VPCs must all be interconnected (no transitivity)

# VPC Endpoints

Create Endpoints that don't use the Internet, but private network

- Enhanced security and lower latency for AWS services which all have public endpoints
- For S3 and DynamoDB you can create a **VPC Endpoint Gateway** in your private VPC
- For all of the rest you use **VPC Endpoint Interface**

# Site to Site VPN

Connect an on-premise VPN to AWS
- Encrypted
- Goes over Internet
- Can't use VPC Endpoints

# Direct Connect (DX)

Physical Connection between on-prem and AWS
- Connection is private, secure, and fast
- Takes about a month to establish
- Can't use VPC Endpoints

# Three Tier Architecture

Typical architecture for the cloud

- Public Subnet - ELB
- Private Subnet - Auto-scaling Group of instances
- Data Subnet - RDS and ElastiCache

Wordpress example two-tier
- Public Subnet - ELB
- Private Subnets - Instances that share vie EFS using ENIs