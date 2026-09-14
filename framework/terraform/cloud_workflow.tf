################################################################################
#DEV
################################################################################

resource "google_workflows_workflow" "dev_orchestrator_workflow" {
  name = "dev-orchestrator-workflow"
  region = var.gcp_region
  description = "Development Workflow for Orchestration"
  service_account = "development-cloud-resource-860@instant-medium-491107-t6.iam.gserviceaccount.com"

  deletion_protection = false

  call_log_level = "LOG_ALL_CALLS"

  source_contents = templatefile("${path.module}/dev_workflow.yml", {})
}


################################################################################
#PROD
################################################################################

resource "google_workflows_workflow" "prod_orchestrator_workflow" {
  name = "prod-orchestrator-workflow"
  region = var.gcp_region
  description = "Production Workflow for Orchestration"
  service_account = "production-workflow@instant-medium-491107-t6.iam.gserviceaccount.com"

  deletion_protection = true

  lifecycle {
    prevent_destroy = true
  }

  call_log_level = "LOG_ALL_CALLS"

  source_contents = templatefile("${path.module}/prod_workflow.yml", {})
}