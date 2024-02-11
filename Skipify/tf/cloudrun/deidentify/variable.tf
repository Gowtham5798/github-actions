variable "project" {
  default = "stovlsandboxnew-399705"
}

variable "region" {
  default = "us-central1"
}

variable "name" {
  default = "cloudrun-srv-deidentify"
}

variable "image" {
  default = "gcr.io/stovlsandboxnew-399705/firstgowtham"
}

variable "container_port" {
  default = "5000"
}

variable "percent" {
  default = "100"
}

variable "latest_revision" {
  default = "true"
}
