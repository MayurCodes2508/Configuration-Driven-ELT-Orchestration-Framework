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