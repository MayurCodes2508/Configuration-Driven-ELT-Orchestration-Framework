{{
  config(
    tags=['prod'],
    )
}}




WITH base AS (
SELECT pipeline_name,
       DATE(created_at) AS created_at,
       COUNTIF(status='SUCCESS') AS success_count,
       COUNT(*) AS records_count

FROM {{ ref('stg_pipeline_runs') }}

GROUP BY 1, 2
),

slo_metrics_calculations AS (
SELECT pipeline_name,
       created_at,
       SAFE_DIVIDE(success_count, records_count) AS success_rate_for_the_day,

       SAFE_DIVIDE(
        SUM(success_count) OVER(PARTITION BY pipeline_name ORDER BY created_at ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),
        SUM(records_count) OVER(PARTITION BY pipeline_name ORDER BY created_at ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
       ) AS success_rate_over_30_days,


FROM base
)

SELECT pipeline_name,
       created_at,
       success_rate_for_the_day,
       COALESCE(success_rate_for_the_day < 0.95, TRUE) is_slo_threshold_for_the_day_breached,
       success_rate_over_30_days,
       COALESCE(success_rate_over_30_days < 0.99, TRUE) is_slo_threshold_over_30_days_breached

FROM slo_metrics_calculations

ORDER BY created_at DESC






