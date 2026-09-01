################################################################################
#DEV
################################################################################

################################################################################
#JOBS
################################################################################


resource "google_cloud_run_v2_job" "dev_elt_system_run" {
  name     = "dev-elt-system-run"
  location = var.gcp_region
  deletion_protection = false
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:testing"
      }
      service_account = "development-cloud-resources-jo@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "dev_metadata_system_run" {
  name = "dev-metadata-system-run"
  location = var.gcp_region
  deletion_protection = false
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:testing"
      }
      service_account = "development-cloud-resource-757@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

################################################################################
#SERVICES
################################################################################

resource "google_cloud_run_v2_service" "dev_execution_service" {
  name = "dev-execution-service"
  project = var.gcp_project_id
  location = var.gcp_region
  description = "Development Execution Run Service"
  client = "terraform"

  deletion_protection = false

  scaling {
    min_instance_count = 0
  }

  template {
    timeout = "60s"

    service_account = "development-logger-run-job@instant-medium-491107-t6.iam.gserviceaccount.com"
    
    containers {
      image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:testing"
    }
    
  }
}


################################################################################
#PROD
################################################################################

################################################################################
#JOBS
################################################################################

resource "google_cloud_run_v2_job" "prod_el_system_run" {
  name     = "prod-el-system-run"
  location = var.gcp_region
  deletion_protection = false
  lifecycle {
    prevent_destroy = false
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/market-analytics-platform-repository/platform-job:latest"
        args = [
          "el_system.orchestrator.main"
        ]
        env {
          name = "ENV"
          value = "PROD"
        }
         env {
          name = "DBT_TARGET"
          value = "prod"
         }
        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "prod-market-analytics-platform-coingecko-api-key-secret"
              version = "1"
            }
          }
        }
      }
      service_account = "production-cloud-resources-job@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_elt_system_run" {
  name     = "prod-elt-system-run"
  location = var.gcp_region
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:latest"
        args = [
          "elt_system.orchestrator.main"
        ]
        env {
          name = "ENV"
          value = "PROD"
        }
         env {
          name = "DBT_TARGET"
          value = "prod"
         }
        env {
          name = "COINGECKO_API_KEY"
          value_source {
            secret_key_ref {
              secret  = "prod-configuration-driven-elt-orchestration-framework-coingecko-api-key-secret"
              version = "1"
            }
          }
        }
      }
      service_account = "production-cloud-resources-job@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_pipeline_run" {
  name = "prod-pipeline-run"
  location = var.gcp_region
  deletion_protection = false
  lifecycle {
    prevent_destroy = false
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:latest"
        args = [
          "orchestrator.orchestrator.main"
        ]
        env {
          name = "TRIGGERED_BY"
          value = "scheduler"
        }
        env {
          name = "ENV"
          value = "PROD"
        }
        env {
        name = "DB_URL"
        value_source {
          secret_key_ref {
            secret  = "prod-configuration-driven-elt-orchestration-framework-neon-db-url-secret"
            version = "1"
            }
          }
        }
      }
      service_account = "production-cloud-resources-518@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

resource "google_cloud_run_v2_job" "prod_metadata_system_run" {
  name = "prod-metadata-system-run"
  location = var.gcp_region
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "600s"
      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:latest"
        args = [
          "metadata_system.orchestrator.main"
        ]
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
              secret  = "prod-configuration-driven-elt-orchestration-framework-neon-db-url-secret"
              version = "1"
            }
          }
         }
      }
      service_account = "production-cloud-resources-525@instant-medium-491107-t6.iam.gserviceaccount.com"
    }
  }
}

################################################################################
#SERVICES
################################################################################