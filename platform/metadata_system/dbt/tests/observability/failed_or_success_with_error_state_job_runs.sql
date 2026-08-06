{{
  config(
    tags=['dev']
    )
}}

SELECT run_id

FROM {{source('metadata', 'raw_job_runs')}}

WHERE
    (status = 'FAILED' AND error_message IS NULL) OR
    (status = 'SUCCESS' AND error_message IS NOT NULL)
