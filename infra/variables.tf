variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region (us-central1 for free tier)"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "aiops-processor"
}

variable "container_image" {
  description = "Container image to deploy"
  type        = string
  default     = ""
}

variable "openai_api_key" {
  description = "OpenAI API Key (stored in Secret Manager)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "min_instances" {
  description = "Minimum number of instances (0 for scale-to-zero)"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 2
}
