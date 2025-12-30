output "service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.ai_processor.uri
}

output "artifact_registry_url" {
  description = "URL of the Artifact Registry repository"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.aiops.repository_id}"
}

output "service_account_email" {
  description = "Email of the Cloud Run service account"
  value       = google_service_account.cloud_run.email
}

output "webhook_url" {
  description = "Webhook URL for Alertmanager"
  value       = "${google_cloud_run_v2_service.ai_processor.uri}/webhook/alertmanager"
}
