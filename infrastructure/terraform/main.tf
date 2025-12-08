# Terraform Configuration for Protocollo Meta Salvage Infrastructure
# Manages cloud resources for monitoring, scaling, and policy enforcement

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  # Uncomment and configure for remote state storage
  # backend "s3" {
  #   bucket = "euystacio-terraform-state"
  #   key    = "meta-salvage/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

# Variables
variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
  default     = "euystacio-ai-cluster"
}

variable "namespace" {
  description = "Kubernetes namespace for deployments"
  type        = string
  default     = "euystacio-ai"
}

variable "monitoring_namespace" {
  description = "Kubernetes namespace for monitoring stack"
  type        = string
  default     = "monitoring"
}

variable "enable_autoscaling" {
  description = "Enable horizontal pod autoscaling"
  type        = bool
  default     = true
}

variable "min_replicas" {
  description = "Minimum number of pod replicas"
  type        = number
  default     = 2
}

variable "max_replicas" {
  description = "Maximum number of pod replicas"
  type        = number
  default     = 10
}

# Provider configuration
provider "kubernetes" {
  # Configure based on your Kubernetes setup
  # config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    # config_path = "~/.kube/config"
  }
}

# Create namespaces
resource "kubernetes_namespace" "euystacio_ai" {
  metadata {
    name = var.namespace
    labels = {
      name        = var.namespace
      environment = "production"
      managed-by  = "terraform"
    }
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = var.monitoring_namespace
    labels = {
      name        = var.monitoring_namespace
      environment = "production"
      managed-by  = "terraform"
    }
  }
}

# Prometheus Operator via Helm
resource "helm_release" "prometheus_operator" {
  name       = "prometheus-operator"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = kubernetes_namespace.monitoring.metadata[0].name
  version    = "52.0.0"

  values = [
    file("${path.module}/helm-values/prometheus-operator-values.yaml")
  ]

  set {
    name  = "prometheus.prometheusSpec.retention"
    value = "30d"
  }

  set {
    name  = "prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage"
    value = "50Gi"
  }
}

# Grafana configuration
resource "helm_release" "grafana" {
  name       = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "grafana"
  namespace  = kubernetes_namespace.monitoring.metadata[0].name
  version    = "7.0.0"

  values = [
    file("${path.module}/helm-values/grafana-values.yaml")
  ]

  depends_on = [helm_release.prometheus_operator]
}

# Open Policy Agent (OPA)
resource "helm_release" "opa" {
  name       = "opa"
  repository = "https://open-policy-agent.github.io/kube-mgmt/charts"
  chart      = "opa"
  namespace  = kubernetes_namespace.euystacio_ai.metadata[0].name
  version    = "1.8.0"

  set {
    name  = "replicas"
    value = "3"
  }

  set {
    name  = "opa.logLevel"
    value = "info"
  }
}

# ConfigMap for Prometheus configuration
resource "kubernetes_config_map" "prometheus_config" {
  metadata {
    name      = "prometheus-config"
    namespace = kubernetes_namespace.monitoring.metadata[0].name
  }

  data = {
    "prometheus.yml" = file("${path.module}/../../monitoring/prometheus/prometheus.yml")
    "rules.yml"      = file("${path.module}/../../monitoring/prometheus/rules.yml")
  }
}

# ConfigMap for Grafana dashboards
resource "kubernetes_config_map" "grafana_dashboards" {
  metadata {
    name      = "grafana-dashboards"
    namespace = kubernetes_namespace.monitoring.metadata[0].name
    labels = {
      grafana_dashboard = "1"
    }
  }

  data = {
    "meta-salvage-overview.json" = file("${path.module}/../../monitoring/grafana/dashboards/meta-salvage-overview.json")
  }
}

# Outputs
output "namespaces" {
  description = "Created Kubernetes namespaces"
  value = {
    euystacio_ai = kubernetes_namespace.euystacio_ai.metadata[0].name
    monitoring   = kubernetes_namespace.monitoring.metadata[0].name
  }
}

output "monitoring_stack" {
  description = "Monitoring stack deployment status"
  value = {
    prometheus = helm_release.prometheus_operator.status
    grafana    = helm_release.grafana.status
  }
}

output "opa_status" {
  description = "OPA deployment status"
  value       = helm_release.opa.status
}
