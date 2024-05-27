# GitHub Action Triggers

https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows

>Workflow triggers are events that cause a workflow to run.
>
>Some events have multiple activity types. For these events, you can specify which activity types will trigger a workflow run.

## Workflow Triggers

There are 4 different ways a workflow can be triggered:

- Events caused by activity in your repo (`push`, `pull_request`)
- Events outside of your repo (`repository_dispatch`)
- Scheduled (cron-like)
- Manually (`workflow_dispatch`)

GitHub is specifically looking for workflows in the `.github/workflows` folder. The `on:` map defines the events that will trigger the workflow. Some events must be on the default branch. All events contain a commit SHA (`GITHUB_SHA`) or git ref (`GITHUB_REF`) to associate with the workflow run.

A workflow can only be triggered from a GitHub application or personal access token (PAT). The `GITHUB_TOKEN` can't be used because of the possibility of creating a recursive workflow run. Those tokens would need to be stored as secrets.

## Repo Events

Here are a list of the most common repo events along with activity types that are unique to that even that will cause an action to be triggered:

- `push` - commit(s) are pushed to a branch

- `pull_request` - when a pull_request action occurs
  - `opened` - PR is opened
  - `closed` - PR is closed

- `fork` - when someone forks a repo

- `release` - when a release action occurs
  - `created` - a release is created
  - `published` - a draft release is published
  - `released` - a release is released

- `issues` - when an issue action occurs
  - `opened` - issue is opened
  - `closed` - issue is closed
  - `assigned` - issue is assigned

- `repository_dispatch` - when a webhook event occurs outside of GitHub.

- `workflow_dispatch` - used for only manually triggering a workflow (on the default branch)