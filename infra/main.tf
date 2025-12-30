# =============================================================================
# ARTIFACT REGISTRY
# =============================================================================

resource "google_artifact_registry_repository" "aiops" {
  location      = var.region
  repository_id = "aiops-platform"
  description   = "Docker repository for AIOps platform"
  format        = "DOCKER"
}

# =============================================================================
# CLOUD RUN SERVICE
# =============================================================================

resource "google_cloud_run_v2_service" "ai_processor" {
  name     = var.service_name
  location = var.region

  template {
    # Scale to zero for free tier
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      # Use placeholder if no image provided yet
      image = var.container_image != "" ? var.container_image : "gcr.io/cloudrun/placeholder"

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      env {
        name  = "LOG_LEVEL"
        value = "INFO"
      }

      # OpenAI API key from Secret Manager (when configured)
      dynamic "env" {
        for_each = var.openai_api_key != "" ? [1] : []
        content {
          name = "OPENAI_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.openai_key[0].secret_id
              version = "latest"
            }
          }
        }
      }

      # Startup probe
      startup_probe {
        http_get {
          path = "/health"
          port = 8000
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }

      # Liveness probe
      liveness_probe {
        http_get {
          path = "/health"
          port = 8000
        }
        period_seconds = 30
      }
    }

    # Service account
    service_account = google_service_account.cloud_run.email
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }

  depends_on = [
    google_artifact_registry_repository.aiops
  ]
}

# =============================================================================
# IAM - Allow unauthenticated access (for webhook)
# =============================================================================

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.ai_processor.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# =============================================================================
# SERVICE ACCOUNT
# =============================================================================

resource "google_service_account" "cloud_run" {
  account_id   = "aiops-processor-sa"
  display_name = "AIOps Processor Service Account"
}

# Grant Secret Manager access
resource "google_project_iam_member" "secret_access" {
  count   = var.openai_api_key != "" ? 1 : 0
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# =============================================================================
# SECRET MANAGER (for API keys)
# =============================================================================

resource "google_secret_manager_secret" "openai_key" {
  count     = var.openai_api_key != "" ? 1 : 0
  secret_id = "openai-api-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "openai_key" {
  count       = var.openai_api_key != "" ? 1 : 0
  secret      = google_secret_manager_secret.openai_key[0].id
  secret_data = var.openai_api_key
}
