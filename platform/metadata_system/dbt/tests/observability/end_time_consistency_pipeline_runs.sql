{{
  config(
    tags=['prod']
    )
}}


SELECT run_id

FROM {{ source('metadata', 'raw_pipeline_runs') }}

WHERE
    (end_time < start_time) OR
    (end_time < created_at)