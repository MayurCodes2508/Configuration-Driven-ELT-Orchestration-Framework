################################################################################
#DEV
################################################################################

resource "google_storage_bucket" "dev_configuration_driven_elt_orchestration_framework_bucket" {
  name                     = "dev-configuration-driven-elt-orchestration-framework-bucket"
  location                 = "asia-south1"
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"
  force_destroy            = true

  soft_delete_policy {
    retention_duration_seconds = 0
  }
}

################################################################################
#PROD
################################################################################

resource "google_storage_bucket" "prod_market_analytics_platform_bucket" {
  name                     = "prod-market-analytics-platform-bucket"
  location                 = "asia-south1"
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"

  lifecycle {
    prevent_destroy = true
  }

  soft_delete_policy {
    retention_duration_seconds = 604800
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      age = 90
    }
  }
}