################################################################################
#DEV
################################################################################

resource "google_secret_manager_secret" "dev_configuration_driven_elt_orchestration_framework_coingecko_api_key_secrets" {
  secret_id = "dev-configuration-driven-elt-orchestration-framework-coingecko-api-key-secret"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "dev_configuration_driven_elt_orchestration_framework_neon_db_url_secrets" {
  secret_id = "dev-configuration-driven-elt-orchestration-framework-neon-db-url-secret"

  replication {
    auto {}
  }
}

################################################################################
#PROD
################################################################################

resource "google_secret_manager_secret" "prod_market_analytics_platform_coingecko_api_keysecrets" {
  secret_id = "prod-market-analytics-platform-coingecko-api-key-secret"

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }

  deletion_protection = true
}

resource "google_secret_manager_secret" "prod_market_analytics_platform_neon_db_url_secrets" {
  secret_id = "prod-market-analytics-platform-neon-db-url-secret"

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }

  deletion_protection = true
}

resource "google_secret_manager_secret" "prod_configuration_driven_elt_orchestration_framework_coingecko_api_key_secrets" {
  secret_id = "prod-configuration-driven-elt-orchestration-framework-coingecko-api-key-secret"

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }

  deletion_protection = true
}

resource "google_secret_manager_secret" "prod_configuration_driven_elt_orchestration_framework_neon_db_url_secrets" {
  secret_id = "prod-configuration-driven-elt-orchestration-framework-neon-db-url-secret"

lifecycle {
  prevent_destroy = true
}
  replication {
    auto {}
  }

  deletion_protection = true
}