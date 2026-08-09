# Data Lake Layer

## Overview

The Data Lake layer stores raw ingestion output from the CoinGecko API in Google Cloud Storage. This is the first persistent landing zone for the platform.

## Current implementation

- Raw JSON responses are converted to a Pandas DataFrame
- `ingestion_timestamp` metadata is appended
- Data is written as Parquet to GCS
- The landing path is structured by layer, source, dataset, entity, and ingestion date

## Path structure

`{layer}/{source}/{dataset}/{entity}/ingestion_dt={ingestion_dt}/ingestion_ts={ingestion_ts}.{format}`

## Purpose

- Preserve raw ingestion payloads
- Enable replay and recovery
- Prepare data for downstream transformation and analytics

## Current status

The current `prod_v1` release writes raw ingestion output to `prod-market-analytics-platform-bucket` in the staging layer.
