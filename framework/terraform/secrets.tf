################################################################################
#DEV
################################################################################

resource "google_secret_manager_secret" "dev_coingecko_api_key_secret" {
  secret_id = "dev-coingecko-api-key-secret"

  deletion_protection = false

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "dev_neon_db_url_secret" {
  secret_id = "dev-neon-db-url-secret"

  deletion_protection = false

  replication {
    auto {}
  }
}

################################################################################
#PROD
################################################################################

resource "google_secret_manager_secret" "prod_neon_db_url_secret" {
  secret_id = "prod-neon-db-url-secret"

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }

  deletion_protection = true
}

resource "google_secret_manager_secret" "prod_coingecko_api_key_secret" {
  secret_id = "prod-coingecko-api-key-secret"

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }

  deletion_protection = true
}
