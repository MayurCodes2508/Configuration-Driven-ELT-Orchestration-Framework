# Configuration System

## Overview

The Configuration System defines pipeline behavior through structured JSON files. Each job config declares the data source, execution parameters, authentication, and destination settings.

## Benefits

- Decouples pipeline behavior from code
- Supports reusable and environment-specific job definitions
- Enables rapid deployment of new ingestion jobs
- Makes pipeline changes visible in config

## Job config structure

A config includes:

- `pipeline_name`
- `job_name`
- `job_type`
- `metadata`
- `exec`
- `destination`

## Current config examples

- `el_system/configs/job/coingecko_sources/dev/market_price.json`
- `el_system/configs/job/coingecko_sources/prod/market_price.json`

Both configs use the same schema and differ mainly by environment-specific bucket and runtime settings.

## Design

The system follows the principle: define what to do, not how to do it. This enables the runner to interpret job definitions dynamically, making the platform extensible.
