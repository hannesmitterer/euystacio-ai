# Terraform Variables for Protocollo Meta Salvage

variable "environment" {
  description = "Deployment environment (production, staging, development)"
  type        = string
  default     = "production"
  
  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Environment must be production, staging, or development."
  }
}

variable "region" {
  description = "Cloud provider region"
  type        = string
  default     = "us-east-1"
}

# Scaling Configuration
variable "autoscaling_config" {
  description = "Autoscaling configuration for services"
  type = object({
    enabled                         = bool
    min_replicas                    = number
    max_replicas                    = number
    target_cpu_utilization_percent  = number
    target_memory_utilization_percent = number
  })
  default = {
    enabled                         = true
    min_replicas                    = 2
    max_replicas                    = 10
    target_cpu_utilization_percent  = 70
    target_memory_utilization_percent = 80
  }
}

# Resource Limits
variable "resource_limits" {
  description = "Resource limits for containers"
  type = object({
    cpu_request    = string
    cpu_limit      = string
    memory_request = string
    memory_limit   = string
  })
  default = {
    cpu_request    = "500m"
    cpu_limit      = "2000m"
    memory_request = "512Mi"
    memory_limit   = "2Gi"
  }
}

# Monitoring Configuration
variable "monitoring_config" {
  description = "Monitoring and observability configuration"
  type = object({
    prometheus_retention_days = number
    prometheus_storage_size   = string
    grafana_admin_password    = string
    alertmanager_enabled      = bool
  })
  default = {
    prometheus_retention_days = 30
    prometheus_storage_size   = "50Gi"
    grafana_admin_password    = "changeme"  # Should be overridden
    alertmanager_enabled      = true
  }
  
  sensitive = true
}

# OPA Configuration
variable "opa_config" {
  description = "Open Policy Agent configuration"
  type = object({
    replicas           = number
    log_level          = string
    decision_log_enabled = bool
  })
  default = {
    replicas           = 3
    log_level          = "info"
    decision_log_enabled = true
  }
}

# Peace Bonds Configuration
variable "peace_bonds_config" {
  description = "Peace Bonds policy enforcement configuration"
  type = object({
    enabled                = bool
    risk_threshold_low     = number
    risk_threshold_medium  = number
    risk_threshold_high    = number
    adaptive_adjustment_rate = number
  })
  default = {
    enabled                = true
    risk_threshold_low     = 0.3
    risk_threshold_medium  = 0.6
    risk_threshold_high    = 0.8
    adaptive_adjustment_rate = 0.1
  }
}

# Tags
variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "Euystacio-AI"
    Component   = "Meta-Salvage"
    ManagedBy   = "Terraform"
    Environment = "production"
  }
}
