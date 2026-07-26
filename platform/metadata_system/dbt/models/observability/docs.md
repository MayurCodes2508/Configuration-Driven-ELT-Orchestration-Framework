# Column Descriptions

{% docs pipeline_runs_status %}

## Pipeline Run Status

The `status` column indicates the final execution state of a pipeline run.  

| Status   | Description                                                             |
|----------|-------------------------------------------------------------------------|
| SUCCESS  | `The pipeline run completed successfully and jobs were executed.`       |
| FAILED   | `The pipeline run terminated with an error.`                            |

{% enddocs %}

{% docs job_runs_status %}

## Job Run Status

The `status` column indicates the final execution state of a job run.  

| Status   | Description                                                             |
|----------|-------------------------------------------------------------------------|
| SUCCESS  | `The job run completed successfully and rows were processed.`           |
| FAILED   | `The job run terminated with an error.`                                 |

{% enddocs %}

{% docs pipeline_runs_run_success_rate_slo_breached_for_the_day %}

## Daily Pipeline Runs Run Success Rate SLO Breach Flag

The `is_slo_threshold_for_the_day_breached` column indicates whether the daily run success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                       |
|------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_for_the_day < 0.95`          | `The daily success‑rate target (≥=95%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_for_the_day >= 0.95`         | `The daily success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_run_success_rate_slo_breached_over_30_days %}

## Over 30 Days Pipeline Runs Run Success Rate SLO Breach Flag

The `is_slo_threshold_over_30_days_breached` column indicates whether the over 30 days run success‑rate SLO was breached.  

| Value | Condition                                   | Meaning                                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_over_30_days < 0.99`          | `The over 30 days success‑rate target (≥=99%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_over_30_days >= 0.99`         | `The over 30 days success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_runtime_success_rate_in_seconds_slo_breached_for_the_day %}

## Daily Pipeline Runs Runtime Success Rate in Seconds SLO Breach Flag

The `is_slo_threshold_for_the_day_breached` column indicates whether the daily runtime success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                       |
|------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_for_the_day < 0.95`          | `The daily success‑rate target (≥=95%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_for_the_day >= 0.95`         | `The daily success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_runtime_success_rate_in_seconds_slo_breached_over_30_days %}

## Over 30 Days Pipeline Runs Runtime Success Rate in Seconds SLO Breach Flag

The `is_slo_threshold_over_30_days_breached` column indicates whether the over 30 days runtime success‑rate SLO was breached.  

| Value | Condition                                   | Meaning                                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_over_30_days < 0.99`          | `The over 30 days success‑rate target (≥=99%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_over_30_days >= 0.99`         | `The over 30 days success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs is_alert_threshold_for_the_day_breached %}

## Daily Total Pipeline Runs Alert Breach Flag

The `is_alert_threshold_for_the_day_breached` column indicates whether the daily execution count for a pipeline alert threshold was breached.

| Value | Condition                                   | Meaning                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `total_runs < avg_total_runs_over_30_days`  | `The daily execution count has fallen below the threshold; threshold alert considered breached.`                                        |
| FALSE | `total_runs >= avg_total_runs_over_30_days` | `The daily execution count is above threshold (>=avg_total_runs_over_30_days); threshold alert not breached.`                           |

{% enddocs %}
