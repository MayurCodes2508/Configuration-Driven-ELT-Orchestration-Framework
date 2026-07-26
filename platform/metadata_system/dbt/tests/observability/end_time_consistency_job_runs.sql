{{
  config(
    tags=['dev']
    )
}}


SELECT run_id

FROM {{ source('metadata', 'raw_job_runs') }}

WHERE
    (end_time < start_time) OR
    (end_time < created_at)