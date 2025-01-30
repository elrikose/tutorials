# Image Vulnerabilities

With Image Layering, there could be vulnerabilities from

- Base images (ubuntu:14)
- App install in container (nginx:1.x)
- Tool install (curl:x.x)

There are two major Databases of Image Vulnerabilites:

- https://cve.mitre.org
- https://nvd.nist.gov

Vulnerabilities can be discovered in images and dependencies using scanning tools.

- Build scanning
- Runtime scanning

In runtime scanning you could add hooks in 2 places:

- Mutating Webhook
- Validation Webhook

Two open source tools:

- Clair
  - Open source
  - Static analysis of vulnerabilities in application containers
  - Ingests vulnerability metadata from a set of sources
  - API
- [Trivy](./trivy.md)
  - Open source
  - Simple, easy, and fast.
