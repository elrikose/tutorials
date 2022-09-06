# Route 53 - Amazon DNS

## DNS Terminology

Domain Registrar: Amazon Route 53, GoDaddy
DNS Records: A, AAAA, CNAME, NS
Zone File: Contains records
Name Server: Resolves DNS queries
Top Level Domain (TLD): .com, .us, .gov
Second Level Domain (SLD): amazon.com, google.com
Fully Qualified Domain Name (FQDN): www.google.com

Root DNS Server is managed by ICANN
TLD DNS Server (.com, .net, etc) is managed by IANA
SLD is managed by Amazon

DNS entries are cached with a Time To Live (TTL) on both the local DNS server and Web browsers

# Route 53

A highly available, scalable, fully managed, DNS. 

- It is authoritative which means the customer can update DNS entries.
- The only AWS service that provides 100% availability SLA
- The 53 in the name comes from the traditional DNS port

# Route 53 Records

Each Record contains:

- Domain or subdomain name
- Record Type: A, AAAA, CNAME
- Value: IP address
- Routing Policy: How Route 53 reponds
- TTL: Amount of time the record is cached at DNS resolvers

# Route 53 Record Types

- A maps a hostname to IPv4
- AAAA maps a hostname to IPv6
- CNAME - maps a hostname to another hostname
- NS - Name servers for the zone

# Hosted Zones

A container for records that define how to route traffic to a domain/subdomain

Public Hosted Zones - records for the Internet
Private Hosted Zones - records for traffic within 1 or more VPCs

# TTL

High TTL (eg 24 hrs)
- Less traffic on Route 53
- Outdated records if you change them

Low TTL
- More traffic on Route 53
- Records are outdated for less times

TTL is mandatory except for Alias records

`dig` actually reports the TTL for A records

# CNAME vs Alias

CNAME is a DNS thing. Aliases are are unique to Route 53 and allow you to point it to an AWS resource.

CNAMEs only work for non-SLDs like api.example.com.

Aliases:
- work for SLDs (example.com) and non-SLDs (api.example.com).
- Aliases are free
- Automatically recognize IP changes

Alias Targets include
- Elastic Load Balancers (ELBs)
- CloudFront Distributions
- API Gateway
- Elastic
- S3 Websites
- VPC Interface Endpoints
- Route 53 record in the same hosted zone
- NOT: EC2 DNS names