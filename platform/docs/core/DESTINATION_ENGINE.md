# Destination Engine

## Overview

The Destination Engine takes extracted data and writes it to the configured storage layer. In this platform, the storage target is Google Cloud Storage and the data format is Parquet.

## Responsibilities

- Build the destination path using metadata and ingestion timestamps
- Convert raw JSON into a tabular format
- Add ingestion metadata fields
- Upload compressed Parquet files to GCS

## Implementation

The destination logic lives in `el_system/job_executors/dests/gcs.py`.

### Key steps

1. Build the object path using `path_template`
2. Convert API response JSON to a Pandas DataFrame
3. Add `ingestion_timestamp`
4. Write Parquet to an in-memory buffer
5. Upload the buffer to GCS

## Path template

Configured path template:

`{layer}/{source}/{dataset}/{entity}/ingestion_dt={ingestion_dt}/ingestion_ts={ingestion_ts}.{format}`

This structure supports logical partitioning and easy data discovery.

## Current status

The production release writes to `prod-market-analytics-platform-bucket` using the staging layer, while development writes to `dev-market-analytics-platform-bucket` in the dev layer.
