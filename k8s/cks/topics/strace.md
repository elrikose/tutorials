# strace for system calls

`strace` is a tool to see what kind of system calls a process can make. Usually pre-installed

Using `strace` with the ls call

```sh
$ strace ls
execve("/usr/bin/ls", ["ls"], 0x7fff958c2210 /* 107 vars */) = 0
brk(NULL)                               = 0x5b3bc4628000
arch_prctl(0x3001 /* ARCH_??? */, 0x7ffffdaf42a0) = -1 EINVAL (Invalid argument)
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x70aa08a73000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=80083, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 80083, PROT_READ, MAP_PRIVATE, 3, 0) = 0x70aa08a5f000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libselinux.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=166280, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 177672, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x70aa08a33000
mprotect(0x70aa08a39000, 139264, PROT_NONE) = 0
mmap(0x70aa08a39000, 106496, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x6000) = 0x70aa08a39000
mprotect(0x70aa08aad000, 8192, PROT_READ) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
munmap(0x70aa08a5f000, 80083)           = 0
statfs("/sys/fs/selinux", 0x7ffffdaf42e0) = -1 ENOENT (No such file or directory)
statfs("/selinux", 0x7ffffdaf42e0)      = -1 ENOENT (No such file or directory)
getrandom("\x3f\x2c\xa7\x86\x83\xc1\x44\x9b", 8, GRND_NONBLOCK) = 8
brk(NULL)                               = 0x5b3bc4628000
brk(0x5b3bc4649000)                     = 0x5b3bc4649000
openat(AT_FDCWD, "/proc/filesystems", O_RDONLY|O_CLOEXEC) = 3
newfstatat(3, "", {st_mode=S_IFREG|0444, st_size=0, ...}, AT_EMPTY_PATH) = 0
read(3, "nodev\tsysfs\nnodev\ttmpfs\nnodev\tbd"..., 1024) = 407
close(3)                                = 0
access("/etc/selinux/config", F_OK)     = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=5712208, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 5712208, PROT_READ, MAP_PRIVATE, 3, 0) = 0x70aa08000000
close(3)                                = 0
ioctl(1, TCGETS, {B38400 opost isig icanon echo ...}) = 0
ioctl(1, TIOCGWINSZ, {ws_row=30, ws_col=194, ws_xpixel=0, ws_ypixel=0}) = 0
openat(AT_FDCWD, ".", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
newfstatat(3, "", {st_mode=S_IFDIR|0775, st_size=4096, ...}, AT_EMPTY_PATH) = 0
getdents64(3, 0x5b3bc462e9f0 /* 21 entries */, 32768) = 720
getdents64(3, 0x5b3bc462e9f0 /* 0 entries */, 32768) = 0
close(3)                                = 0
newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x4), ...}, AT_EMPTY_PATH) = 0
write(1, "apparmor.md\t   conftest.md\t\t fal"..., 152apparmor.md          conftest.md           falco.md           imagevulnerabilities.md  kubesec.md  networkpolicies.md  samples     secrets.md             supplychain.md  upgrade.md
) = 152
write(1, "authentication.md  containerrunt"..., 141authentication.md  containerruntimes.md  imagehardening.md  ingress.md                    mtls.md     opa.md              seccomp.md  securitycontexts.md  trivy.md
) = 141
close(1)                                = 0
close(2)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

And you can see a more summarized view with `-cw`:

```sh
$ strace -cw ls 
apparmor.md        conftest.md           falco.md           imagevulnerabilities.md  kubesec.md  networkpolicies.md  samples     secrets.md           supplychain.md  upgrade.md
authentication.md  containerruntimes.md  imagehardening.md  ingress.md               mtls.md     opa.md              seccomp.md  securitycontexts.md  trivy.md
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 21.67    0.000394          21        18           mmap
 16.08    0.000292         291         1           execve
  8.55    0.000155          19         8           newfstatat
  8.44    0.000153          21         7           mprotect
  8.03    0.000146          29         5           read
  7.11    0.000129          14         9           close
  7.01    0.000127          18         7           openat
  3.58    0.000065          32         2         2 statfs
  2.82    0.000051          12         4           pread64
  2.41    0.000044          14         3           brk
  2.18    0.000040          19         2           getdents64
  2.06    0.000037          37         1           munmap
  1.97    0.000036          17         2           write
  1.78    0.000032          16         2         2 access
  1.62    0.000029          14         2           ioctl
  1.57    0.000029          14         2         1 arch_prctl
  0.73    0.000013          13         1           getrandom
  0.63    0.000011          11         1           rseq
  0.61    0.000011          11         1           prlimit64
  0.59    0.000011          10         1           set_tid_address
  0.57    0.000010          10         1           set_robust_list
------ ----------- ----------- --------- --------- ----------------
100.00    0.001816          22        80         5 total
```

# proc folder

The `/proc` folder:

- Information and connections to processes and kernel
- Learn how processes work
- Configuration and admin taks
- Files that don't exist, but you can access them. 
- Interface from the users

Activity:
- List syscalls
- Find open files
- Read secret values

Go to your control plane node. Get the pid of your etcd via `ps -ef` and then pass to the command. `-f` follows.

```sh
sudo strace -p 1608 -f
```

To get the count of system calls use

```sh
sudo strace -p 1608 -f -cw
```

Press Ctrl-C and then you have the list of calls

```
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 77.38   67.512027       13424      5029      1021 futex
 19.74   17.219306        2828      6087           epoll_pwait
  2.39    2.085326         385      5404           nanosleep
  0.20    0.174402         146      1189           write
  0.17    0.145218        1792        81           fdatasync
  0.08    0.072082          62      1148       480 read
  0.01    0.008141         110        74           tgkill
  0.01    0.007163          55       129           pwrite64
  0.01    0.006669        6669         1         1 restart_syscall
  0.01    0.005715          77        74           getpid
  0.01    0.004771          64        74         1 rt_sigreturn
  0.00    0.003590          81        44           sched_yield
  0.00    0.001542          53        29           lseek
  0.00    0.000767          54        14           setsockopt
  0.00    0.000719         143         5           close
  0.00    0.000617          51        12           fcntl
  0.00    0.000479          68         7         3 epoll_ctl
  0.00    0.000320          80         4         2 accept4
  0.00    0.000257          85         3           openat
  0.00    0.000247          41         6           getdents64
  0.00    0.000078          39         2           getsockname
------ ----------- ----------- --------- --------- ----------------
100.00   87.249439                 19416      1508 total
```

Using the `/proc` folder you can then look at the list of open files:

```sh
$ cd /proc/1608
$ # ls
arch_status  cgroup      coredump_filter  exe      io         maps       mountstats  oom_adj        patch_state  sched      smaps         statm    timers
attr         clear_refs  cpuset           fd       limits     mem        net         oom_score      personality  schedstat  smaps_rollup  status   timerslack_ns
autogroup    cmdline     cwd              fdinfo   loginuid   mountinfo  ns          oom_score_adj  projid_map   sessionid  stack         syscall  uid_map
auxv         comm        environ          gid_map  map_files  mounts     numa_maps   pagemap        root         setgroups  stat          task     wchan
```

The `exe` file is a link and points to the executable:

```sh
$ ls -ald exe
lrwxrwxrwx 1 root root 0 Jun 29 17:00 exe -> /usr/local/bin/etcd
```

The list of files are in the `fd` folder:

```sh
ls -l
total 0
lrwx------ 1 root root 64 Jun 29 16:01 0 -> /dev/null
l-wx------ 1 root root 64 Jun 29 16:01 1 -> 'pipe:[27348]'
lrwx------ 1 root root 64 Jun 29 16:01 10 -> /var/lib/etcd/member/snap/db
lrwx------ 1 root root 64 Jun 29 16:01 100 -> 'socket:[420163]'
lrwx------ 1 root root 64 Jun 29 16:01 101 -> 'socket:[419648]'
lrwx------ 1 root root 64 Jun 29 16:01 11 -> 'socket:[417756]'
lr-x------ 1 root root 64 Jun 29 16:01 12 -> /var/lib/etcd/member/wal
l-wx------ 1 root root 64 Jun 29 16:01 13 -> /var/lib/etcd/member/wal/0000000000000012-00000000001ac9fa.wal
lrwx------ 1 root root 64 Jun 29 16:01 14 -> 'socket:[28233]'
l-wx------ 1 root root 64 Jun 29 16:01 15 -> /var/lib/etcd/member/wal/1.tmp
...
```

File `10` has a database and dumping through the DB can find all sorts of goodies like secrets.

There is also a file named `environ` that lists all of the environment variables for secret information:

```sh
$ cd /proc/1608
$ cat environ
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binHOSTNAME=masterSSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crtHOME=/root
```

Another handy tool to look at the whole process tree with pids is `pstree -p`