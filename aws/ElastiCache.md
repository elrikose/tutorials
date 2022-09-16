# ElastiCache

Used to get managed Redis or Memcached, in-memory DBs. High-performance, low latency.

- Makes your application stateless
- AWS handles OS maintenance/patching
- Requires a lot of application code changes.

Use Case #1
- Works just like a cache with the backend being RDS.
- You must have strategies for invalidating data

Use Case #2
- Application data stored in a cache

Redis
- Mult AZ with failover
- There are read replicas
- Backup and Restore

Memcached
- Sharding architecture
- No HA
- Doesn't persist
- Can't backup and restore
- multithreaded

## Caching Stategies

Lazy Loading / Cache Aside / Lazy Population
- Cache hits are great because it is 1 query
- Cache misses are expensive because they require a 3 step query
  - Check the cache (miss)
  - Load from DB
  - Write to cache
- It takes a while to load the cache (warm up the cache)

Write Through
- When app writes to the DB, it also loads in cache
- You will have to use Lazy Loading as well for stuff not written to the cache.
- If cache is small you may have to write a lot of data that is never read.
- Usually an optimization to Lazy Loading

Cache Evictions and Time to Live (TTL)
- Get rid of items when:
  - Stale
  - Memory is full
  - TTL
- TTL can be seconds to days

## ElastiCache Replication

Cluster Mode Disabled - You can have 1 primary node and up to 5 replicas for failover.

- Asynchronous
- Primary is read/write
- Other nodes are read-only

Cluster Mode Enabled - Data is partitioned across shards.

- Each shard has a primary and up to 5 replicase
- Multi-AZ
- Up to 500 nodes per cluster