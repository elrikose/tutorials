# Terraform Cloud

Hashicorp's SaaS Service for Terraform (https://app.terraform.io)

Features:
- State file management
- State history
- Previous Applies
- Variable injection
- SSO for Enterprises
- Cost Estimation
- Integrates with ServiceNow, Kubernetes

# Terms

Organization - account you login as
Workspaces - Part of an organization, unique run environment
Teams - RBAC assigned to multiple workspaces
Runs - Single Terraform run

# Workflow Types

Version Control - GitOps, pull requests and webhooks
CLI Driven - using `terraform` CLI
API Driven - using Terraform API

# Permissions / RBAC

Organization Level Permissions
- Manage Policies
- Manage Policy Overrides
- Manage Workspaces
- Manage Git Settings

Organization Owners have special powers
- Publish private modules
- Invite users to organization
- Manage teams
- View all secrets
- Manage organization permissions and settings
- Delete organizations
- Manage Agents

Workspace Level Permissions
- Read Runs
- Queue plans
- Apply runs
- Lock/Unlock workspaces
- Read variables
- Read/Write variables
- Read state outputs

Built-in Permission Sets
- Read - Read runs, read variables
- Plan - Queue plans, read variables
- Write - Apply runs, read/write variables

Workspace Admins - special role to give all permissions for workspace

# API Tokens

https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/api-tokens

Organization API Tokens
- Permissions across the organization
- Only one token valid at a time
- Only generatable from Org Owners
- Not recommended for general use

Team API Tokens
- Allow Access to workspaces
- Only one API token per team valid at time
- Any team member can generat the token
- Regeneration of token invalidates previous token

User API Tokens
- Attached to a user
- Most flexible
- Real user or service account user

# Private Registry

You can publish private modules across your organization
- All users in your org can view the private modules
- Using `terraform login` will obtain a token for Terraform cloud
- You have to manually set a team token in your CLI config

# Cost Estimation

Rough estimation of the cloud spend based on your runs

- Only available at Teams and Governance license level
- Limited support for modules

# Workflow Options

- You can choose a Terraform version for a workspace
- Always auto-approve
- Share state globally 

# SCM Support

- Github
- Gitlab
- Bitbucket
- Azure DevOps

# Run environments

A run environment is a virtual machine or container to execute your code.

Run environments get the following environment variables

- `TF_RUN_ID` - ID of the run (unique)
- `TFC_WORKSPACE_NAME` - Workspace name
- `TFC_WORKSPACE_SLUG` - full name of the org/workspace
- `TFC_CONFIGURATION_VERSION_GIT_BRANCH` - Branch name
- `TFC_CONFIGURATION_VERSION_GIT_COMMIT_SHA`
- `TFC_CONFIGURATION_VERSION_GIT_TAG`

# Cloud Agents

A way to run your terraform locally. Requires the Business license. 
- Agents only support Linux x86 or Docker.
- Requires 4 GB of disk and 2 GB of RAM
- Network access to Hashicorp URLs

