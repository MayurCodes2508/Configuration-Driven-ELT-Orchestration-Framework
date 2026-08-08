# Schema Validation

## Overview

Schema validation enforces correctness of every job configuration before the runner executes it. This prevents invalid pipeline definitions from reaching runtime.

## Implementation

The schema is defined in `el_system/schemas/root_schema.json`, which references `el_system/schemas/exec_schemas/api_exec_schema.json` and `el_system/schemas/dest_schemas/gcs_dest_schema.json`. It includes requirements for:

- pipeline identification
- metadata fields
- execution parameters
- pagination settings
- page size controls
- query parameters
- authentication config
- destination settings

## Validation flow

1. Load job configuration
2. Load JSON schema
3. Validate the config using `jsonschema_rs`
4. Fail fast if the config is invalid

## Current constraints

- `pipeline_name` must be `market_analytics_platform`
- `job_name` must start with `dev_` or `prod_`
- `job_type` is currently fixed to `ingestion`
- `exec.type` must be `ApiExecCommand`
- production page size is enforced at up to 250
- destination format is fixed to `parquet`

## Benefits

- catches configuration issues early
- ensures consistent job structure
- reduces runtime errors
- supports future config-driven expansion
