terraform {
  required_version = ">= 0.14"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

# Enable necessary APIs.
resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
}

resource "google_project_service" "cloud_build" {
  service = "cloudbuild.googleapis.com"
}

# Deploy the Docker image to Cloud Run.
resource "google_cloud_run_service" "default" {
  name     = "notstuck-app"
  location = var.region

  template {
    spec {
      containers {
        image = "docker.io/${var.docker_username}/notstuck:latest"

        # Inject secret environment variables.
        env {
          name = "OPENAI_API_KEY"
          value_source {
            secret_key_ref {
              name = "openai-api-key"   # Must match the secret ID in Secret Manager.
              key  = "latest"           # Uses the latest version.
            }
          }
        }
        env {
          name = "PINECONE_API_KEY"
          value_source {
            secret_key_ref {
              name = "pinecone-api-key"
              key  = "latest"
            }
          }
        }
        env {
          name = "PINECONE_ENV"
          value_source {
            secret_key_ref {
              name = "pinecone-env"
              key  = "latest"
            }
          }
        }
        env {
          name = "PINECONE_INDEX_NAME"
          value_source {
            secret_key_ref {
              name = "pinecone-index-name"
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

# Allow public (unauthenticated) access to the Cloud Run service.
resource "google_cloud_run_service_iam_member" "noauth" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_service.default.status[0].url
}
