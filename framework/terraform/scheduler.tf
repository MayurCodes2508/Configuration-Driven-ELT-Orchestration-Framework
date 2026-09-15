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
    google_workflows_workflow.prod_orchestrator_workflow
   ]

  retry_config {
    retry_count          = 3
    max_retry_duration   = "3600s"
    min_backoff_duration = "5s"
    max_backoff_duration = "3600s"
    max_doublings        = 5
  }

  http_target {
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/instant-medium-491107-t6/locations/asia-south1/workflows/prod-orchestrator-workflow/executions"
    http_method = "POST"

    oauth_token {
      service_account_email = "production-cloud-resources-sch@instant-medium-491107-t6.iam.gserviceaccount.com"
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}

