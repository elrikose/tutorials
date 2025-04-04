# Certified Kubernetes Security Specialist (CKS)

These pages contain all the notes I used for studying for the Certified Kubernetes Security Specialist (CKS) Exam:

- [CKS Portal](https://trainingportal.linuxfoundation.org/learn/dashboard/)
- [CKS Handbook](https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2)
- [killer.sh Simulator](./killer.md) - [killer.sh](https://killer.sh) simulator
- [Killer Coda](./killercoda.md) - [Killer Coda](https://killercoda.com/killer-shell-cks) CKS scenarios
- [CKS Questions](./questions.md) - Random Questions I have found online that have caused me problems

Helpful CKS Course on YouTube:

https://www.youtube.com/watch?v=d9xfB5qaOfg

# Security Best Practices

There are three broad categories of security

- Host Security (VM)
- Kubernetes Cluster Security
- Application Security

In a cloud provider they should provide Host and Cluster Security by default so you often only have to worry about application security.

## Host Security

Nodes should only run Kubernetes to reduce the attack surface. The Hosts should also have runtime security tools. SSH and IAM should be locked down.

## Kubernetes Cluster Security

All components should be secure and up to date
- API Server
- Kubelet
- ETCD - encrypted

Restrict external access

Admission Controllers using Open Policy Agent and NodeRestriction

Security benchmarking with Kubebench

## Application Security

- No Hardcoded credentials
- RBAC
- Sandbox containers
- Container Hardening
  - run as user
  - readonly file system
- mTLS / Service Meshes

## Topics

- [Attack Surface](./topics/attacksurface.md)
- [Auditing](./topics/auditing.md)
- [Authentication and Authorization](./topics/authentication.md)
- [Cilium for Authentication/Encryption](./topic/cilium.md)
- [Cilium Network Policies](./topic/ciliumnetworkpolicy.md)
- [Container Immutability](./topics/immutability.md)
- [Container Runtime Sandboxes](./topics/containerruntimes.md)
- [Image Hardening](./topics/imagehardening.md)
- [Image Vulnerabilities](./topics/imagevulnerabilities.md)
- [Ingress](./topics/ingress.md)
- [Mutual TLS (mTLS)](./topics/mtls.md)
- [Network Policies](./topics/networkpolicies.md)
- [Pod Security Standards](./topics/podsecuritystandards.md)
- [Role-based Access Control (RBAC)](./topics/rbac.md)
- [Secrets](./topics/secrets.md)
- [Security Contexts](./topics/securitycontexts.md)
- [Securing the Supply Chain](./topics/supplychain.md)
- [Service Accounts](./topics/serviceaccounts.md)
- [Upgrading Kubernetes](./topics/upgrade.md)
- [Verify Platform Binaries](./topics/verifybinaries.md)

## Tools

[Cheatsheet](./CHEATSHEET.md)

Kernel Tools
- [AppArmor](./topics/apparmor.md)
- [seccomp](./topics/seccomp.md)
- [strace](./topics/strace.md)

Admission Controllers
- [Open Policy Agent](./topics/opa.md) (OPA)

Runtime Scanning
- [KubeBench](./topics/kubebench.md)
- [Falco](./topics/falco.md)

Static Analysis
- [Conftest](./topics/conftest.md) - Part of OPA
- [Kubesec](./topics/kubesec.md)
- [Trivy](./topics/trivy.md)
