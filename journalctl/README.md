# journalctl

`journalctl` is a utility for showing logs from journald, systemd’s logging service. journald has logs from the kernel as well as services installed under `/etc/systemd`.

## Showing logs

Show all log messages since last boot:

```sh
journalctl -b
```

Show all log messages during previous boot:

```
journalctl -b -1
```

Use `--since` and/or `--until` with a natural language format:

```
journalctl --since "22:00:00"
journalctl --since "20 minutes ago"
journalctl --since "10 minutes ago" --until "5 minutes ago"
```

Show logs from a specific service

```
journalctl -u kubelet.service
```

Show logs from a specific service with extra data

```
journalctl -x -u kubelet.service
```

Follow the logs

```
journalctl -u kubelet.service -f
```

Filter logs by a priority. If you specify a priority it is that priority and any priority less than that. Priorities:
- 0 or "emerg"
- 1 or "alert"
- 2 or "crit"
- 3 or "err"
- 4 or "warning"
- 5 or "notice"
- 6 or "info"
- 7 or "debug"

These three command are all the same thing:

```
journalctl -p emerg..err
journalctl -p err 
journalctl -p 3
```

For showing logs by user you must pass the uid:

```
$ id plex
uid=998(plex) gid=998(plex) groups=998(plex),44(video),109(render)
```

```
journalctl _UID=998
```

Show logs as **json**:

```
journalctl -o json
journalctl -o json-pretty
```

## List previous boots

To show the journal of all boots

```sh
journalctl --list-boots
```

An example:

```sh
$ journalctl --list-boots
-53 fcac3447dd00432c8b35f9fb71dfc3ac Fri 2022-08-19 20:56:06 EDT—Fri 2022-08-19 21:51:52 EDT
...
 -2 caef9716a0f04ee48518e94981e13f0b Sat 2022-12-03 16:06:32 EST—Sun 2022-12-04 02:23:33 EST
 -1 4a2d2ede84f04b93a182f5b46347ef4a Sun 2022-12-04 16:22:24 EST—Sun 2022-12-04 23:20:05 EST
  0 5be9a988f7a04009923dc1995db21bbd Thu 2022-12-08 21:17:03 EST—Thu 2022-12-08 21:17:38 EST
```

# Journal Disk Usage

```sh
$ journalctl --disk-usage
Archived and active journals take up 4.0G in the file system.
```