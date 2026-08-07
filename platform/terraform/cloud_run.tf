################################################################################
#DEV
################################################################################

resource "google_cloud_run_v2_job" "dev_el_system_run" {
  name     = "dev-el-system-run"
  location = "asia-south1"
  deletion_protection = false
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:testing"
        args = [
          "el_system.orchestrator.main"
        ]
        env {
          name = "ENV"
          value = "DEV"
        }
        env {
          name = "DBT_TARGET"
          value = "dev"
        }
        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "dev-market-analytics-platform-coingecko-api-key-secret"
              version = "1"
            }
          }
        }
      }
      service_account = "development-cloud-resources-jo@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "dev_pipeline_run" {
  name = "dev-pipeline-run"
  location = "asia-south1"
  deletion_protection = false
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:testing"
        args = [
          "orchestrator.orchestrator.main"
        ]
         env {
          name = "TRIGGERED_BY"
          value = "scheduler"
         }
         env {
           name = "ENV"
           value = "DEV"
         }
         env {
          name = "DB_URL"
          value_source {
            secret_key_ref {
              secret  = "dev-market-analytics-platform-neon-db-url-secret"
              version = "1"
            }
          }
         }
      }
      service_account = "development-cloud-resource-860@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "dev_metadata_system_run" {
  name = "dev-metadata-system-run"
  location = "asia-south1"
  deletion_protection = false
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:testing"
        args = [
          "metadata_system.orchestrator.main"
        ]
         env {
          name = "ENV"
          value = "DEV"
          
         }
         env {
          name = "DBT_TARGET"
          value = "dev"
         }
         env {
          name = "NEON_DB_URL"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-neon-db-url-secret"
              version = "1"
            }
          }
         }
      }
      service_account = "development-cloud-resource-757@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

################################################################################
#PROD
################################################################################

resource "google_cloud_run_v2_job" "prod_el_system_run" {
  name     = "prod-el-system-run"
  location = "asia-south1"
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:latest"
        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-coingecko-api-key-secret"
              version = "1"
            }
          }
        }
        env {
          name = "ENV"
          value = "PROD"
        }
         env {
          name = "DBT_TARGET"
          value = "prod"
         }
      }
      service_account = "production-cloud-resources-job@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_pipeline_run" {
  name = "prod-pipeline-run"
  location = "asia-south1"
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:latest"
        env {
        name = "DB_URL"
        value_source {
          secret_key_ref {
            secret  = "prod-market-analytics-platform-neon-db-url-secret"
            version = "1"
            }
          }
        }
        env {
          name = "TRIGGERED_BY"
          value = "scheduler"
        }
        env {
          name = "ENV"
          value = "PROD"
        }
      }
      service_account = "production-cloud-resources-518@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_metadata_system_run" {
  name = "prod-metadata-system-run"
  location = "asia-south1"
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:latest"
         env {
          name = "ENV"
          value = "PROD"
          
         }
         env {
          name = "DBT_TARGET"
          value = "prod"
         }
         env {
          name = "NEON_DB_URL"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-neon-db-url-secret"
              version = "1"
            }
          }
         }
      }
      service_account = "production-cloud-resources-525@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}