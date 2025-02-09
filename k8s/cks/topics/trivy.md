# Trivy

[Trivy](https://github.com/aquasecurity/trivy) is a scanner for vulnerabilities within an image container.

Examples

Through docker it is easy:

```sh
docker run ghcr.io/aquasecurity/trivy:latest image nginx:latest
```

And then it dumps out a log

```
nginx:latest (debian 12.5)
==========================
Total: 173 (UNKNOWN: 2, LOW: 88, MEDIUM: 59, HIGH: 22, CRITICAL: 2)

┌────────────────────┬─────────────────────┬──────────┬──────────────┬─────────────────────────┬───────────────────┬──────────────────────────────────────────────────────────────┐
│      Library       │    Vulnerability    │ Severity │    Status    │    Installed Version    │   Fixed Version   │                            Title                             │
├────────────────────┼─────────────────────┼──────────┼──────────────┼─────────────────────────┼───────────────────┼──────────────────────────────────────────────────────────────┤
│ apt                │ CVE-2011-3374       │ LOW      │ affected     │ 2.6.1                   │                   │ It was found that apt-key in apt, all versions, do not       │
│                    │                     │          │              │                         │                   │ correctly...                                                 │
│                    │                     │          │              │                         │                   │ https://avd.aquasec.com/nvd/cve-2011-3374                    │
├────────────────────┼─────────────────────┤          │              ├─────────────────────────┼───────────────────┼──────────────────────────────────────────────────────────────┤
│ bash               │ TEMP-0841856-B18BAF │          │              │ 5.2.15-2+b2             │                   │ [Privilege escalation possible to other user than root]      │
│                    │                     │          │              │                         │                   │ https://security-tracker.debian.org/tracker/TEMP-0841856-B1- │
│                    │                     │          │              │                         │                   │ 8BAF                                                         │
├────────────────────┼─────────────────────┤          │              ├─────────────────────────┼───────────────────┼──────────────────────────────────────────────────────────────┤
│ bsdutils           │ CVE-2022-0563       │          │              │ 1:2.38.1-5+deb12u1      │                   │ util-linux: partial disclosure of arbitrary files in chfn    │
│                    │                     │          │              │                         │                   │ and chsh when compiled...                                    │
│                    │                     │          │              │                         │                   │ https://avd.aquasec.com/nvd/cve-2022-0563                    │
├────────────────────┼─────────────────────┤          ├──────────────┼─────────────────────────┼───────────────────┼──────────────────────────────────────────────────────────────
...
```

```sh
docker run ghcr.io/aquasecurity/trivy image httpd:2.4.39-alpine > infra.txt

docker run ghcr.io/aquasecurity/trivy image nginx:1.19.1-alpine-perl > app1.txt
docker run ghcr.io/aquasecurity/trivy image nginx:1.20.2-alpine > app2.txt
```

Here is how you get all of the critical ones:

```sh
docker run ghcr.io/aquasecurity/trivy image -s CRITICAL <container image name>
```

Only showing CRITICAL

```sh
$ docker run ghcr.io/aquasecurity/trivy image -s CRITICAL nginx:1.20.2-alpine
2024-05-07T03:02:40.389Z        INFO    Detected OS: alpine
2024-05-07T03:02:40.390Z        INFO    Detecting Alpine vulnerabilities...
2024-05-07T03:02:40.400Z        INFO    Number of language-specific files: 0
2024-05-07T03:02:40.400Z        WARN    This OS version is no longer supported by the distribution: alpine 3.14.6
2024-05-07T03:02:40.401Z        WARN    The vulnerability detection may be insufficient because security updates are not provided

nginx:1.20.2-alpine (alpine 3.14.6)
===================================
Total: 3 (CRITICAL: 3)

+---------+------------------+----------+-------------------+---------------+---------------------------------------+
| LIBRARY | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |                 TITLE                 |
+---------+------------------+----------+-------------------+---------------+---------------------------------------+
| curl    | CVE-2022-32207   | CRITICAL | 7.79.1-r1         | 7.79.1-r2     | curl: Unpreserved file permissions    |
|         |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2022-32207 |
+---------+                  +          +                   +               +                                       +
| libcurl |                  |          |                   |               |                                       |
|         |                  |          |                   |               |                                       |
+---------+------------------+          +-------------------+---------------+---------------------------------------+
| zlib    | CVE-2022-37434   |          | 1.2.12-r0         | 1.2.12-r2     | zlib: heap-based buffer               |
|         |                  |          |                   |               | over-read and overflow in             |
|         |                  |          |                   |               | inflate() in inflate.c via a...       |
|         |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2022-37434 |
+---------+------------------+----------+-------------------+---------------+---------------------------------------+
```

And if you are looking for 2 specific CVEs, here is a good way to search with `grep -e`:

```sh
$ docker run ghcr.io/aquasecurity/trivy image -s CRITICAL nginx:1.20.2-alpine | grep -e CVE-2023-23914 -e CVE-2022-37434
2025-02-09T19:38:31Z	INFO	[vulndb] Need to update DB
2025-02-09T19:38:31Z	INFO	[vulndb] Downloading vulnerability DB...
...
│         │ CVE-2023-23914 │          │        │                   │ 7.79.1-r5     │ curl: HSTS ignored on multiple requests               │
│         │ CVE-2023-23914 │          │        │                   │ 7.79.1-r5     │ curl: HSTS ignored on multiple requests               │
│ zlib    │ CVE-2022-37434 │          │        │ 1.2.12-r0         │ 1.2.12-r2     │ zlib: heap-based buffer over-read and overflow in inf │
```
