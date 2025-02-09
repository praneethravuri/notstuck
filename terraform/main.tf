resource "google_cloud_run_service" "default" {
  name     = "notstuck-app"
  location = var.region

  template {
    spec {
      containers {
        image = "docker.io/${var.docker_username}/notstuck:latest"

        # Inject secret environment variables using the correct block name.
        env {
          name = "OPENAI_API_KEY"
          value_from {
            secret_key_ref {
              name = "openai-api-key"   # Must match the secret ID in Secret Manager.
              key  = "latest"           # Uses the latest version.
            }
          }
        }

        env {
          name = "PINECONE_API_KEY"
          value_from {
            secret_key_ref {
              name = "pinecone-api-key"
              key  = "latest"
            }
          }
        }

        env {
          name = "PINECONE_ENV"
          value_from {
            secret_key_ref {
              name = "pinecone-env"
              key  = "latest"
            }
          }
        }

        env {
          name = "PINECONE_INDEX_NAME"
          value_from {
            secret_key_ref {
              name = "pinecone-index-name"
              key  = "latest"
            }
          }
        }
      }
    }
  }

  // Use the correct block name "traffic" for routing configuration.
  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}
