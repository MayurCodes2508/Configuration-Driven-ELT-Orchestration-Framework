# Environments

## Supported environments

The project supports two separate environments:

- `dev`
- `prod`

Each environment uses dedicated configuration, storage, and runtime resources.

## Environment-specific configs

- Dev job config: `el_system/configs/job/coingecko_sources/dev/market_price.json`
- Prod job config: `el_system/configs/job/coingecko_sources/prod/market_price.json`

## Environment differences

- Dev uses `dev-market-analytics-platform-bucket` and `layer = dev`
- Prod uses `prod-market-analytics-platform-bucket` and `layer = staging`
- Dev EL ingestion runs via `dev-el-system-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/el-job:testing`
- Dev dbt execution runs via `dev-dbt-transformations-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/dbt-job:dev_v1`
- Dev pipeline orchestration runs via `dev-pipeline-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/pipeline_run:testing`
- Dev metadata ingestion runs via `dev-metadata-system-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/metadata-job:testing`
- Prod EL ingestion runs via `prod-el-system-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/el-job:latest`
- Prod dbt execution runs via `prod-dbt-transformations-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/dbt-job:prod_v1`
- Prod pipeline orchestration runs via `prod-pipeline-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/pipeline_run:latest`
- Prod metadata ingestion runs via `prod-metadata-system-run` using `asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/metadata-job:latest`
- Prod uses Cloud Scheduler for ingestion execution

## Secrets and credentials

- Local development uses `dev.env` for `COINGECKO_API_KEY` and `DB_URL`
- Production is provisioned to use Google Secret Manager via Terraform

## Current status

`prod_v1` is the current production environment release. Dev remains isolated so testing can continue without affecting production resources.
