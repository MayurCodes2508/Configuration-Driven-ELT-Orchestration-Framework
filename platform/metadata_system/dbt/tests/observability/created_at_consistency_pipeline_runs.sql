{{
  config(
    tags=['prod']
    )
}}



SELECT  run_id,
        start_time,
        created_at

FROM {{ source('metadata', 'raw_pipeline_runs') }}

WHERE created_at > start_time