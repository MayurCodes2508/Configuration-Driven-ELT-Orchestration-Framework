{{
  config(
    tags=['prod']
    )
}}


SELECT run_id

FROM {{ source('metadata', 'raw_pipeline_runs') }}

WHERE
    (ingestion_ts < end_time) OR
    (ingestion_ts < created_at) OR
    (ingestion_ts < start_time)