# Networking

# Commands

Get a list of IP and Mac addresses

`nmap`:

```sh
$ sudo nmap -sn 192.168.86.*
Starting Nmap 7.80 ( https://nmap.org ) at 2022-12-17 15:15 EST
Nmap scan report for _gateway (192.168.1.1)
Host is up (0.00040s latency).
MAC Address: 88:3D:34:C3:1C:54 (Google)
Nmap scan report for 192.168.1.20
Host is up (0.31s latency).
MAC Address: 44:66:32:3F:27:FA (ecobee)
Nmap scan report for 192.168.1.22
Host is up (0.58s latency).
MAC Address: 24:7B:4D:7D:21:87 (Texas Instruments)
Nmap scan report for 192.168.1.24
Host is up (0.00051s latency).
MAC Address: 00:22:AB:56:C9:A8 (Seiko Epson)
...
```

`arp`:

```sh
 $ arp -a
? (192.168.1.1) at 88:3d:24:c3:c:54 on en0 ifscope [ethernet]
thermostat.lan (192.168.86.20) at 44:66:32:3f:27:fa on en0 ifscope [ethernet]
ring-732187.lan (192.168.1.22) at 24:7b:4d:7d:21:87 on en0 ifscope [ethernet]
? (192.168.86.23) at 8a:3c:de:f1:c7:48 on en0 ifscope [ethernet]
...
```

Get a list of open ports (Linux):

```sh
$ netstat -tuple
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name
tcp        0      0 localhost:32401         0.0.0.0:*               LISTEN      plex       28900      -
tcp        0      0 localhost:32600         0.0.0.0:*               LISTEN      plex       29120      -
tcp        0      0 0.0.0.0:6443            0.0.0.0:*               LISTEN      root       24009      -
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      root       26578      -
...
```

Get a list of open ports (macOS):

```sh
$ netstat -anvp tcp
Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)      rhiwat
tcp6       0      0  *.54415                *.*                    LISTEN       131072  ...
tcp4       0      0  *.54415                *.*                    LISTEN       131072  ...
tcp6       0      0  *.5000                 *.*                    LISTEN       131072  ...
tcp4       0      0  *.5000                 *.*                    LISTEN       131072  ...
tcp6       0      0  *.7000                 *.*                    LISTEN       131072  ...
tcp4       0      0  *.7000                 *.*                    LISTEN       131072  ...
...
```
