{{
  config(
    tags=['prod']
    )
}}



SELECT  success_rate_over_30_days

FROM {{ ref('slo_successful_runs_success_rate_for_the_day_and_over_30_days') }}

WHERE success_rate_over_30_days NOT BETWEEN 0 and 1
