{{
  config(
    tags=['dev']
    )
}}



SELECT  run_id,
        start_time,
        created_at

FROM {{ source('metadata', 'raw_job_runs') }}

WHERE created_at > start_time