# Troubleshooting

4 Types of errors in Terraform and how to fix:

Language/Syntax
- `terraform fmt`
- `terraform validate`

State Errors - Remote resources different from state
- `terraform -refresh-only`
- `terraform -replace`

Core Errors - Bug in Terraform
- Hard to fix
- TF_LOG files
- Log a Github issue

Plugin/Provider Error - An API has changed and the provider doesn't deal with it.
- Hard to fix
- TF_LOG files
- Log a Github issue

# Debugging Terraform

Detailed logs can be enabled by setting the `TF_LOG` environment variable to:

- TRACE
- DEBUG
- INFO
- WARN
- ERROR
- JSON

You can separate logs by Core or Provider with `TF_LOG_CORE` or `TF_LOG_PROVIDER`.

`TF_LOG_PATH` is the log path

# Crash Logs

Terraform is written in Golang, so if it ever crashes it creates a `crash.log`. Create a Github ticket with the crash.