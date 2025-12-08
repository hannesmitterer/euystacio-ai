# Protocollo Meta Salvage - Operational Runbooks

## Table of Contents
1. [System Health Checks](#system-health-checks)
2. [Alert Response](#alert-response)
3. [Deployment Procedures](#deployment-procedures)
4. [Incident Response](#incident-response)
5. [Scaling Operations](#scaling-operations)
6. [Backup and Recovery](#backup-and-recovery)

## System Health Checks

### Daily Health Check

Run this daily to verify system status:

```bash
#!/bin/bash
# Daily health check script

echo "=== Euystacio AI Health Check ==="
echo "Date: $(date)"
echo ""

# Check Kubernetes pods
echo "1. Pod Status:"
kubectl get pods -n euystacio-ai
echo ""

# Check metrics
echo "2. Current Metrics:"
curl -s http://euystacio-api:8000/api/metrics/thresholds | jq '.metrics'
echo ""

# Check OPA status
echo "3. OPA Policy Status:"
kubectl get pods -n euystacio-ai -l app=opa-peace-bonds
echo ""

# Check recent alerts
echo "4. Recent Alerts:"
curl -s http://prometheus:9090/api/v1/alerts | jq '.data.alerts[] | select(.state=="firing")'
echo ""

echo "✓ Health check complete"
```

### Metric Thresholds

#### Critical Thresholds
- **QEK**: Must be ≥ 0.85 (ideal: 0.938)
- **H-VAR**: Must be ≤ 0.10 (ideal: 0.043)
- **Ethisches Ideal**: Must be ≥ 0.95 (ideal: 1.0)
- **Symbiosis Score**: Must be ≥ 0.5

#### Warning Thresholds
- **QEK**: < 0.88
- **H-VAR**: > 0.08
- **Ethisches Ideal**: < 0.97
- **Symbiosis Score**: < 0.6

## Alert Response

### High Priority Alerts

#### QEK Below Minimum Threshold

**Alert**: `QEK below minimum threshold: 0.82 < 0.85`

**Impact**: Core ethical kernel not meeting standards

**Response Steps**:
1. Check recent changes:
   ```bash
   kubectl logs -n euystacio-ai deployment/euystacio-api --tail=100
   ```

2. Verify input data quality:
   ```bash
   curl http://euystacio-api:8000/api/metrics/qek/details
   ```

3. Review red_code.json integrity:
   ```bash
   python -c "import json; print(json.load(open('red_code.json')))"
   ```

4. If issue persists > 15 minutes:
   - Notify on-call team
   - Consider rolling back recent changes
   - Document in incident log

#### H-VAR Exceeded Maximum

**Alert**: `H-VAR exceeded maximum threshold: 0.12 > 0.10`

**Impact**: High volatility detected in ethical metrics

**Response Steps**:
1. Check for unusual activity:
   ```bash
   # Check request rates
   curl http://prometheus:9090/api/v1/query?query=rate(http_requests_total[5m])
   ```

2. Review recent risk events:
   ```bash
   curl http://euystacio-api:8000/api/metrics/risk/events?limit=50
   ```

3. Verify system resources:
   ```bash
   kubectl top pods -n euystacio-ai
   kubectl top nodes
   ```

4. If caused by legitimate traffic spike:
   - Monitor for stabilization
   - Consider scaling up resources

5. If caused by anomalous behavior:
   - Investigate root cause
   - Apply Peace Bonds restrictions if needed

#### Peace Bonds Policy Violation

**Alert**: `High risk provider detected: risk_score=0.85`

**Impact**: Provider attempting access with high risk profile

**Response Steps**:
1. Review violation details:
   ```bash
   kubectl logs -n euystacio-ai deployment/opa-peace-bonds --tail=50 | grep "deny"
   ```

2. Check provider credentials:
   ```bash
   # Query provider risk attributes
   curl http://euystacio-api:8000/api/providers/{provider_id}/risk
   ```

3. Determine if violation is legitimate:
   - Review provider history
   - Check for false positives
   - Verify risk calculation

4. Take action:
   - If legitimate threat: Maintain block
   - If false positive: Adjust policy thresholds
   - Document decision

### Medium Priority Alerts

#### High CPU Usage

**Alert**: `CPU usage is above 80% for more than 10 minutes`

**Response Steps**:
1. Identify resource-intensive pods:
   ```bash
   kubectl top pods -n euystacio-ai --sort-by=cpu
   ```

2. Check if autoscaling is working:
   ```bash
   kubectl get hpa -n euystacio-ai
   ```

3. If autoscaling at max replicas:
   - Review current load patterns
   - Consider increasing max_replicas
   - Optimize resource-intensive operations

4. Temporary mitigation:
   ```bash
   # Manually scale up
   kubectl scale deployment euystacio-api --replicas=8 -n euystacio-ai
   ```

#### High Memory Usage

**Alert**: `Memory usage is above 85% for more than 10 minutes`

**Response Steps**:
1. Check memory usage by pod:
   ```bash
   kubectl top pods -n euystacio-ai --sort-by=memory
   ```

2. Check for memory leaks:
   ```bash
   kubectl logs -n euystacio-ai deployment/euystacio-api | grep -i "memory\|oom"
   ```

3. If memory leak suspected:
   - Restart affected pods
   - Investigate application code
   - Consider adding memory limits

## Deployment Procedures

### Standard Deployment

1. **Pre-deployment checks**:
   ```bash
   # Run tests
   pytest -v
   
   # Verify configuration
   kubectl diff -f infrastructure/kubernetes/
   ```

2. **Deploy**:
   ```bash
   # Apply Kubernetes manifests
   kubectl apply -f infrastructure/kubernetes/euystacio-deployment.yaml
   
   # Watch rollout
   kubectl rollout status deployment/euystacio-api -n euystacio-ai
   ```

3. **Post-deployment verification**:
   ```bash
   # Check pod status
   kubectl get pods -n euystacio-ai
   
   # Verify metrics
   curl http://euystacio-api:8000/health
   
   # Monitor for 15 minutes
   watch -n 30 'kubectl get pods -n euystacio-ai'
   ```

### Emergency Rollback

If deployment causes issues:

```bash
# Quick rollback
kubectl rollout undo deployment/euystacio-api -n euystacio-ai

# Verify rollback
kubectl rollout status deployment/euystacio-api -n euystacio-ai

# Check health
curl http://euystacio-api:8000/health
```

### Blue-Green Deployment

For zero-downtime deployments:

```bash
# Deploy new version (green)
kubectl apply -f infrastructure/kubernetes/euystacio-deployment-green.yaml

# Verify green deployment
kubectl get pods -n euystacio-ai -l version=green

# Switch traffic
kubectl patch service euystacio-api -n euystacio-ai -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for issues
# If problems, switch back to blue
kubectl patch service euystacio-api -n euystacio-ai -p '{"spec":{"selector":{"version":"blue"}}}'
```

## Incident Response

### Severity Levels

**P0 - Critical**: System down, data loss, security breach
**P1 - High**: Significant degradation, multiple alerts
**P2 - Medium**: Partial degradation, isolated issues
**P3 - Low**: Minor issues, no user impact

### P0 - Critical Incident

1. **Immediate Actions** (0-5 minutes):
   - Alert on-call team
   - Create incident channel
   - Begin incident log
   - Assess blast radius

2. **Triage** (5-15 minutes):
   - Identify root cause
   - Implement immediate mitigation
   - Update stakeholders

3. **Resolution** (15-60 minutes):
   - Apply fix
   - Verify system recovery
   - Monitor for stability

4. **Post-Incident** (24-48 hours):
   - Complete incident report
   - Conduct post-mortem
   - Implement preventive measures

### Incident Response Commands

```bash
# Gather diagnostic information
./scripts/gather-diagnostics.sh

# Check all service health
kubectl get all -n euystacio-ai
kubectl get all -n monitoring

# Export logs
kubectl logs -n euystacio-ai deployment/euystacio-api --all-containers > incident-logs.txt

# Check events
kubectl get events -n euystacio-ai --sort-by='.lastTimestamp'
```

## Scaling Operations

### Manual Scaling

```bash
# Scale up
kubectl scale deployment euystacio-api --replicas=10 -n euystacio-ai

# Scale down
kubectl scale deployment euystacio-api --replicas=3 -n euystacio-ai

# Verify
kubectl get deployment euystacio-api -n euystacio-ai
```

### Adjust HPA Parameters

```bash
# Edit HPA
kubectl edit hpa euystacio-api-hpa -n euystacio-ai

# Or apply new configuration
kubectl apply -f infrastructure/kubernetes/euystacio-deployment.yaml
```

### Resource Limit Adjustments

```bash
# Check current limits
kubectl describe deployment euystacio-api -n euystacio-ai | grep -A 5 "Limits\|Requests"

# Update limits
kubectl set resources deployment euystacio-api \
  --requests=cpu=500m,memory=512Mi \
  --limits=cpu=2000m,memory=2Gi \
  -n euystacio-ai
```

## Backup and Recovery

### Configuration Backup

```bash
# Backup Kubernetes configurations
kubectl get all -n euystacio-ai -o yaml > backup-k8s-$(date +%Y%m%d).yaml

# Backup ConfigMaps
kubectl get configmap -n euystacio-ai -o yaml > backup-configmaps-$(date +%Y%m%d).yaml

# Backup Secrets (secure storage required)
kubectl get secrets -n euystacio-ai -o yaml > backup-secrets-$(date +%Y%m%d).yaml
```

### Metrics Data Backup

```bash
# Prometheus snapshot
curl -XPOST http://prometheus:9090/api/v1/admin/tsdb/snapshot

# Download snapshot
kubectl cp monitoring/prometheus-0:/prometheus/snapshots/latest ./prometheus-backup-$(date +%Y%m%d)
```

### Recovery Procedures

#### Restore from Backup

```bash
# Restore Kubernetes resources
kubectl apply -f backup-k8s-20250101.yaml

# Restore ConfigMaps
kubectl apply -f backup-configmaps-20250101.yaml

# Verify restoration
kubectl get all -n euystacio-ai
```

#### Disaster Recovery

1. **Provision new cluster**:
   ```bash
   cd infrastructure/terraform
   terraform init
   terraform apply
   ```

2. **Restore configurations**:
   ```bash
   kubectl create namespace euystacio-ai
   kubectl create namespace monitoring
   kubectl apply -f backup-k8s-latest.yaml
   ```

3. **Restore monitoring stack**:
   ```bash
   helm install prometheus-operator prometheus-community/kube-prometheus-stack \
     -n monitoring -f helm-values/prometheus-operator-values.yaml
   ```

4. **Verify recovery**:
   ```bash
   kubectl get all -n euystacio-ai
   kubectl get all -n monitoring
   curl http://euystacio-api:8000/health
   ```

## Monitoring Stack Management

### Restart Prometheus

```bash
kubectl rollout restart statefulset/prometheus-prometheus-operator -n monitoring
```

### Restart Grafana

```bash
kubectl rollout restart deployment/grafana -n monitoring
```

### Update Prometheus Configuration

```bash
# Edit ConfigMap
kubectl edit configmap prometheus-config -n monitoring

# Reload Prometheus
kubectl exec -n monitoring prometheus-prometheus-operator-0 -- \
  curl -X POST http://localhost:9090/-/reload
```

### Update Grafana Dashboards

```bash
# Update ConfigMap
kubectl apply -f monitoring/grafana/dashboards/meta-salvage-overview.json

# Restart Grafana to load new dashboards
kubectl rollout restart deployment/grafana -n monitoring
```

## Contact Information

### On-Call Rotation
- Check PagerDuty/Opsgenie for current on-call
- Escalation: [escalation policy]

### Emergency Contacts
- System Owner: [contact]
- Infrastructure Team: [contact]
- Security Team: [contact]

### Communication Channels
- Slack: #euystacio-ops
- Incident Channel: #incident-[id]
- Status Page: [url]

---

*Last Updated: 2025-12-08*
*Version: 1.0*
