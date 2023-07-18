# Terraform Workspaces

There are two types of workspaces

- CLI Workspaces
- Terraform Cloud Workspaces

They used to call them Environments. They are similar in concept to git branches.

```sh
$ terraform workspace list
* default
```

- In Local State the workspace states are stored in `terraform.tfstate.d`
- In Remote State they are stored right in the backend.
- There is named value that you can use called `terraform.workspace` Interpolate `{terraform.workspace}`

# Multiple Workspaces

Supported in a number of different backends
- Azure
- Consul
- Google
- Kubernetes
- Local
- Postgres
- Remote
- S3

Multiple workspaces allow you to store multiple states, which makes it easy to do a `dev`, `prod`, etc.

# Terraform Cloud Run Triggers

You can connect up workspaces togethers with triggers 1 workspace can attach to 20 source workspaces. 

You can consume data from those other workspaces

# Workspace CLI Commands

List all the workspaces (current workspace has a `*`)

```sh
$ terraform workspace list
  default
* dev
  prod
```

Show the current workspace

```sh
$ terraform workspace show
dev
```

Select a different workspace

```sh
$ terraform workspace select prod
Switched to workspace "prod"
```

Create a new workspace

```sh
$ terraform workspace new staging
Created and switched to workspace "staging"
```

Delete a workspace

```sh
$ terraform workspace delete staging
Deleted workspace "staging"
```

# Local vs Terraform Cloud Differences

Data is stored differently

Local
- Terraform files are stored on disk
- Variables are stored in `.tfvars` files
- State is on disk or in remote backend
- Creds are stored in shell or environment

Remote
- Terraform files are stored in a version controlled repo
- Variables are stored in workspace
- State is in workspace
- Creds are stored in workspace as sensitive

# Sentinel

Sentinel is an embedded policy as code framework, automating regulatory or governance policies.

Sentinel is part of Team & Governance. 

- Embedded - Policy enforcement actively rejecting behaviors instead of detecting
- Fine grained, conditional policy - conditionalize one policy based on another policy
- Enforcement levels - Advisory, soft, hard level
- Mutli-cloud

Benefits of Policy as Code
- Sandboxing
- Codification
- Version Control
- Testing
- Automation

Sentinel specific
- The Sentinel Language is built to be non-programmer friendly
- There is a CLI tool for dev and testing
- There is a test framework for automation

Sentinel Policy examples:
- Restrict OS image types
- Force certain tags on resources
- Disallow 0.0.0.0/0 CIDR blocks in security groups
- Restrict instance types 
- Require buckets to be encrypted
- Restrict providers are allowed

Sentinel sits in between Plan and Apply