{{
  config(
    tags=['prod'],
    )
}}




SELECT is_alert_threshold_for_the_day_breached

FROM {{ ref('alert_daily_runs_consistency') }}

WHERE (is_alert_threshold_for_the_day_breached IS FALSE AND total_runs < avg_total_runs_over_30_days) OR
      (is_alert_threshold_for_the_day_breached IS TRUE AND total_runs > avg_total_runs_over_30_days)