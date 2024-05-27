# Introduction

# What are GitHub Actions

From the Certification course [study guide](https://learn.microsoft.com/en-us/training/modules/github-actions-automate-tasks/2-github-actions-automate-development-tasks):

>GitHub Actions are packaged scripts to automate tasks in a software-development workflow in GitHub. You can configure GitHub Actions to trigger complex workflows that meet your organization's needs; each time developers check new source code into a specific branch, at timed intervals, or manually. The result is a reliable and sustainable automated workflow, which leads to a significant decrease in development time.

# How to Create Actions

- Search for GitHub Actions in the [GitHub Marketplace](https://github.com/marketplace?type=).
- Search open-source projects for existing workflows.
- Write your own GitHub Actions from scratch.

# Action Types

There are three types of GitHub actions:

- Container actions - Linux only
- JavaScript actions - Linux, Mac, or Windows
- Composite actions - combines multiple workflow steps into a single step

# Part of an Action

GitHub Actions are made up of workflows, jobs, and steps. Here is an example step:

```yaml
steps:
  - uses: actions/checkout@v2
  - name: Build code
    run: |
      make install
```

There are also other items that can be in a workflow file including:

- `name:` - The name of the workflow
- `description:` - Description of the workflow
- `author:` - Who or what team wrote the workflow
- `inputs:` - Get user input and set in a variable
- `runs:` - Runs a docker container
- `branding:` - Branding info for the Marketplace

To create a workflow you add a workflow yaml file to the `.github/workflows` folder in your GitHub repo. Here is a sample file mentioned in the GitHub certification:

```yaml
name: A workflow for my Hello World file
on: push
jobs:
  build:
    name: Hello world action
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - uses: ./action-a
      with:
        MY_NAME: "Mona"
```

Notes about the workflow:

- `on:` is the trigger, in this case when there is a push. This can be a string or an array.
- `jobs:` contains the list of 1 to many jobs. A job is a unit that is split across runners.
- `runs-on:` tells what environment the job will run on. In this case above it is the latest Ubuntu.
- `steps:` are the jobs steps. Above there are two steps
  - `actions/checkout@v1` checkout the current repository
  - `./action-a` the path to the container action.
- `MY_NAME` is the parameter variable to pass to the action step

# Runners

A runner is a server of where the runner service is installed. This could be:

- cloud runner - hosted by GitHub
- self-hosted runner

Self-hosted runners require the `self-hosted` tag in the `runs-on:` field. The `runs-on:` field can also accept an array like so:

```yaml
runs-on: [self-hosted, macos]
```

Depending on your GitHub license will determine if there are usage limits for cloud-based runners.