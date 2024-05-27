# Logging

All build have logs. To access them

- Navigate to the **Actions** tab in your repository.
- In the left sidebar, click the desired workflow.
- From the list of workflow runs, select the desired run.
- Under Jobs, select the desired job.
- Read the log output.

# Verbose Logging

Sometimes the build workflow logs are not enough. It you set certain secrets in a repo, the logging will be more verbose:

- `ACTIONS_RUNNER_DEBUG=true` - Runner loging will be enabled
- `ACTIONS_STEP_DEBUG=true` - Step loging will be enabled
