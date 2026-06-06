output "deployment_name" {
  description = "Name of the Kubernetes deployment"
  value       = kubernetes_deployment.fraud_detection.metadata[0].name
}

output "service_name" {
  description = "Name of the Kubernetes service"
  value       = kubernetes_service.fraud_detection_service.metadata[0].name
}

output "replicas" {
  description = "Number of running replicas"
  value       = kubernetes_deployment.fraud_detection.spec[0].replicas
}

output "api_port" {
  description = "API NodePort"
  value       = var.node_port
}
