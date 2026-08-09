# Design Tradeoffs

## Overview

This document summarizes the architectural tradeoffs made during the design of `prod_v1`.

## Key tradeoffs

### Custom runner versus workflow engine

- Chosen: custom orchestration in `orchestrator/runner.py`
- Benefit: simple, easy to control, fast to ship
- Tradeoff: less built-in workflow orchestration than managed solutions like Airflow

### Config-driven pipeline versus hardcoded scripts

- Chosen: declarative JSON configs
- Benefit: flexible job definitions and clear separation of logic
- Tradeoff: requires strict schema enforcement and more upfront config design

### GCS landing zone versus direct warehouse writes

- Chosen: write raw data to GCS first
- Benefit: robust raw data retention and separation of ingestion and analytics
- Tradeoff: additional layer between ingestion and analytic warehouse

### Page-based extraction versus incremental ingestion

- Chosen: pagination by page and per_page
- Benefit: matches CoinGecko API and works for `prod_v1`
- Tradeoff: not optimized for delta-only ingestion, which is a future improvement

### Environment separation

- Chosen: separate dev/prod configs, buckets, and secret resources
- Benefit: safer production releases and clear boundary between environments
- Tradeoff: more infrastructure to manage

## `prod_v1` strategy

`prod_v1` prioritizes stability and clarity over advanced orchestration. It delivers a working production ingestion pipeline while leaving advanced retry, incremental loads, and analytics transformation to later versions.
