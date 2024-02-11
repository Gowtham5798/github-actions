provider "google" {
  project     = "skipify-demo"                                    # Replace with your Google Cloud project ID
  region      = var.region                                     # Replace with your desired region
}

resource "google_cloud_run_service" "cloudrun-deidentify" {
  name     = var.name
  location = var.region

  template {
    spec {
      containers {
        image = var.image
        ports {
          container_port = var.container_port
        }
      }
    }
  }

  traffic {
    percent         = var.percent
    latest_revision = var.latest_revision
  }
}

# Create public access
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}
# Enable public access on Cloud Run service
resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.cloudrun-deidentify.location
  project     = google_cloud_run_service.cloudrun-deidentify.project
  service     = google_cloud_run_service.cloudrun-deidentify.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
# Return service URL
output "url" {
  value = google_cloud_run_service.cloudrun-deidentify.status[0].url
}
