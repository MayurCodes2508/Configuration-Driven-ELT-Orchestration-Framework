################################################################################
#DEV
################################################################################


resource "google_workflows_workflow" "dev_framework_orchestrator" {
  name = "dev-framework-orchestrator"
  region = var.gcp_region
  description = "Dev Workflow for Framework Orchestration"
  service_account = "development-cloud-resource-860@instant-medium-491107-t6.iam.gserviceaccount.com"

  deletion_protection = false

  call_log_level = "LOG_ALL_CALLS"

  source_contents = templatefile("${path.module}/workflow.yml", {})
}

