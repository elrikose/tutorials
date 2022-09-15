# Relational Database Service (RDS)

Managed DB service that uses SQL.
- Postgres
- MySQL
- MariaDB
- Oracle
- Microsoft SQL Server
- Aurora (AWS DB)

Managed service
- Automated provisioning/OS patching
- Continuous backups. Restore to a specific timestamp
- Monitoring
- Read replicas for improved read performane
- Multiple AZs for Disaster Recovery
- Maintenance Windows
- Vertical and Horizontal scaling
- EBS backed
- NO SSH to instances

Backups
- Automatically enabled
- Backed up every 5 minutes all the way to oldest
- 7 days of retention (can increase to 35)

Snapshots
- Manually triggered
- Retention for as long as you want

Storage
- If you run out of storage space, RDS autoscales
- Set a Max Storage Threshold
- It will automatically scale
  - Free storage is less than 10%
  - Low storage lasts at least 5 minutes
  - 6 hours have passed since last modification

## RDS Read Replicas

- Up to 5 Read Replicas
- Same AZ, Cross AZ, Cross Region
- Replication is asynchronous
- Can be promoted to a R/W DB.

Use Case
- Main Application writes to Main Database
- Reporting Application reads from read replica
- Read replicas are for SELECT only (no INSERT, UPDATE, or DELETE)

Costs
- Read Replicas have no cost in same region
- There is a cost for multi-region

## Mutli AZ (Disaster Recovery)

- Master database synchronizes changes to a different AZ
- Failover in case of a loss of AZ, network, or storage
- No manual intervention
- Read Replicas can be Multi AZ.
- You don't need to stop the DB to enable Multi AZ
- Behind the scenes, a snapshot is taken and move to a different AZ, then synchronizes.

## Database Encryption

- Encrypt database master and replicas using AWS KMS at launch time
- Master must be encrypted for replicas to be
- You have to restore from a snapshot as encrypted if you encryting an unencrypted database.
- You can use TLS for communication, but requires AWS root certs
- Yse IAM roles to auth instead of user/pass.
- No SSH except RDS custom
- Audit logs can be enabled and sent to CloudWatch.

## Amazon Aurora

- Aurora is a AWS cloud optimized RDBMS.
- Not open source
- Drivers for Postgres and MySQL work for Aurora
- Big performance gains using Aurora over MySQL (5x) and Postgres (3x)
- Storage starts at 10GB and automatically grows up to 128 TB
- Can have up to 15 replicas. MySQL is only 5
- Aurora is HR native
- Costs about 20% more that RDS

HA and Read Scaling
- Stores 6 copies of data across 3 AZ
- 4 out of 6 needed for writes
- 3 out of 6 for reads
- Self healing replication
- Storage is striped across 100s of volumes.
- 1 master takes the writes, automatically fails over in 30s
- Any read replica can become the master
- Supports cross-region replication

Aurora DB Cluster
- There is a writer endpoint that is pointed to the master
- You can setup autoscaling
- There are reader endpoint that connects to all endpoints. Load balancers

Features
- Automatic fail-over
- Backup and Recovery
- Isolation and security
- Industry compliance
- Push button scaling
- Advanced Monitoring
- Routine Maintenance
- Backtrack: restore data to any point in time
