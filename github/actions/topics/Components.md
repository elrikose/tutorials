# GitHub Actions Components

There are 4 main components of GitHub Actions (from outside to inside)

- Workflow
- Job
- Step
- Action

A **Workflow** is encapsulated in yaml files in the `.github/workflows` folder in a GitHub repo. A workflow has to have at least one job.

A **Job** is a section of the workflow that links to a runner. Multiple jobs can be defined in a workflow. A `runs-on:` field defines the runner type.

A **Step** is a task that can run an action.

An **Action** are the command that are executed. They can either be referenced externally like the checkout command (`uses: actions/checkout@v3`) or a list of command `run: make install`.

