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

# Routing Policies

- Simple - You can specify multiple IP addresses and it is up to the client to decide which IP.
- Weighted - Control a percentage of the requests.
- Failover
- Latency Based
- Geolocation
- Multi-Value Answer
- Geoproximity

Weighted
- Load balancing use cases
- 70/20/10 for example. They don't have to add to 100
- Set a record to 0 if you want to stop sending requests.
- Set all records to 0 if you want them to be returned equally.
- Health check-able unlike simple

Latency
- Redirect to the resource closest based on latency
- German user may be redirected to US if that's the lowest latency
- Health check-able unlike simple
- You specify the region

Failover
- If a health check fails, fail over to a secondary instance
- Only 1 primary and 1 secondary configured.

Geolocation
- If a user comes from a COntinent, Country, or US State
- Create a default user
- Use cases: localization 
- Can be used with health checks

Geoproximity
- You bias a resource so that more traffic in a geo goes to 1 over another.
- Biases of 0 on 2 resources will be equal bias.
- Done to shift more in case there are stronger resources.

Multi-Value
- Routing traffic to multiple resources
- Different from simple because you can assign health checks.
- Up to 8 values are returnable
- Not a substitute for an ELB.

# Route 53 - Traffic Flow

Simplify the process of creating and maintaining records in large and complex configurations using a visual editor to create traffic policies.

The visual editors are great for geoproximity maps. It is costly at $50/month

# Health Checks

HTTP checks for public resources. 15 global health checkers will check the endpoint health.
- Healthy/Unhealthy threshold count 3
- Interval 30 seconds (10 seconds is higher cost)
- HTTP/HTTPS/TCP

You need to let the Route 54 health checkers access your infrastructure in a security group

IP Ranges of AWS services: 
https://ip-ranges.amazonaws.com/ip-ranges.json

```
    {
      "ip_prefix": "15.177.0.0/18",
      "region": "GLOBAL",
      "service": "ROUTE53_HEALTHCHECKS",
      "network_border_group": "GLOBAL"
    },
```
