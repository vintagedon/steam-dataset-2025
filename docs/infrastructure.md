<!--
---
title: "Infrastructure Specifications and Performance Analysis"
description: "Comprehensive documentation of the Steam Dataset 2025 computational infrastructure, including hardware specifications, database performance benchmarks, and optimization strategies for multi-modal analytics at scale"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-02"
version: "1.0"
status: "Published"
tags:
- type: [infrastructure-documentation/performance-analysis/technical-specifications]
- domain: [database-performance/postgresql/system-architecture/benchmarking]
- tech: [postgresql-16/proxmox/nvme-storage/intel-i9/ubuntu-24-04]
- audience: [data-engineers/database-administrators/researchers/infrastructure-teams]
related_documents:
- "[Data Dictionary](data_dictionary-pending.md)"
- "[Project Repository Overview](../README.md)"
- "[Database Schema Documentation](../database/schema.sql)"
---
-->

# 🏗️ Infrastructure Specifications and Performance Analysis

This document provides comprehensive technical specifications and performance analysis for the Steam Dataset 2025 computational infrastructure. The infrastructure demonstrates enterprise-grade capabilities optimized for multi-modal analytics, supporting relational data processing, vector similarity search, and graph analysis at scale within the Proxmox Astronomy Lab environment.

---

# 🎯 1. Introduction

This section establishes the infrastructure context for the Steam Dataset 2025 project, documenting the computational environment used to develop, test, and validate our multi-modal database approach. The specifications provide essential reproducibility information and performance baselines for researchers working with similar large-scale gaming datasets.

## 1.1 Purpose

This documentation serves as the definitive reference for the computational infrastructure supporting Steam Dataset 2025 development and validation. It provides performance baselines, configuration specifications, and optimization strategies discovered through systematic testing and real-world application with 8,711+ applications and 36,265+ user reviews.

## 1.2 Scope

What's Covered:

- Complete hardware specifications and performance characteristics
- PostgreSQL 16 configuration optimized for multi-modal workloads
- Database performance benchmarks with Steam dataset workloads
- Storage subsystem analysis and optimization recommendations
- Infrastructure scaling considerations for full 260k+ dataset

## 1.3 Target Audience

Primary Users: Database administrators, data engineers, infrastructure teams implementing similar analytics platforms  
Secondary Users: Academic researchers requiring reproducibility specifications, developers optimizing PostgreSQL for analytics workloads  
Background Assumed: Familiarity with database administration concepts, PostgreSQL configuration, and basic system benchmarking principles

## 1.4 Overview

The infrastructure employs a virtualized approach within Proxmox enterprise virtualization, combining high-performance Intel processors with enterprise NVMe storage optimized for analytical workloads. Configuration emphasizes write-heavy database operations while maintaining sub-millisecond read performance for interactive analytics applications.

---

# 📋 2. Hardware Specifications

This section details the physical and virtual hardware configuration supporting the Steam Dataset 2025 infrastructure, providing complete specifications necessary for performance analysis and reproducibility.

## 2.1 Virtual Machine Configuration

The Steam Dataset 2025 infrastructure operates on proj-pgsql01, a dedicated PostgreSQL virtual machine within the Proxmox Astronomy Lab cluster.

| Component | Specification | Performance Impact |
|---------------|------------------|----------------------|
| Host CPU | Intel i9-13900H (Raptor Lake) | High single-thread performance for complex queries |
| vCPU Allocation | 8 virtual cores | Optimized for PostgreSQL connection handling |
| Memory | 32 GiB RAM | Sufficient for 12 GiB shared_buffers + OS overhead |
| Storage Controller | virtio-scsi with io_uring | Modern async I/O for optimal database performance |
| Network | Virtio-net (10 Gbps internal) | High-bandwidth cluster communication |

## 2.2 Storage Subsystem

Storage performance is critical for database analytics workloads, particularly for Write-Ahead Log (WAL) operations that constrain transaction throughput.

| Component | Specification | Performance Characteristics |
|---------------|------------------|-------------------------------|
| Primary Storage | Samsung PM983 1.92TB NVMe SSD | Enterprise-grade endurance (1.3 DWPD) |
| Form Factor | M.2 22110 (MZ1LB1T9HALS-00007) | PCIe 3.0 interface |
| Sequential Performance | 3,000 MB/s read / 1,400 MB/s write | Measured: ~1.02 GiB/s sustained write |
| Random Performance | 480k read IOPS / 42k write IOPS | Critical for database random access |
| Cache Configuration | No cache (Proxmox default) | Direct storage access for consistency |

### Storage Performance Validation

Systematic testing confirmed storage capabilities exceed database requirements:

```bash
# 16KB sequential write test (simulating PostgreSQL WAL)
fio --name=pg-wal --filename=/mnt/data/.waltest --size=2G \
    --bs=16k --rw=write --iodepth=32 --numjobs=2 --direct=1 --group_reporting
```

Results:

- Aggregate Bandwidth: 1,023 MiB/s (~1.02 GiB/s)  
- IOPS: 65,500 (16KB operations)
- Latency: Average 30 µs, p95 48 µs, p99 94 µs
- Device Utilization: 71% (indicating headroom for additional VMs)

---

# ⚙️ 3. Software Configuration

This section documents the complete software stack configuration, emphasizing PostgreSQL optimization for multi-modal analytics workloads combining relational data, JSONB documents, and vector similarity search.

## 3.1 Operating System Environment

| Component | Version | Configuration Notes |
|---------------|-------------|------------------------|
| Operating System | Ubuntu 24.04 LTS | Long-term support for stability |
| Kernel | 6.8+ (Ubuntu default) | Modern io_uring support |
| PostgreSQL | 16.10 | Latest stable with vector extension support |
| Python Environment | 3.9+ | Data processing and analytics |

## 3.2 PostgreSQL Configuration

The PostgreSQL configuration balances analytical performance with system stability, optimized through systematic benchmarking with Steam dataset workloads.

### Memory and Performance Settings

```sql
-- Core memory configuration
shared_buffers = 12GB                    -- 37.5% of total RAM (PostgreSQL best practice)
effective_cache_size = 24GB              -- 75% of total RAM for query planning
work_mem = 64MB                          -- Per-operation memory (increase to 512MB for complex joins)
maintenance_work_mem = 2GB               -- Large enough for index creation and VACUUM
```

### Write-Ahead Logging (WAL) Optimization

```sql
-- WAL configuration for high-volume writes
wal_level = replica                      -- Required for pgvector replication
wal_compression = on                     -- Reduce WAL size and I/O
max_wal_size = 32GB                      -- Prevent checkpoint storms during bulk loads
min_wal_size = 2GB                       -- Reasonable minimum for steady-state
checkpoint_timeout = 15min               -- Balance durability vs. performance
checkpoint_completion_target = 0.9       -- Spread checkpoint I/O over time
```

### Query Processing and Parallelism

```sql
-- Parallel query configuration
max_parallel_workers = 8                 -- Match vCPU count
max_parallel_workers_per_gather = 4      -- Allow parallel scans for large tables
effective_io_concurrency = 256           -- NVMe can handle high concurrency
random_page_cost = 1.10                  -- Slightly favor sequential over random (NVMe)
seq_page_cost = 1.0                      -- Baseline for cost calculations
```

### Monitoring and Extensions

```sql
-- Performance monitoring
shared_preload_libraries = 'pg_stat_statements'
track_io_timing = on                     -- Essential for I/O performance analysis

-- Vector similarity search support
CREATE EXTENSION IF NOT EXISTS vector;   -- pgvector for embeddings
```

---

# 📊 4. Performance Benchmarks and Analysis

This section presents comprehensive performance analysis based on systematic benchmarking with PostgreSQL standard tools and real Steam dataset workloads. All benchmarks were conducted with the production configuration and provide realistic performance expectations.

## 4.1 Database Transaction Performance

### Read-Write Transaction Throughput

PostgreSQL's standard pgbench tool provides reliable transaction throughput measurements using the TPC-B-like workload with scale factor 100 (equivalent to ~10GB database).

| Concurrent Connections | Transactions per Second | Average Latency | Performance Notes |
|---------------------------|---------------------------|-------------------|-------------------|
| 8 | 12,563.8 TPS | 0.637 ms | Linear scaling region |
| 16 | 20,145.1 TPS | 0.794 ms | Optimal concurrency |
| 32 | 21,607.2 TPS | 1.481 ms | Peak throughput |
| 64 | 18,455.6 TPS | 3.468 ms | Contention degradation |

Key Finding: Peak durable write performance occurs at 32 concurrent connections, limited by WAL fsync operations rather than storage bandwidth.

### Read-Only Query Performance

```bash
# Hot cache read-only benchmark
sudo -u postgres pgbench -S -T 60 -c 16 -j 8 bench
```

Result: 205,504.5 TPS with 0.078 ms average latency, demonstrating excellent memory-resident performance for interactive analytics.

## 4.2 WAL Performance Analysis

Write-Ahead Log performance directly constrains transaction throughput in PostgreSQL. Systematic testing isolated the commit/flush bottleneck:

### Commit/Flush Ceiling Test

```bash
# Simulate PostgreSQL commit pattern with fsync per write
fio --name=wal-commit --filename=/mnt/data/.waltest --size=1G \
    --bs=16k --rw=write --ioengine=psync --fdatasync=1 \
    --direct=1 --time_based=1 --runtime=30
```

Results:

- Maximum fsync operations: 6,068 per second
- Fsync latency percentiles: p50 67 µs, p95 379 µs, p99 523 µs
- Group commit efficiency: ~3.3-3.6 transactions per fsync at peak throughput

Interpretation: The measured 21,607 TPS aligns perfectly with 6,068 fsync/s × 3.56 transactions/fsync, confirming that transaction throughput is WAL-bound, not storage-bound.

## 4.3 Steam Dataset Workload Performance

Real-world performance with Steam dataset operations demonstrates practical capabilities:

### Bulk Data Ingestion

- 8,711 applications + 36,265 reviews: Ingested in 12 seconds using COPY with local synchronous_commit disabled
- Sustained write rate: ~707 records per second during transactional inserts
- Vector index creation: HNSW indexes built in <3 seconds for 8k applications

### Analytical Query Performance

| Query Type | Response Time | Notes |
|----------------|------------------|-----------|
| Genre aggregations | <50 ms | Materialized views with unique indexes |
| Price distribution analysis | <100 ms | Direct column access with btree indexes |
| JSONB content searches | 200-500 ms | Depends on JSON complexity and filters |
| Vector similarity search | <10 ms | HNSW index enables sub-10ms k-NN queries |

---

# 🔧 5. Optimization Strategies and Scaling Considerations

This section provides actionable optimization strategies discovered through systematic testing and practical experience with Steam dataset workloads, along with scaling considerations for production deployments.

## 5.1 Performance Optimization Guidelines

### For High-Volume Ingestion

During bulk data loading operations, significant performance improvements are achievable through session-scoped configuration changes:

```sql
BEGIN;
SET LOCAL synchronous_commit = off;      -- Allow WAL batching for bulk operations
SET LOCAL work_mem = '512MB';            -- Increase memory for large sorts/joins
-- Perform bulk operations (COPY, large INSERTs)
COMMIT;
ANALYZE <affected_tables>;               -- Update statistics after bulk changes
```

Performance Impact: 2-4x throughput improvement for bulk loading operations with minimal risk during controlled ingestion periods.

### For Complex Analytics Workloads

```sql
-- Session optimization for complex queries
SET work_mem = '1GB';                    -- Increase for multi-table joins
SET enable_hashjoin = on;                -- Ensure hash joins are available
SET random_page_cost = 1.0;              -- Trust NVMe random access performance
```

## 5.2 Multi-VM Scaling Strategy

The Samsung PM983 NVMe provides substantial headroom for multiple database VMs:

### Theoretical Scaling Capacity

- Current utilization: ~65.5k IOPS (16KB sequential writes)
- Drive capacity: 480k read IOPS, 42k write IOPS (4KB random)
- Scaling headroom: Support for 3-5 additional similar workloads

### Recommended VM Distribution

| Workload Type | VM Count | Resource Allocation | Expected Performance |
|------------------|-------------|------------------------|------------------------|
| Analytics (Read-heavy) | 2-3 VMs | 16 GB RAM, 4 vCPU | >100k TPS read-only |
| OLTP (Balanced) | 2-3 VMs | 24 GB RAM, 6 vCPU | ~15k TPS durable writes |
| ETL/Processing | 1-2 VMs | 32 GB RAM, 8 vCPU | Batch processing |

### Performance Monitoring

Essential metrics for ongoing performance validation:

```sql
-- Key monitoring queries
SELECT * FROM pg_stat_database WHERE datname = 'steam5k';
SELECT * FROM pg_stat_user_tables WHERE relname LIKE 'applications%';
SELECT query, calls, mean_exec_time FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;
```

---

# 📚 6. References & Related Resources

This section provides comprehensive references to hardware specifications, benchmark methodologies, and PostgreSQL optimization resources used in developing and validating the infrastructure configuration.

## 6.1 Internal References

| Document Type | Title | Relationship | Link |
|-------------------|-----------|------------------|----------|
| [Schema Documentation] | Database Schema & Structure | Infrastructure supports this schema design | [../database/schema.sql] |
| [Performance Benchmarks] | Raw Benchmark Results | Source data for performance analysis | [pgsql01-benchmarks.txt] |
| [Configuration Files] | PostgreSQL Configuration | Complete production configuration | [../database/postgresql.conf] |

Repository Navigation: Use current repository structure from repo-tree.txt for accurate file paths and cross-references.

---

# 📜 7. Documentation Metadata

This section provides comprehensive information about document creation, revision history, and authorship, maintaining transparency about the document's development process and enabling effective version management.

## 7.1 Change Log

| Version | Date | Changes | Author |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-02 | Initial documentation creation with complete infrastructure specifications | VintageDon |

*Document Version: 1.0 | Last Updated: 2025-09-02 | Status: Published*
