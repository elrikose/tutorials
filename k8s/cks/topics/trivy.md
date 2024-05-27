# Trivy

[Trivy](https://github.com/aquasecurity/trivy) is a scanner for vulnerabilities within an image container.

Examples

```sh
trivy image httpd:2.4.39-alpine > infra.txt

trivy image nginx:1.19.1-alpine-perl > app1.txt
trivy image nginx:1.20.2-alpine > app2.txt
```

Here is how you get all of the critical ones:

```sh
trivy image -s CRITICAL <container image name>
```

Only showing CRITICAL

```sh
$ trivy image -s CRITICAL nginx:1.20.2-alpine
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
