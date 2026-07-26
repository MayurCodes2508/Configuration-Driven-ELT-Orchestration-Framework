{{
  config(
    tags=['prod']
    )
}}



SELECT	is_slo_threshold_for_the_day_breached

FROM {{ ref('slo_successful_runs_success_rate_of_runtime_in_seconds_for_the_day_and_over_30_days') }}

WHERE is_slo_threshold_for_the_day_breached NOT IN (TRUE, FALSE)