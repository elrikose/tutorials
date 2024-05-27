# GitHub Environment Variables

Environment Variables are used to define values that can be passed to jobs, steps, and actions. These values

## Default Environment Variables

There are many default environment variables that can be used in both a cloud-hosted and self-hosted runner. A default environment variable starts with a `$` and are uppercase.

- `GITHUB_SHA` - the SHA value of the commit or tag
- `GITHUB_REF` - the fully formed Git ref for the branch or tag
- `GITHUB_WORKFLOW` - the name of the workflow. If one isn't specified, it uses the path name.
- `RUNNER_OS` - one of `Linux`, `Windows`, or `macOS`
- `RUNNER_ARCH` - One of `X86`, `X64`, `ARM`, or `ARM64`

## Custom Environment Variables

Custom environment variables are defined by the workflow creator/editor and can be defined at these levels:

- Workflow
- Job
- Step

Here is an example:

```yaml
name: Environment example
on:
  workflow_dispatch

env:
  WORKFLOW_LEVEL: "Workflow"

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      JOB_LEVEL: "Job"

    steps:
      - name: "Using the Environment"
        run: echo "$WORKFLOW_LEVEL $JOB_LEVEL $STEP_LEVEL"
        env:
          STEP_LEVEL: "Step"
```

## Contexts

Contexts are similar to environment variables. Contexts can be used in the code itself instead of actions the runners do. For example `github.ref` here only allow it to be user on main. You couldn't use `$GITHUB_REF`:

```yaml
jobs:
  prod-check:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
```
