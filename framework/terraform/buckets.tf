################################################################################
#DEV
################################################################################

resource "google_storage_bucket" "dev_market_analytics_platform_bucket" {
  name                     = "dev-market-analytics-platform-bucket"
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