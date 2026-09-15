################################################################################
#DEV
################################################################################

################################################################################
#JOBS
################################################################################

resource "google_cloud_run_v2_job" "dev_execution_job" {
  name = "dev-execution-job"
  project = var.gcp_project_id
  location = var.gcp_region
  
  deletion_protection = false

  template {
    template {
      max_retries = 2
      timeout = "300s"

      service_account = "development-cloud-resources-jo@instant-medium-491107-t6.iam.gserviceaccount.com"

      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:testing"
        command = [ "python", "-u", "-m", "elt_system.orchestrator.main" ]
      }
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
      env {
        name = "triggeredBy"
        value = "scheduler"
      }
    }
    
  }
}


################################################################################
#PROD
################################################################################

################################################################################
#JOBS
################################################################################

resource "google_cloud_run_v2_job" "prod_execution_job" {
  name     = "prod-execution-job"
  location = var.gcp_region
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  template {
    template {
      max_retries = 2
      timeout = "300s"

      service_account = "production-run-job@instant-medium-491107-t6.iam.gserviceaccount.com"

      containers {
        image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:latest"
        command = [ "python", "-u", "-m", "elt_system.orchestrator.main" ]
      }
    }
  }
}

################################################################################
#SERVICES
################################################################################

resource "google_cloud_run_v2_service" "prod_execution_service" {
  name = "prod-execution-service"
  project = var.gcp_project_id
  location = var.gcp_region
  description = "Production Execution Run Service"
  client = "terraform"

  deletion_protection = true

  lifecycle {
    prevent_destroy = true
  }

  scaling {
    min_instance_count = 0
  }

  template {
    timeout = "60s"

    service_account = "production-run-service@instant-medium-491107-t6.iam.gserviceaccount.com"
    
    containers {
      image = "asia-south1-docker.pkg.dev/instant-medium-491107-t6/configuration-driven-elt-orchestration-framework-repository/framework:latest"
      env {
        name = "triggeredBy"
        value = "scheduler"
      }
    }
    
  }
}
