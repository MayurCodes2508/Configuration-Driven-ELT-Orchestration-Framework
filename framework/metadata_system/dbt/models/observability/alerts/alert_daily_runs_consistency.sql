{{
  config(
    tags=['prod']
    )
}}


WITH base AS (
SELECT  pipeline_name,
        DATE(created_at) AS _day,
        COUNT(*) AS total_runs

FROM {{ ref('stg_pipeline_runs') }}

GROUP BY 1, 2
),

comparison_metric AS (
SELECT  pipeline_name,
        _day,
        total_runs,
        AVG(total_runs) OVER(PARTITION BY pipeline_name ORDER BY _day DESC ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS avg_total_runs_over_30_days

FROM base
)

SELECT  pipeline_name,
        _day,
        total_runs,
        avg_total_runs_over_30_days,
        COALESCE(total_runs < avg_total_runs_over_30_days, TRUE) AS is_alert_threshold_for_the_day_breached

FROM comparison_metric