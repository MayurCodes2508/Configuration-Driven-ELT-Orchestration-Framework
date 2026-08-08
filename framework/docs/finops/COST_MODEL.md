# Cost Model

## Overview

The cost model is designed to keep production infrastructure lightweight while supporting reliable ingestion of market data.

## Primary cost drivers

- Cloud Run execution time
- Google Cloud Storage usage
- Secret Manager and scheduler overhead
- PostgreSQL metadata writes

## Production cost controls

- Production bucket soft-delete retention of 7 days
- Files older than 90 days transition to `COLDLINE`
- Hourly scheduled Cloud Run jobs instead of always-on compute
- Compressed Parquet storage for efficient data storage

## Current status

`prod_v1` uses serverless execution and lifecycle-managed storage. This reduces ongoing compute and storage cost while keeping the ingestion pipeline operational.
