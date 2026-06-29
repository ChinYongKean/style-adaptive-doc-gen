# Infrastructure DR / RTO / RPO Report

## 1. Overview

This report documents the Disaster Recovery posture of the production AWS infrastructure, covering Recovery Time Objectives and Recovery Point Objectives.

The platform uses a fully managed serverless architecture. Service-level failover is handled transparently by AWS, resulting in near-zero RTO and RPO for availability scenarios.

## 2. Account Information

| Field | Value |
| --- | --- |
| Account Name | Production Environment |
| Account ID | 123456789012 |
| Region | ap-southeast-1 (Singapore) |
| Architecture | Serverless — Fully Managed |

## 3. Service Availability — RTO & RPO

| Service | AZ Config | RPO | RTO | Managed By |
| --- | --- | --- | --- | --- |
| Lambda | Multi-AZ (automatic) | 0 | ~1 min | AWS |
| API Gateway | Multi-AZ (automatic) | 0 | ~1 min | AWS |
| DynamoDB | Multi-AZ (3 replicas) | 0 | ~1 min | AWS |
| S3 | Multi-AZ (3+ facilities) | 0 | ~1 min | AWS |
| OpenSearch | Multi-AZ (configured) | 0 | ~5 min | AWS |

## 4. Data Recovery

- **DynamoDB PITR** — enabled, 35-day retention, RPO ~5 minutes
- **S3 Versioning** — enabled, zero RPO for individual objects
- **OpenSearch Daily Snapshot** — 24-hour RPO, stored in S3

## 5. Recommendations

- Increase OpenSearch snapshot frequency to hourly
- Implement cross-region backup for critical data
- Document re-index-from-DynamoDB runbook as alternative recovery path
