# Docker

[Docker](https://docs.docker.io) is a tool for managing container images.

# Helpful Commands

Run a detached busybox image named `box` that sleeps for 1 hour (3600 seconds)

```sh
docker run -d --name box busybox sleep 3600
```

List the running containers:

```sh
docker ps
CONTAINER ID   IMAGE     COMMAND        CREATED         STATUS         PORTS     NAMES
d21a6e66628c   busybox   "sleep 3600"   3 seconds ago   Up 3 seconds             box
```


Run another sleep command in a previously started container namespace (the contianer:

```sh
docker run -d --name box2 --pid=container:box busybox sleep 7200
```

Execute into the running container and list the running processes

```sh
$ docker exec -it box ps -ef
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
    7 root      0:00 sleep 2400
   32 root      0:00 ps -ef
```

Execute into the running container with a shell

```sh
$ docker exec -it box /bin/sh
/ # ps -a
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
    7 root      0:00 sleep 2400
   19 root      0:00 /bin/sh
   25 root      0:00 ps -a
/ # exit
```

Kill the running containers

```sh
docker kill box box2
```

Remove the containers:

```sh
docker rm -f box
docker rm -f box2
```
