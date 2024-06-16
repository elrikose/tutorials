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

## Running a container in separate namespaces

Launch two different containers and they get a separate namespace

```sh
podman run --name c1 -d ubuntu sh -c 'sleep 1d'
podman run --name c2 -d ubuntu sh -c 'sleep 999d'
```

Exec'ing into `c1`:

```sh
$ podman exec c1 ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2792  1064 ?        Ss   19:26   0:00 sh -c sleep 1d
root           2  0.0  0.0   2688  1080 ?        S    19:26   0:00 sleep 1d
root           7  0.0  0.1   7880  3948 ?        R    19:34   0:00 ps aux
```

Exec'ing into `c2`:

```sh
$ podman exec c2 ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2792  1124 ?        Ss   19:33   0:00 sh -c sleep 999d
root           2  0.0  0.0   2688  1048 ?        S    19:33   0:00 sleep 999d
root           3  0.0  0.1   7880  3956 ?        R    19:33   0:00 ps aux
```



## Running a container in same namespace

Launch two different containers in the same namespace

```sh
podman run --name c1 -d ubuntu sh -c 'sleep 1d'
podman run --name c2 --pid=container:c1 -d ubuntu sh -c 'sleep 999d'
```

Exec'into either container will show both sleep processes

```sh
$ podman exec c2 ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2792  1064 ?        Ss   19:26   0:00 sh -c sleep 1d
root           2  0.0  0.0   2688  1080 ?        S    19:26   0:00 sleep 1d
root           4  0.0  0.0   2792  1060 ?        Ss   19:28   0:00 sh -c sleep 999d
root           5  0.0  0.0   2688  1100 ?        S    19:28   0:00 sleep 999d
root           6  0.0  0.1   7880  3964 ?        R    19:29   0:00 ps aux
```
