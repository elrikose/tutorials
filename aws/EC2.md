# Elastic Compute Cloud (EC2)

## EC2 Instance Store

If you need a high-performance hardware disk, use EC2 Instance Store.

- Ephemeral / Not durable - Buffer or cache
- Better I/O performance
- Risk of data loss if hardware fails
- Backups/Replication is your responsibility

## EBS Volume Types

- gp2 / gp3 (SSD): General Purpose
- io1 / io2: High performance SSD volume
- stl:  Low cost HDD
- scl: Lowest cost

### gp2/gp3

- Cost effective, low-latency
- Boot Volumes, Dev/Test environments
- 1 GiB - 16 TiB

gp3 is the new generation
- Baseline of 3,000 IOPS, throughput of 125 MiB/s
- Can increase to 16,000 IOPS and 1000 MiB/s

gp2 
- Small volumes burst up to 3000 IOPS
- The larger the volume the more IOPS, max IPS is 16,000
- 3 IOPS per GB, 5334 GB use Max IOPS.

## Provisioned IOPS (PIOPS) SSD

Applications that need more that 16,000 IOPS like apps that need sustained IOPS, for example database workloads. It also supports multi-attach.

### io1/io2 
- 4 GiB - 16 TiB
- Max PIOS 64,000 for Nitro EC2 and 32,000 for others
- Can increase PIOPs independently from storage
- io2 is more durable than io1, so just use io2

### io2 Block Express
- 4 GiB - 64 TiB
- Sub ms latency
- Max PIOPS: 256,000 with IOPS:GiB ratio of 1,000:1

## Hard Disk Drives (HDD)

- Cannot be a boot volume
- 125 MiB to 16 TiB

### stl

Throughput optimised HDD
- Big Data, Data Warehouses, Log Processing
- Max throughput 500 MiB/s - max IOPS 500

### scl

Cold HDD
- Data that is infrequently accessed
- Low cost
- Max throughput 250 MiB/s, max IOPS 250


## EBS Multi-Attach (io1/io2-only)

Attach the same EBS volume to multiple EC2 instances. Each instance has read/write permissions to the volume.

- Use for clustered applications
- apps must manage concurrent write operations
- Must use a file system that is cluster-aware

# Elastic File System - EFS

Managed NFS that can be mounted on many EC2 instances in multi Availiabilty Zones. It is:
- highly available
- scalable
- expensive (3x the cost of gp2)

It is useful for content managment, web serving, data sharing

It uses:
- NFS 4.1
- You must wrap a security group around it.
- Only compatible with Linux AMIs

Performance
- 1000s of concurrent NFS clients, 10 GB+/s throughput.
- Grow to Petabyte scal NFS automatically

Performance modes:
- General Purpose: latency sensitive (web servers, CMS)
- Max I/O: throughput and highly parallel (Big Data, media processing)

## EFS Storage Classes

Storage tiers

- Standard: frequently accessed
- Infrequent: cost to retrieve, low price to store

If you store it in one zone, it is big savings


# EBS versus EFS

EBS Volumes
- Only 1 instance at a time
- Only 1 AZ
- Migration requires snapshot and restore in another AZ
- Root volumes get terminated by default

EFS Volumes
- Mounted to 1 or 100s across multiple AZ
- Only for Linux
- 3x more pricier than EBS
