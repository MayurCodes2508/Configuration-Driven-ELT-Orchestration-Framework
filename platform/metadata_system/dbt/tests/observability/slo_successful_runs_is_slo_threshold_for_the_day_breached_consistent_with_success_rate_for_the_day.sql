{{
  config(
    tags=['prod']
    )
}}



SELECT  is_slo_threshold_for_the_day_breached

FROM {{ ref('slo_successful_runs_success_rate_for_the_day_and_over_30_days') }}

WHERE   (is_slo_threshold_for_the_day_breached IS FALSE AND success_rate_for_the_day < 0.95) OR
        (is_slo_threshold_for_the_day_breached IS TRUE AND success_rate_for_the_day >= 0.95)
