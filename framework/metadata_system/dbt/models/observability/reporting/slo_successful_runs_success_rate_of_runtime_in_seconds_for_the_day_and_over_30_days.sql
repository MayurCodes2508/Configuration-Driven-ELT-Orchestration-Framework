{{
  config(
    tags=['prod'],
    )
}}





WITH base AS (
SELECT pipeline_name,
       DATE(created_at) AS created_at,
       TIMESTAMP_DIFF(end_time, start_time, SECOND) AS runtime

FROM {{ ref('stg_pipeline_runs') }}

WHERE status = 'SUCCESS'
),

runtime_breach_threshold_flag AS (
SELECT pipeline_name,
       created_at,
       runtime,
       COALESCE(runtime > 120, TRUE) is_runtime_threshold_breached

FROM base
),

success_and_records_count AS (
SELECT pipeline_name,
       created_at,
       COUNTIF(is_runtime_threshold_breached IS false) AS success_count,
       COUNT(*) AS records_count

FROM runtime_breach_threshold_flag

GROUP BY 1, 2
),

slo_metrics_calculations AS (
SELECT pipeline_name,
       created_at,
       SAFE_DIVIDE(success_count, records_count) AS success_rate_for_the_day,
       SAFE_DIVIDE(
        SUM(success_count) OVER(PARTITION BY pipeline_name ORDER BY created_at ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),
        SUM(records_count) OVER(PARTITION BY pipeline_name ORDER BY created_at ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
       ) AS success_rate_over_30_days

FROM success_and_records_count
)

SELECT pipeline_name,
       created_at,
       success_rate_for_the_day,
       COALESCE(success_rate_for_the_day < 0.95, TRUE) AS is_slo_threshold_for_the_day_breached,
       success_rate_over_30_days,
       COALESCE(success_rate_over_30_days < 0.99, TRUE) AS is_slo_threshold_over_30_days_breached

FROM slo_metrics_calculations

