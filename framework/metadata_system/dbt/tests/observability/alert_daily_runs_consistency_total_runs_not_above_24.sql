{{
  config(
    tags=['prod']
    )
}}



SELECT total_runs

FROM {{ ref('alert_daily_runs_consistency') }}

WHERE total_runs > 24