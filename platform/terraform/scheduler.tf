################################################################################
#PROD
################################################################################

resource "google_cloud_scheduler_job" "prod_pipeline_run_scheduler" {
  name      = "prod-pipeline-run-scheduler"
  region    = "asia-south1"
  schedule  = "0 * * * *"
  time_zone = "Asia/Kolkata"
  lifecycle {
    prevent_destroy = true
  }
  depends_on = [ 
    google_cloud_run_v2_job.prod_pipeline_run
   ]

  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = "https://asia-south1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/instant-medium-491107-t6/jobs/prod-pipeline-run:run"
    http_method = "POST"

    oauth_token {
      service_account_email = "production-cloud-resources-sch@instant-medium-491107-t6.iam.gserviceaccount.com"
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}

