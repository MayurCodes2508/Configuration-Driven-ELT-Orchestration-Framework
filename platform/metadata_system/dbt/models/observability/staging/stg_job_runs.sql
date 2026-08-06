{{
  config(
    tags=['prod'],
    )
}}


SELECT run_id,
       pipeline_run_id,
       lower(trim(job_name)) AS job_name,
       lower(trim(system)) AS system,
       lower(trim(job_type)) AS job_type,
       lower(trim(sub_jobtype)) AS sub_jobtype,
       lower(trim(status)) AS status,
       start_time,
       end_time,
       created_at,
       lower(trim(error_message)) AS error_message,
       job_metrics,
       extra_metadata,
       ingestion_ts

FROM {{ source('metadata', 'raw_job_runs') }}

QUALIFY row_number() OVER(PARTITION BY run_id ORDER BY ingestion_ts) = 1