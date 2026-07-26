# Optimization Strategies

## Overview

These strategies improve the efficiency and cost profile of the platform in `prod_v1`.

## Current optimizations

- `per_page` and `page` pagination match the CoinGecko API
- Prod page size is set to 250 for fewer total requests
- Data is written as compressed Parquet with Snappy
- Objects are partitioned logically by ingestion date and timestamp
- Serverless Cloud Run execution avoids long-lived infrastructure cost

## Cost-aware design

- Batch API extraction minimizes request overhead
- GCS lifecycle rules reduce long-term storage cost
- Separate dev/prod resources prevent test traffic from affecting production costs

## Future opportunities

- Add incremental ingestion to reduce data volume
- Add retries with exponential backoff for transient failures
- Add downstream warehouse optimization in BigQuery/dbt
