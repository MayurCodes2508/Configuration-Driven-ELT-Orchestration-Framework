# **MARKET ANALYTICS PLATFORM - PRODUCTION RELEASE CHANGELOG**

## **Overview**

This release introduces significant architectural improvements to the data platform, focusing on modularization, metadata management, and observability enhancements.

---

### **1. CI/CD & INFRASTRUCTURE IMPROVEMENTS**

#### **New Workflows Added**

- **dbt Transformations CI** (`.github/workflows/ci_dbt_transformations.yml`)
  - Automated build and test pipeline for dbt models
  - GCP authentication with workload identity
  - Python 3.12.3 support with pip dependency management
  - Separate build and test jobs with conditional test execution on dev branch

#### **Workflow Standardization**

- Unified workflow structure across `ci_el_system.yml`, `ci_metadata_system.yml`, and `ci_orchestrator_run.yml`
- Added `defaults.run.working-directory` for consistent working paths
- Standardized job structure: **Build** (main execution) + **Test** (conditional on dev branch)
- Added `workflow_dispatch` trigger for manual executions
- Restructured dependency compilation and validation steps
- Docker containerization for reproducible test environments

#### **Key Workflow Changes**

- Removed per-workflow YAML path triggers (`.github/workflows/*.yml` removed from paths)
- Removed feature branch (`feature/**`) pattern from metadata and orchestrator workflows
- Unified authentication pattern with `id: auth` for credential reuse
- Python version pinned to `3.12.3` for consistency

---

### **2. DATA TRANSFORMATION LAYER (dbt) RESTRUCTURING**

#### **Project Structure Reorganization**

- **Moved** `models/staging/`, `models/reporting/`, `models/docs.md`, `models/exposures/`, `models/sources/` → `models/observability/`
- Created **two business domains**:
  - **`business/`** - Business-focused analytics models
  - **`observability/`** - Pipeline and system monitoring models

#### **Model Reorganization**

- **Staging Models** (`dbt_transformations/models/observability/staging/`)
  - New: `stg_pipeline_runs.sql` - Pipeline execution tracking
  - New: `stg_job_runs.sql` - Individual job execution tracking

- **Reporting Models** (`dbt_transformations/models/observability/reporting/`)
  - `slo_successful_runs_success_rate_for_the_day_and_over_30_days.sql` - SLO tracking for success rates
  - `slo_successful_runs_success_rate_of_runtime_in_seconds_for_the_day_and_over_30_days.sql`
  - Updated runtime threshold: **15 seconds → 120 seconds**
  - New metadata YAML files for both models with comprehensive column definitions

- **New Alerts Module** (`dbt_transformations/models/observability/alerts/`)
  - `alert_daily_runs_consistency.sql` - Daily pipeline execution consistency monitoring
  - Detects anomalies using 30-day rolling average

#### **Data Tests**

- **20+ new tests** added to `dbt_transformations/tests/observability/`:
  - Alert consistency validation
  - SLO threshold validation (for runs and runtime)
  - Job/pipeline run state consistency
  - Timestamp ordering validation
  - Error message correlation with status

#### **Configuration Updates**

- **dbt_project.yml**: New tag-based organization
  - Models tagged with `business` or `observability`
  - Sub-tags: `prod`, `dev` for environment control
  - New data_tests section for test tagging

- **Dockerfile** (`dbt_transformations/Dockerfile`):
  - Separated `COPY` commands for better caching
  - Added `ENTRYPOINT` with dbt commands
  - Runs: source freshness → tests → models

#### **Documentation Updates**

- Enhanced column descriptions in `docs.md`
- New documentation for `alert_daily_runs_consistency` model
- Improved markdown formatting with headers

#### **Source Configuration**

- New `sources.yml` with comprehensive raw data documentation:
  - `raw_pipeline_runs` - Pipeline execution records
  - `raw_job_runs` - Individual job records
  - Freshness checks (warn after 3h, error after 6h)
  - Data quality tests with SQL validators

---

### **3. ORCHESTRATION SYSTEM REFACTORING**

#### **Architecture Changes** (el_system, metadata_system, orchestrator)

**Job Configuration Schema Simplification:**

- **Removed** from job configs: `job_name`, `system`, `job_type`, `sub_jobtype`
- **New approach**: Dynamically derived from execution context:
  - `job_type`: "extraction" or "ingestion" (determined by presence of `dest`)
  - `sub_jobtype`: Derived from `exec_type` (e.g., "Api" from "ApiExecCmd")
  - `system`: Set to "el" or "metadata" at runtime

**Metadata Class Improvements:**

- New `get_metadata()` method for dynamic metadata derivation
- Updated `build_job_metadata()` to accept `job_name` parameter
- Centralized system identifier logic

**Orchestrator Error Handling:**

- New structured error handling in `orchestrator.py`:
  - Separate try-catch blocks for: loading, validation, execution
  - Detailed METADATA_DUMP at each failure point
  - Graceful error propagation with context

- Logging enhancements:
  - Removed default logger configuration
  - Added stdout/stderr filtering by log level
  - CRITICAL logs go to stderr only

**Runner Class Refactoring:**

- Constructor now takes `loader` instead of `metadata`
- Lazy evaluation of exec_cfg and dest_cfg
- Improved null-safety checks

---

#### **API Execution Command Enhancement** (el_system)

**Before:**

```json
{
  "base_url": "https://api.coingecko.com/api/v3",
  "path": "/coins/markets"
}
```

**After:**

- `base_url` removed from job configs
- New `root_url_registry` in `APIExec` class:

  ```python
  root_url_registry = {"coingecko": "https://api.coingecko.com/api/v3"}
  ```

- URL construction is now centralized and source-driven
- ApiExecCommand now accepts `url` parameter

**Benefits:**

- Eliminates hardcoded URLs in configs
- Single source of truth for API endpoints
- Easier to manage across environments

---

#### **Schema Validation Updates**

**Removed Requirements:**

- `job_name`, `system`, `job_type`, `sub_jobtype` no longer required in root schema

**API Exec Schema Changes:**

- Removed `base_url` field requirement
- Updated path minLength: 1 → 2
- Changed `vs_currency` from enum to constant: `"inr"`

**GCS Destination Schema:**

- Updated bucket minLength: 1 → 2
- Updated format minLength: 1 → 2

---

### **4. JOB CONFIGURATION UPDATES**

**Simplified Job Configs:**

- Removed static metadata from:
  - `el_system/configs/job/coingecko_sources/dev/market_price.json`
  - `el_system/configs/job/coingecko_sources/prod/market_price.json`
  - `metadata_system/configs/job/neon_sources/*/job_runs.json`
  - `metadata_system/configs/job/neon_sources/*/pipeline_runs.json`

- Configs now contain only:
  - `metadata` (source, dataset, entity)
  - `exec` (execution type and parameters)
  - `dest` (destination configuration, if applicable)

---

### **5. DEPENDENCY & ENVIRONMENT MANAGEMENT**

#### **Python Requirements Updates**

**Standardization:**

- Python version: 3.14 → **3.12** (across all systems)
- Requirements regenerated with explicit dependency documentation

**Key Changes:**

- dbt-core: **1.11.11** with all adapters updated
- google-cloud-bigquery: **3.41.0** with pandas support
- Removed python-dotenv from explicit dependencies
- Added comprehensive dependency tree comments

#### **Dev Requirements**

- Removed `-c requirements.txt` constraint lines (cleaner dependency management)
- Explicit dependency tracking improved

---

### **6. GITIGNORE & ENVIRONMENT CONFIGURATION**

#### **Updated .gitignore**

- Changed: `*dev_testing.py*` → `dev_test*` (broader pattern)
- Removed: `tests/` directory from ignore
- Added: `state/` directory to ignore

#### **Environment Variables**

- **example.env** formatting normalized:
  - Changed: `API_KEY = ABC...` → `API_KEY=ABC...` (no spaces around `=`)

---

### **7. LOGGING IMPROVEMENTS**

#### **Log Statement Reordering**

Consistent pattern applied across all systems:

- Success/initialization message first
- Completion/metadata message last

Example (el_system, metadata_system, orchestrator):

```python
# Before
log.info("Metadata Loading Completed...")
log.info("Obj: X | Instance Initialized Successfully...")

# After
log.info("Obj: X | Instance Initialized Successfully...")
log.info("Metadata Loading Completed...")
```

#### **New Logging Configuration** (orchestrator)

- Loguru logger setup with stream filtering
- INFO, SUCCESS, ERROR, WARNING, DEBUG, TRACE → stdout
- CRITICAL → stderr

---

### **8. ERROR HANDLING IMPROVEMENTS**

#### **Exception Handling Pattern**

- **Before**: Generic `raise` statements
- **After**: Removed automatic re-raise; errors logged with context

Applied to:

- `orchestrator/loader.py` - Job catalog and config loading
- `orchestrator/validator.py` - Schema validation
- `el_system/orchestrator/validator.py`
- `metadata_system/orchestrator/validator.py`

---

### **9. RUNTIME ADJUSTMENTS**

#### **Sleep Time Adjustments** (orchestrator)

- Execution start time polling: 3 seconds → **5 seconds**
- Cloud Logging query delay: 5 seconds → **10 seconds**
- Better reliability for external service queries

---

### **10. DOCKERFILE OPTIMIZATIONS**

**Layer Caching Improvements:**

- Separated COPY statements for better rebuild efficiency
- Requirements copied separately
- dbt_project.yml copied as its own layer
- packages.yml separated from dependencies

---

## **MIGRATION GUIDE FOR PRODUCTION**

### **Critical Changes**

1. **Job Configuration Update Required**
   - Remove `job_name`, `system`, `job_type`, `sub_jobtype` from all job JSONs
   - Test with new metadata derivation logic

2. **API Endpoint Management**
   - Review all API configurations
   - Ensure source names match `root_url_registry`
   - Remove hardcoded `base_url` fields

3. **dbt Models**
   - Update any documentation references to old model paths
   - Review observability/business model separation
   - Test all 20+ new data quality tests

4. **Schema Validation**
   - Update client code expecting old required fields
   - Validate new runtime thresholds (120s for runtime SLO)

5. **Environment Compatibility**
   - Pin to Python 3.12.3
   - Update container base images
   - Regenerate requirements.txt if needed

---

## **TESTING CHECKLIST**

- [ ] dbt models compile successfully
- [ ] All 20+ new data quality tests pass
- [ ] API orchestration with new URL registry works
- [ ] Database orchestration without job_name in config works
- [ ] New alerting models populate correctly
- [ ] SLO tracking with 120s threshold functional
- [ ] Logging output to stdout/stderr correct
- [ ] Docker builds for all systems complete
- [ ] GitHub Actions workflows trigger correctly
