variable "app_name" {
  description = "Application name for fraud detection system"
  default     = "fraud-detection"
}

variable "namespace" {
  description = "Kubernetes namespace"
  default     = "default"
}

variable "replicas" {
  description = "Number of pod replicas for high availability"
  default     = 3
}

variable "image_name" {
  description = "Docker image name"
  default     = "fraud-detection-api"
}

variable "image_tag" {
  description = "Docker image tag"
  default     = "v1.0"
}

variable "container_port" {
  description = "Container port for the FastAPI app"
  default     = 8000
}

variable "node_port" {
  description = "NodePort for external access"
  default     = 30080
}
