# Linux

# Linux Boot

- BIOS
- Master Boot Record
- Loader (grub)
- Kernel
- User Processes

# System Information

Linux Distro Info

```
cat /etc/*-release
cat /proc/version

lsb_release -a
```

Kernel Info

```
uname -a
```

Show CPU/Memory information

```
cat /proc/cpuinfo
lscpu

cat /proc/meminfo
```

Process Manager

```
top
```

# Find

```
# Find all files
find . -type f

# Find all folders
find . -type d

# Find all text files
find . -type f -name  "*.txt"

# Find all files to a certain folder depth (eg. 4)
find . -maxdepth 4 -type f
```