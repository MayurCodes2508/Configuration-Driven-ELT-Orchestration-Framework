################################################################################
#SHARED
################################################################################

resource "google_artifact_registry_repository" "dev_configuration_driven_elt_orchestration_framework_repo" {
  repository_id = "configuration-driven-elt-orchestration-framework-repository"
  format        = "DOCKER"
  location      = "asia-south1"
  project       = "instant-medium-491107-t6"
  lifecycle {
    prevent_destroy = true
  }
}