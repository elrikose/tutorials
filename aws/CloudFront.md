# CloudFront

CloudFront is a Content Delivery Network (CDN). 
- It is global, not region based.
- Improves getting files at the edge
- 400 points of presence around world
- DDoS protection
- AWS WAF
- Exposes external HTTPS to internal backends

CloudFront to a EC2 instance requires an ALB front end. CloudFront to an S3 bucket is an easy way to serve content without an EC2 instance.

Data is cached locally from another region

You access S3 buckets via a Origin Access Identity (OAI).

# CloudFront versus S3 Cross Region Replication

CloudFront
- Global Edge network
- There is a caching TTL
- Great for static content available everywhere

S3 Cross Region Replication
- Must be configured for all regions
- Files are updated in real-time
- Read only
- Dynamic content and low-latency in a few regions due to the management cost.


# Origins

S3 Buckets
- Enhanced security with CloudFront Origin Access Identity (OAI)
- Can be used as ingress to upload files as well.

Custom HTTP
- ALB
- EC2 Instance
- S3 Website (enabled in S3 config)

The OAI + S3 Bucket policy is what is used so that it can access the bucket over the private AWS network.

ALB or EC2 Origins
- Security gourp must allow all public IPs of edge locations
- ALBS must be public, EC2 can be private

# GEO Restrictions

Restrict distribution
- Whitelisting countries
- Blacklist countries

Uses a 3rd party Geo-IP Database

# Caching

With CloudFront you can cache based on:
- Headers
- Cookies
- Query String Params

The cache lives on each Edge location and is retrieved from the origin.

Minimize requests to Origin by maximizing cach hits. Control with the TTL. You can invalidate part of the cache with the CreateInvalidation API. 

Maximize cache hit by separating static content (images, files) with dynamic content (REST APIs at Endpoints like EC2 instances).

# Security

Security
- GEO Restrictions like above
- HTTPS

## HTTPS 

Viewer Protocol Policy
- Between User and Edge Location
- HTTP -> HTTPS
- Prevent HTTP

Origin Protocol Policy
- Between Backend and Edge location
- HTTPS Only
- Match what the user is doing 

S3 websites don't support HTTPS

# Signed URL / Signed Cookie

Use case: Distribute paid shared content all around the world

Signed URL - Access to individual files
Signed Cookie - Access to multiple files

Attach a policy
- Give the URL an expiration
- Whitelist IP ranges to access the data
- Trusted signers

Flow:
- Client access application and authenticates
- Use AWS SDK to generate signed URL that you pass to the client
- Client then can use signed URL to go to an edge location.
- Edge location uses OAI to get info from S3 bucket.

Unlike S3 Pre-signed URLs, Signed URLs:
- Allow access to an S3 path no matter the origin
- Filtering by Path, date, expiration, IP
- Caching
- There is an account wide key/pair that only the root user can manage.

Versus S3 Pre-signed:
- You issue the request as the person who pre-signed the URL
- Uses an IAM key of the signing principal
- Limited lifetime

## Signed URL Process

Two types of signers
- Recommended: Trusted Key Group - APIs to create and rotate keys
- Not-recommended: CloudFront Key Pair - root account to manage keys

Then you create the key groups for your CloudFront distribution. Requires private/private key. Private is for your app. Public is for CloudFront URLs.

# Pricing

Edge locations have different prices. India is twice as expensive as North America.

Three price classes
- All - all regions but costlier
- 200 - Most regions but excludes most expensive
- 100 - Only the least expensive regions

# Multiple Origins

Route to different origins based on content type

- /api/* -> send to an ALB
- /movies/* -> send to 1 S3 bucket
- /* - Send to a different S3 bucket

You can specify a primary and secondary origin for HA. Both ALBs or S3 buckets work for this. Good idea to put data in different regions.

# Field Level Encryption

Sensitive info is encrypted at the edge closer to user.

You use Asymmetric Key encryption to select 10 fields in a POST and encrypt them with your keys before they are passed on to the backend which has custom logic to decrypt it.


