# Podman

[Podman](https://podman.io/docs) is an open source tool for managing container images. It has a similar syntax to docker. 


# Helpful Commands

Run a detached busybox image named `box` that sleeps for 1 hour (3600 seconds)

```sh
podman run -d --name box busybox sleep 3600
```

List the running containers:

```sh
$ podman ps
CONTAINER ID  IMAGE                             COMMAND         CREATED             STATUS                 PORTS       NAMES
9b25b1ac464e  docker.io/library/busybox:latest  sleep 3600      3 seconds ago       Up 3 seconds ago                   box
```

Run another sleep command in a previously started container namespace (the contianer:

```sh
podman run -d --name box2 --pid=container:box busybox sleep 7200
```

Execute into the running container and list the running processes

```sh
$ podman exec -it box ps -ef
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
    8 root      0:00 sleep 2400
   32 root      0:00 ps -ef
```

Execute into the running container with a shell

```sh
$ podman exec -it box /bin/sh
/ # ps -a
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
    8 root      0:00 sleep 2400
   20 root      0:00 /bin/sh
   23 root      0:00 ps -a
/ # exit
```

Kill the running containers

```sh
podman kill box box2
```

Remove the containers:

```sh
podman rm -f box
podman rm -f box2
```
