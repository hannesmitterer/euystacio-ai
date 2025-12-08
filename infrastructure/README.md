# Infrastructure - Protocollo Meta Salvage

This directory contains Infrastructure as Code (IaC) configurations for deploying and managing the Protocollo Meta Salvage system.

## Directory Structure

```
infrastructure/
├── terraform/           # Terraform configurations
│   ├── main.tf         # Main Terraform configuration
│   └── variables.tf    # Variable definitions
├── kubernetes/         # Kubernetes manifests
│   ├── euystacio-deployment.yaml    # Core application deployment
│   └── opa-peace-bonds.yaml        # OPA policy enforcement
└── README.md
```

## Overview

The infrastructure supports:
- **Kubernetes Orchestration**: Container orchestration and management
- **Horizontal Pod Autoscaling**: Dynamic scaling based on metrics
- **Prometheus & Grafana**: Monitoring and observability
- **Open Policy Agent**: Policy-as-code enforcement
- **Terraform Management**: Infrastructure as code

## Quick Start

### Deploy with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply configuration
terraform apply
```

### Deploy with Kubernetes

```bash
# Create namespaces
kubectl create namespace euystacio-ai
kubectl create namespace monitoring

# Deploy application
kubectl apply -f kubernetes/euystacio-deployment.yaml

# Deploy OPA
kubectl apply -f kubernetes/opa-peace-bonds.yaml

# Verify deployments
kubectl get all -n euystacio-ai
```

## Terraform Configuration

### Resources Created

The Terraform configuration creates:

1. **Kubernetes Namespaces**
   - `euystacio-ai`: Application namespace
   - `monitoring`: Monitoring stack namespace

2. **Helm Releases**
   - Prometheus Operator (kube-prometheus-stack)
   - Grafana
   - Open Policy Agent (OPA)

3. **ConfigMaps**
   - Prometheus configuration
   - Grafana dashboards
   - OPA policies

### Variables

Key variables that can be customized:

| Variable | Description | Default |
|----------|-------------|---------|
| `cluster_name` | Kubernetes cluster name | `euystacio-ai-cluster` |
| `namespace` | Application namespace | `euystacio-ai` |
| `monitoring_namespace` | Monitoring namespace | `monitoring` |
| `enable_autoscaling` | Enable HPA | `true` |
| `min_replicas` | Minimum pod replicas | `2` |
| `max_replicas` | Maximum pod replicas | `10` |

### Customization

Create a `terraform.tfvars` file:

```hcl
cluster_name = "my-cluster"
namespace = "euystacio-ai"

autoscaling_config = {
  enabled                         = true
  min_replicas                    = 3
  max_replicas                    = 15
  target_cpu_utilization_percent  = 70
  target_memory_utilization_percent = 80
}

resource_limits = {
  cpu_request    = "1000m"
  cpu_limit      = "4000m"
  memory_request = "1Gi"
  memory_limit   = "4Gi"
}
```

## Kubernetes Manifests

### Euystacio Deployment

The main application deployment includes:

- **Deployment**: 3 replicas of the Euystacio API
- **Service**: ClusterIP service exposing ports 8000 (HTTP) and 9090 (metrics)
- **HPA**: Horizontal Pod Autoscaler with multiple metrics

#### Autoscaling Metrics

The HPA scales based on:
1. **CPU**: Target 70% utilization
2. **Memory**: Target 80% utilization
3. **Symbiosis Score**: Custom metric (target: 0.5)

#### Resource Configuration

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### OPA Peace Bonds

The OPA deployment provides:

- **3 Replicas**: For high availability
- **Policy ConfigMap**: Peace Bonds policy definitions
- **Service**: Exposes OPA on port 8181

#### Policy Structure

Two main policies:
1. **peace-bonds.rego**: Core risk evaluation and enforcement
2. **adaptive-enforcement.rego**: Dynamic threshold adjustment

## Scaling Strategies

### Horizontal Pod Autoscaling

Automatic scaling based on:
- CPU and memory utilization
- Custom metrics (Symbiosis Score)
- Configurable min/max replicas

### Vertical Scaling

Adjust resource limits:

```bash
kubectl set resources deployment euystacio-api \
  --requests=cpu=1000m,memory=1Gi \
  --limits=cpu=4000m,memory=4Gi \
  -n euystacio-ai
```

### Cluster Autoscaling

For node-level scaling, configure cluster autoscaler in your cloud provider:

```bash
# Example for GKE
gcloud container clusters update euystacio-ai-cluster \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10
```

## Monitoring Integration

### Prometheus Configuration

The Terraform deployment automatically configures Prometheus to scrape:
- Application metrics from `/metrics`
- Symbiosis metrics from `/api/metrics/symbiosis`
- Threshold metrics from `/api/metrics/thresholds`
- OPA metrics from OPA service

### Grafana Dashboards

Dashboards are provisioned automatically:
- Meta Salvage Overview
- System Health
- Peace Bonds Enforcement

Access Grafana:

```bash
kubectl port-forward -n monitoring svc/grafana 3000:80
# Open http://localhost:3000
```

## Security Considerations

### Network Policies

Apply network policies to restrict traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: euystacio-api-policy
  namespace: euystacio-ai
spec:
  podSelector:
    matchLabels:
      app: euystacio-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: ingress-controller
```

### Secrets Management

Store sensitive data in Kubernetes Secrets:

```bash
kubectl create secret generic euystacio-secrets \
  --from-literal=api-key=<your-key> \
  --from-literal=db-password=<your-password> \
  -n euystacio-ai
```

### RBAC

Implement Role-Based Access Control:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: euystacio-role
  namespace: euystacio-ai
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

## Disaster Recovery

### Backup

Regular backups of:
- Kubernetes resources
- Prometheus data
- Grafana dashboards
- OPA policies

```bash
# Backup script
./scripts/backup-infrastructure.sh
```

### Restoration

Restore from backup:

```bash
# Restore Kubernetes resources
kubectl apply -f backup/kubernetes-resources.yaml

# Restore Prometheus data
# See monitoring/README.md for details
```

## Troubleshooting

### Common Issues

#### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n euystacio-ai

# Check logs
kubectl logs <pod-name> -n euystacio-ai
```

#### HPA Not Scaling

```bash
# Check HPA status
kubectl describe hpa euystacio-api-hpa -n euystacio-ai

# Verify metrics server
kubectl top nodes
kubectl top pods -n euystacio-ai
```

#### OPA Policy Errors

```bash
# Check OPA logs
kubectl logs deployment/opa-peace-bonds -n euystacio-ai

# Validate policy
opa test infrastructure/kubernetes/opa-peace-bonds.yaml
```

### Resource Constraints

If experiencing resource issues:

1. Check node resources:
   ```bash
   kubectl top nodes
   ```

2. Review pod resource usage:
   ```bash
   kubectl top pods -n euystacio-ai --sort-by=memory
   ```

3. Adjust resource limits or scale nodes

## Cost Optimization

### Resource Right-Sizing

Monitor actual resource usage and adjust:

```bash
# Check resource usage over time in Prometheus
# Query: avg_over_time(container_cpu_usage_seconds_total[24h])
```

### Autoscaling Policies

Tune autoscaling to match your workload:
- Adjust target utilization percentages
- Set appropriate min/max replicas
- Use cluster autoscaling for node optimization

### Development vs. Production

Use different configurations:

```bash
# Development (smaller resources)
terraform apply -var-file=dev.tfvars

# Production (production resources)
terraform apply -var-file=prod.tfvars
```

## Maintenance

### Regular Tasks

1. **Update Helm Charts**:
   ```bash
   helm repo update
   helm upgrade prometheus-operator prometheus-community/kube-prometheus-stack -n monitoring
   ```

2. **Rotate Secrets**:
   ```bash
   kubectl create secret generic euystacio-secrets \
     --from-literal=api-key=<new-key> \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

3. **Review Resource Usage**:
   - Check Grafana dashboards
   - Review Prometheus metrics
   - Adjust HPA settings if needed

4. **Update Policies**:
   ```bash
   kubectl apply -f kubernetes/opa-peace-bonds.yaml
   ```

## Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [OPA Documentation](https://www.openpolicyagent.org/docs/)

## Support

For infrastructure issues:
1. Check [Runbooks](../docs/RUNBOOKS.md)
2. Review [Developer Guide](../docs/DEVELOPER_GUIDE.md)
3. Open GitHub issue with details

---

*Last Updated: 2025-12-08*
*Version: 1.0*
