terraform {
  backend "gcs" {
    bucket = "cloudrun-backend"
    prefix = "terraform/state"
  }
}
