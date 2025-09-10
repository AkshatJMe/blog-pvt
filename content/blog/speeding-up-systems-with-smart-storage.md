+++
title = "Speeding Up Systems With Smart Storage"
description = "Caching is the hidden engine behind fast, responsive systems. This guide breaks down core caching concepts from hits and misses to eviction policies and write strategies—along with tools like Redis, Memcached, and CDNs that power real-world performance at scale."
imagesq = "/images/blog/speeding-up-systems-with-smart-storage/square.jpeg"
image = "/images/blog/speeding-up-systems-with-smart-storage/caching.jpeg"
authorName = "akshat-jain"
date = 2022-03-03T22:20:17+05:30
tags = ["System Design", "caching"]
+++

Caching involves storing frequently accessed data in a fast cache to reduce access latency.  Improves system performance by minimizing data retrieval time. Reduces redundancy in data access.

## Key Terms

### 1. Cache Miss  
**What It Is:** Occurs when requested data isn't found in the cache.  
**Impact:** Requires fetching data from slower main memory, increasing latency.

### 2. Cache Hit  
**What It Is:** Happens when requested data is found in the cache.  
**Impact:** Allows quick retrieval, reducing access time.

### 3. Cache Invalidation  
**Definition:** Marking cached data as invalid or outdated.  
**Purpose:** Ensures that stale data isn’t used.

---

## Cache Eviction Policy

**Purpose:** Decides which items to remove from the cache when full.

- **LRU (Least Recently Used):** Evicts least recently accessed item.  
- **LFU (Least Frequently Used):** Evicts least frequently accessed item.  
- **FIFO (First-In-First-Out):** Evicts the oldest item.  
- **Random Replacement:** Evicts a random item.  
- **MRU (Most Recently Used):** Evicts most recently accessed item.

---

## Cache Write Strategy

- **Write Through:** Writes to both cache and main memory (ensures consistency, higher latency).  
- **Write Back:** Writes to cache first, updates main memory later (fast but risk of inconsistency).  
- **Write Around:** Writes directly to main memory, bypassing cache (avoids unnecessary caching).

---

## Differences Between Cache and Databases

| Feature         | Cache                    | Database                 |
|-----------------|--------------------------|--------------------------|
| Purpose         | Performance enhancement  | Structured data storage   |
| Data Durability | Sacrifices persistence   | Prioritizes durability    |
| Latency         | Low                      | Higher                   |
| Data Management | Lightweight structures   | Complex management        |
| Lifespan        | Short-term               | Long-term                |


---

## Distributed Cache

**Definition:** A caching system across multiple nodes.  
**Benefits:** Improves scalability, availability, and performance.

---

## Caching Tools

- **Redis:** In-memory store, supports data structures, persistence, distributed caching.  
- **Memcached:** Optimized for quick lookups, distributed, no persistence.

---

## Content Delivery Network (CDN)

**Definition:** Distributed servers for efficient content delivery.

### Why CDNs Are Needed

- Reduces latency  
- Global reach  
- Scalability  
- Load balancing  
- Content caching  
- Dynamic content acceleration  
- Security & reliability  
- Improved user experience  
- Bandwidth savings

### Examples of CDNs

Akamai, Cloudflare, Amazon CloudFront, Microsoft Azure CDN, KeyCDN, Cachefly.