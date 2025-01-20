# Cilium

Cilium is a networking plugin for Kubernetes. It can be used outside of Kubernetes. It is built on top of eBPF. It was just promoted to CNCF in 2023

eBPF allows the kernel to be programmable by loading programs into the kernel.

- For Cilium it inserts itself into the networking stack.
- With eBPF you can short-circuit all of the virtual network traversal across the host and pod network.
- eBPF is also a good place to insert policy checks

# History

In the early days, Cilium had Network Security Groups (NSGs) at the Layer 3/4 layer of the OSI model. It could control traffic based on K8s identities. They didn't want to use IP addresses because they are transient.

There was Network Policies that were unique (CRD) to Cilium. So next came Layer 7 network policies that didnt act at the IP level, but at the application level.

Next up was Transparent Encryption, followed by mutual authentication.

# Pod-to-Pod Encryption using Cilium

Transparent Encryption has been in Cilium for a long time.

- Enabled per cluster
- IPSec or Wiregaurd
- No changes to app or configuration
- Works for all IP traffic (not just TCP)

Mutual Authentication is newer and directs people to think of mutual TLS (mTLS).

In the cloud native world, this is typically implemented by Sidecar patterns via service meshes. Downsides:

- Additional resource usage
- Extra hops and latency
- Sidecars add complexity
- Only works for TCP traffic (not UDP)

Cilium implements next-generation mutual authentication:

- Cilium agents implement TLS handshakes
- No need for a proxy sidecar
- Supports any IP protocol
- Two line change to the YAML (`authentication:`)

```yaml
  ingress:
  - fromEndpoints:
    - matchLabels:
       run: service
    authentication:
       mode: "required"
```

# Effortless Mutual Authentication

- Built on eBPF
- Configure with 2 additional lines in network policy
- SPIFFE (plugin based identity interface)
- No sidecars for cryptographic identity authentication
- Authentication is decoupled from encryption

# Reference

[Effortless Mutual Authentication with Cilium | Liz Rice - YouTube](https://www.youtube.com/watch?v=0t_lhV0fvQ8&t=16s)
