variable "project" {
  default = "skipify-demo"
}

variable "region" {
  default = "us-central1"
}

variable "name" {
  default = "cloudrun-srv-deidentify"
}

variable "image" {
  default = "gcr.io/skipify-demo/my-cloudrun02"
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
