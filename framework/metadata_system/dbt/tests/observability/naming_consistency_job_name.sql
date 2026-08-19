{{
  config(
    tags=['dev'],
    )
}}


SELECT run_id

FROM {{ source('metadata', 'raw_job_runs') }}

WHERE job_name NOT LIKE 'prod_%'