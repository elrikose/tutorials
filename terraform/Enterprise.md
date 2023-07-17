# Terraform Enterprise

Terraform Enterprise is the self-hosted version of Terraform Cloud installed on a Linux VM
- Audit logging
- SAML SSO
- No resource limits to the system

# Requirements

External Services mode
- Postgres
- Cloud storage (S3, Azure, GCP)

Mounted Disk mode
- Everything is stored on VM

Demo mode
- Not recommended for production
- Data can be backed up with snapshots

Must have a Terraform Enterprise License and TLS Certificates

Linux OS Distributions
- Ubuntu
- Debian
- RHEL
- Amazon Linux
- Oracle Linux

Disk Space
- 10 GB of root volume
- 40 GB for docker volume
- 8 GB of RAM
- 4 CPU cores

# Air Gapped Environments

Terraform Enterprise is not on the internet
- Public Sector
- Large Enterprise

You must install the Air Gapped version of the software.

# Terraform Products

- OSS
- Terraform Cloud Free - 1 concurrent run
- Terraform Cloud Teams - 2 concurrent runs
- Terraform Cloud Governance - 2 concurrent runs
- Terraform Cloud Business - Unlimited runs, SSO, Self hosted agents, Audit logging, ServiceNow
- Terraform Enterprise (self-hosted) - Unlimited runs, SSO, Audit Logging, ServiceNow

Team management, Sentinel Policy, Cost Estimation is only on Teams or higher 
