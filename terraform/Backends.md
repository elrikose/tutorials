# Terraform Backends

A backend defines how operation are performed and state snapshots are stored. There are two types of backends

Standard Backends
- Store state only
- Third party backends like S3
- Must use the CLI to perform operations

Enhanced Backends
- Store state
- Perform terraform operations
- Two types:
  - local - file and state storage on local machine
  - remote - file and state stored in cloud, Terraform Cloud

# Standard Backends

Examples in cloud:
- AWS S3
- Azure Storage Accounts
- Google Cloud Storage
- Alibaba Object Storage Service (OSS)

Examples locally or in cloud:
- Artifactory (can't lock)
- Hashicorp Consul
- etcd (can't lock)
- Postgres
- Kubernetes
- HTTP 

AWS example: 

```js
backend "s3" {
    bucket = "terraform-bucket-state-abcdef"
    key = "state"
    region = "us-east-1"
}
```

Backups will only be local and does not require Terraform Cloud or a workspace.

# Local Backends

- State is stored on the local filesystem
- Performs operations on the local machine
- Locks using system APIs.

Local example defaults to local:

```js
terraform {
}
```

Override state location

```js
terraform {
  backend "local" {
    path = "path/to/state/tf.tfstate"
  }
}
```



# Remote Backends

Only two major remote backends:
- Terraform Cloud (OSS)
- Terraform Enterprise (on-prem)

Both basically give you a code build server called Terraform Cloud Run Environment.

When using a remote backend you have to set a Workspace.

```js
terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "acme-co"
    workspaces {
      name = "my-project"
    }
  }
}
```

If you specify a prefix instead, you will be prompted for the other workspaces that have that prefix, like:

- `my-project-dev`
- `my-project-prod`

```js
terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "acme-co"
    workspaces {
      prefix = "my-project-"
    }
  }
}
```

You can choose to pass the backend parameters with `terraform init -backend-config=backend.config.hcl`.

# Referencing Output State From Other Configuration

If you want to reference other state, put state in a datablock. It reads outputted values from the state:

```js
data "terraform_remote_state" "earlier_state" {
  backend = "local"
  config = {
    path = "path/to/state/tf.tfstate"
  }
```

```js
resource "aws_instance" "my_instance" {
  subnet_id = data.terraform_remote_state.earlier_state.outputs.subnet_id
}
```

Only output values exposed at the root level of the module are accessible. You can't access data or resource values.

# State Locking

Backends that lock state prevent writing to state and others from acquiring the lock.

- Most commands support disable state locking with the `-lock` command
- You can force unlock a state with `terraform force-unlock <lock-id> -force`

# Sensitive Backend Data

State files are stored in backends and can store sensitive data in the json.

- Don't share state files
- Don't commit state files to git

Terraform Cloud/Enterprise has more protections
- State file is only held in memory
- Encrypted in both transit and at rest
- Detailed audit logging in Terraform Enterprise

Bucket or Storage Accounts should have encryption and versioning turned on.

# Terraform Ignore

Often you want to limit certain folders from being uploaded to the remote backend. Use `.terraformignore`.

- If not present ignores `.git` and `.terraform/modules` by default
- You cant have multiple `.terraformignore` files in subdirectories. Only the root `.terraformignore` is read.
