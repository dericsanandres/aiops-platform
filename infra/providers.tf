terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "opentofu/google"
      version = "~> 5.0"
    }
  }

  # Local backend for MVP - switch to GCS for production
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
