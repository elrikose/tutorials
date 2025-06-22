# Kube Bench (kube-bench)

# CIS

CIS - Center of Intenet Security

CIS Benchmarks are default Kubernetes security rules that all cloud providers use. There are PDFs that define all of the benchmarks by name.

# kube-bench

kube-bench is a tool that can analyze control plane and workers for CIS Benchmarks

https://github.com/aquasecurity/kube-bench

Run it with Docker:

```sh
$ docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t docker.io/aquasec/kube-bench:latest run --version 1.32
```

Options

```sh
-c 1.2.20 = Run the benchmark version 1.2.20 only
--targets [master|node|controlplane|etcd|policies] = Target a specific part of the cluster
```

# Sample Reports

Here are all the benchmark section versions

1.1 Control Plane Node Security
1.2 Control Plane API Security
1.3 Control Plane Controller Manager Security
1.4 Control Plane Scheduler Security
2 Etcd
3.1 Control Plane Authentication and Authorization
3.2 Control Plane Logging
4.1 Worker Node Config Files
4.2 Kubelet
4.3 kube-proxy


Here is where you just check benchmark 1.2.20 for Kubernetes version 1.32

```sh
$ docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t docker.io/aquasec/kube-bench:latest run --targets master -c 1.2.20 --version 1.32
[INFO] 1 Control Plane Security Configuration
[INFO] 1.2 API Server
[WARN] 1.2.20 Ensure that the --request-timeout argument is set as appropriate (Manual)

== Remediations master ==
1.2.20 Edit the API server pod specification file /etc/kubernetes/manifests/kube-apiserver.yaml
and set the below parameter as appropriate and if needed.
For example, --request-timeout=300s


== Summary master ==
0 checks PASS
0 checks FAIL
1 checks WARN
0 checks INFO

== Summary total ==
0 checks PASS
0 checks FAIL
1 checks WARN
0 checks INFO
```

```sh
$ kube-bench run -c 1.1.19
[INFO] 1 Master Node Security Configuration
[INFO] 1.1 Master Node Configuration Files
[PASS] 1.1.19 Ensure that the Kubernetes PKI directory and file ownership is set to root:root (Automated)

== Summary master ==
1 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO

[INFO] 2 Etcd Node Configuration

== Summary etcd ==
0 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO

[INFO] 3 Control Plane Configuration

== Summary controlplane ==
0 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO

[INFO] 4 Worker Node Security Configuration

== Summary node ==
0 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO

[INFO] 5 Kubernetes Policies

== Summary policies ==
0 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO

== Summary total ==
1 checks PASS
0 checks FAIL
0 checks WARN
0 checks INFO
```
