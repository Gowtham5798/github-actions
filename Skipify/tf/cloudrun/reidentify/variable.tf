variable "project" {
  default = "skipify-demo"
}

variable "region" {
  default = "us-central1"
}

variable "name" {
  default = "cloudrun-srv-reidentify"
}

variable "image" {
  default = "gcr.io/skipify-demo/reidentify01"
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
