variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region for Cloud Run"
  type        = string
  default     = "us-central1"
}

variable "docker_username" {
  description = "Your Docker Hub username (where the image is hosted)"
  type        = string
}
