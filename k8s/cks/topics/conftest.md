# Conftest

Conftest is part of the Open Policy Agent. Test framework for Kubernetes configurations that uses Rego.

The following `deployment.rego` file does two things:

- forces deployments to run as non root
- forces deployments to have an `app` label

## Kubernetes Analysis

```js
package main

deny[msg] {
  input.kind = "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot = true
  msg = "Containers must not run as root"  
}

deny[msg] {
  input.kind = "Deployment"
  not input.spec.selector.matchLabels.app
  msg = "Containers must provide app label for pod selectors"
}
```

You have to run the static analyzer in Docker

```sh
docker run --rm -v $(pwd):/project openpolicyagent/conftest test deploy.yaml
```

And it a deployment doesn't have a securityContext, it will throw this error

```sh
Unable to find image 'openpolicyagent/conftest:latest' locally
latest: Pulling from openpolicyagent/conftest
....
FAIL - deploy.yaml - main - Containers must not run as root
```

And if it didn't have the label in the manifest:

```sh
$ docker run --rm -v $(pwd):/project openpolicyagent/conftest test deploy.yaml
FAIL - deploy.yaml - main - Containers must provide app label for pod selectors
```

## Dockerfile Analysis

You can also pass in Dockerfiles and force it to deny ubuntu base images like "ubuntu". Create a `base.rego`

```js
package main

denylist = [
  "ubuntu"
]

deny[msg] {
  input[i].Cmd == "from"
  val := input[i].Value
  contains(val[i], denylist[_])

  msg = sprintf("unallowed image found %s", [val])
}
```

You can also realize if a Dockerfile `RUN` command from calling package managers:

```js
package commands

denylist = [
  "apk",
  "apt",
  "pip",
  "curl",
  "wget",
]

deny[msg] {
  input[i].Cmd == "run"
  val := input[i].Value
  contains(val[_], denylist[_])

  msg = sprintf("unallowed commands found %s", [val])
}
```

And then you run it in the same way.

```sh
docker run --rm -v $(pwd):/project openpolicyagent/conftest test Dockerfile --all-namespaces
```

