# grep

Find and include 1 line after:

```shell
$ grep -A 1 "^root" /etc/passwd 
root:*:0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1:System Services:/var/root:/usr/bin/false
```

Find and include 1 line before:

```shell
$ grep -B 1 "^root" /etc/passwd
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
```

Find and include 1 lines before and after:

```shell
$ grep -C 1 "^root" /etc/passwd
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1:System Services:/var/root:/usr/bin/false
```

# ripgrep (rg)

Ripgrep is a fast grep tool that does a better job of outputing text for multiple files. It also shows the line number 

Install:

```
brew install ripgrep
```

One file:

```
$ rg "^root" /etc/passwd 
12:root:*:0:0:System Administrator:/var/root:/bin/sh
```

Multiple files:

```
$ rg "root" /etc/passwd /etc/group 
/etc/group
13:wheel:*:0:root
14:daemon:*:1:root
15:kmem:*:2:root
16:sys:*:3:root
17:tty:*:4:root
18:operator:*:5:root
...

/etc/passwd
12:root:*:0:0:System Administrator:/var/root:/bin/sh
13:daemon:*:1:1:System Services:/var/root:/usr/bin/false
```