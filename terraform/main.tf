terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }
  required_version = ">= 1.0"
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

# Kubernetes Deployment (manages ReplicaSet)
resource "kubernetes_deployment" "fraud_detection" {
  metadata {
    name      = var.app_name
    namespace = var.namespace
    labels = {
      app     = var.app_name
      student = "arooj-fatima"
      sap     = "70148200"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.app_name
        }
      }

      spec {
        container {
          name              = "${var.app_name}-api"
          image             = "${var.image_name}:${var.image_tag}"
          image_pull_policy = "Never"

          port {
            container_port = var.container_port
          }

          resources {
            requests = {
              memory = "256Mi"
              cpu    = "250m"
            }
            limits = {
              memory = "512Mi"
              cpu    = "500m"
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = var.container_port
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }
        }
      }
    }
  }
}

# Kubernetes Service
resource "kubernetes_service" "fraud_detection_service" {
  metadata {
    name      = "${var.app_name}-service"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = var.app_name
    }

    type = "NodePort"

    port {
      port        = 80
      target_port = var.container_port
      node_port   = var.node_port
    }
  }
}
