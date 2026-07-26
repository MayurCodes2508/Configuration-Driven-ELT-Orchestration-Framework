{{
  config(
    tags=['prod']
    )
}}



SELECT avg_total_runs_over_30_days

FROM {{ ref('alert_daily_runs_consistency') }}

WHERE avg_total_runs_over_30_days > 24.00