################################################################################
#DEV
################################################################################

resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Identity pool for market analytics CI pipeline"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions Provider"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.owner"      = "assertion.repository_owner"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
    attribute_condition = "assertion.repository_owner == 'MayurCodes2508'"
}

resource "google_service_account_iam_member" "wif_binding" {
  service_account_id = "projects/instant-medium-491107-t6/serviceAccounts/github-workflows@instant-medium-491107-t6.iam.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/projects/144449440045/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/MayurCodes2508/market-analytics-platform"
  
  depends_on = [ 
    google_iam_workload_identity_pool.github_pool,
    google_iam_workload_identity_pool_provider.github_provider
   ]
}