# Monitoring Stack for Protocollo Meta Salvage

This directory contains the configuration for the monitoring and observability stack, including Prometheus for metrics collection and Grafana for visualization.

## Directory Structure

```
monitoring/
├── prometheus/
│   ├── prometheus.yml       # Main Prometheus configuration
│   └── rules.yml           # Recording rules for pre-computed metrics
├── grafana/
│   ├── dashboards/
│   │   └── meta-salvage-overview.json  # Main dashboard
│   └── datasources/
│       └── prometheus.yml  # Prometheus datasource configuration
└── README.md
```

## Prometheus

### Configuration

The Prometheus configuration (`prometheus.yml`) defines:

1. **Scrape Intervals**: 15s global, with job-specific overrides
2. **Alertmanager Integration**: For alert notification
3. **Scrape Configs**: Multiple jobs for different components

### Scrape Jobs

| Job Name | Target | Metrics Path | Interval |
|----------|--------|--------------|----------|
| prometheus | localhost:9090 | /metrics | 15s |
| euystacio-core | euystacio-api:8000 | /metrics | 10s |
| symbiosis-metrics | euystacio-api:8000 | /api/metrics/symbiosis | 30s |
| threshold-monitor | euystacio-api:8000 | /api/metrics/thresholds | 15s |
| risk-detection | euystacio-api:8000 | /api/metrics/risk | 20s |
| tfm1 | tfm1-service:8080 | /metrics | 15s |
| peace-bonds | opa-service:8181 | /metrics | 30s |
| node-exporter | node-exporter:9100 | /metrics | 15s |

### Recording Rules

Recording rules pre-compute frequently used queries for better performance:

#### Symbiosis Metrics
- `symbiosis_score:avg_5m`: 5-minute average
- `symbiosis_score:rate_5m`: Rate of change

#### Ethical Metrics
- `qek_value:current`: Current QEK value
- `qek_value:avg_5m`: QEK 5-minute average
- `hvar_value:current`: Current H-VAR value
- `ethisches_ideal_value:current`: Current Ethisches Ideal value

#### Risk Metrics
- `risk_score:total`: Total risk score across all sources
- `risk_events:rate_5m`: Risk event rate
- `risk_events:high_severity_rate`: High-severity risk event rate

#### Peace Bonds Metrics
- `peace_bonds:policy_evaluations_total`: Total policy evaluations
- `peace_bonds:violations_rate`: Policy violation rate

### Running Prometheus Locally

```bash
# Using Docker
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/prometheus/rules.yml:/etc/prometheus/rules/rules.yml \
  prom/prometheus

# Access Prometheus UI
open http://localhost:9090
```

### Querying Metrics

Examples of useful queries:

```promql
# Current symbiosis score
symbiosis_score

# QEK deviation from ideal
abs(qek_value - 0.938)

# Risk event rate (per second)
rate(risk_events_total[5m])

# Peace Bonds violations in last hour
increase(peace_bonds_violations_total[1h])

# System availability
avg_over_time(up[1h])
```

## Grafana

### Dashboards

#### Meta Salvage Overview Dashboard

The main dashboard provides a comprehensive view of the system:

**Panels**:
1. **Symbiosis Score** (Graph): Real-time and 5-min average
2. **QEK Gauge**: Current value with thresholds
3. **H-VAR Gauge**: Current value with thresholds
4. **Ethisches Ideal** (Stat): Compliance percentage
5. **Risk Events Rate** (Graph): All events and high-severity
6. **Peace Bonds Status** (Stat): Policy evaluation count
7. **TFM-1 Equilibrium** (Graph): Balance over time
8. **System Availability** (Graph): Service uptime
9. **Adaptive Adjustments** (Graph): Peace Bonds adjustment rate
10. **Alerts Summary** (Table): Currently firing alerts

**Alert Conditions**:
- Symbiosis Score < 0.5 triggers alert

### Datasources

The Prometheus datasource is pre-configured to connect to the Prometheus instance.

Configuration:
- **URL**: `http://prometheus:9090`
- **Access**: Proxy
- **Scrape Interval**: 15s
- **Query Timeout**: 60s

### Running Grafana Locally

```bash
# Using Docker
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  -v $(pwd)/grafana/datasources:/etc/grafana/provisioning/datasources \
  -v $(pwd)/grafana/dashboards:/etc/grafana/provisioning/dashboards \
  grafana/grafana

# Access Grafana UI
open http://localhost:3000
# Default credentials: admin/admin
```

### Importing Dashboards

Dashboards are automatically provisioned from the `dashboards/` directory. To manually import:

1. Navigate to Grafana UI
2. Click "+" → "Import"
3. Upload `meta-salvage-overview.json`
4. Select Prometheus datasource
5. Click "Import"

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster
- kubectl configured
- Helm 3.x installed

### Deploy with Terraform

```bash
cd ../infrastructure/terraform
terraform init
terraform apply
```

This will deploy:
- Prometheus Operator
- Grafana
- Required ConfigMaps and Services

### Manual Deployment

```bash
# Create namespace
kubectl create namespace monitoring

# Apply Prometheus configuration
kubectl create configmap prometheus-config \
  --from-file=prometheus.yml \
  --from-file=rules.yml \
  -n monitoring

# Apply Grafana datasources
kubectl create configmap grafana-datasources \
  --from-file=datasources/prometheus.yml \
  -n monitoring

# Apply Grafana dashboards
kubectl create configmap grafana-dashboards \
  --from-file=dashboards/meta-salvage-overview.json \
  -n monitoring \
  --dry-run=client -o yaml | \
  kubectl label -f - grafana_dashboard=1 --local -o yaml | \
  kubectl apply -f -

# Install Prometheus Operator via Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-operator prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi

# Install Grafana via Helm
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana \
  -n monitoring \
  --set persistence.enabled=true \
  --set persistence.size=10Gi
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n monitoring

# Port-forward Prometheus
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090

# Port-forward Grafana
kubectl port-forward -n monitoring svc/grafana 3000:80

# Get Grafana admin password
kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

## Alerting

### Alert Rules

Alert rules are defined in `prometheus-alerts.yaml` (in `tfm1/equilibrium-topup/` for existing rules).

To add new alert rules:

1. Create alert definition in `rules.yml`:
```yaml
groups:
  - name: meta_salvage_alerts
    rules:
      - alert: LowSymbiosisScore
        expr: symbiosis_score < 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low symbiosis score detected"
          description: "Symbiosis score is {{ $value }}"
```

2. Reload Prometheus configuration:
```bash
kubectl exec -n monitoring prometheus-xxx-0 -- \
  curl -X POST http://localhost:9090/-/reload
```

### Alert Channels

Configure notification channels in Alertmanager:
- Slack
- Email
- PagerDuty
- Webhook

## Metrics API Endpoints

The Euystacio API should expose the following metrics endpoints:

| Endpoint | Description |
|----------|-------------|
| `/metrics` | Standard Prometheus metrics |
| `/api/metrics/symbiosis` | Symbiosis score metrics |
| `/api/metrics/thresholds` | Threshold monitor metrics |
| `/api/metrics/risk` | Risk detection metrics |
| `/health` | Health check endpoint |

Example implementation:

```python
from prometheus_client import Counter, Gauge, generate_latest
from flask import Response

# Define metrics
symbiosis_score = Gauge('symbiosis_score', 'Current symbiosis score')
qek_value = Gauge('qek_value', 'Quantum Ethical Kernel value')
risk_events = Counter('risk_events_total', 'Total risk events', ['severity'])

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

## Troubleshooting

### Prometheus Not Scraping Targets

1. Check target status:
   ```bash
   curl http://localhost:9090/api/v1/targets
   ```

2. Verify network connectivity:
   ```bash
   kubectl exec -n monitoring prometheus-xxx-0 -- \
     wget -O- http://euystacio-api:8000/metrics
   ```

3. Check Prometheus logs:
   ```bash
   kubectl logs -n monitoring prometheus-xxx-0
   ```

### Grafana Dashboards Not Loading

1. Verify datasource:
   ```bash
   curl http://localhost:3000/api/datasources
   ```

2. Check dashboard provisioning:
   ```bash
   kubectl logs -n monitoring deployment/grafana | grep dashboard
   ```

3. Manually test Prometheus connection:
   - Go to Configuration → Data Sources
   - Click Prometheus
   - Click "Test"

### High Cardinality Issues

If Prometheus is consuming too much memory:

1. Reduce scrape intervals
2. Add metric relabeling to drop unused labels
3. Increase Prometheus resources
4. Enable remote write for long-term storage

## Best Practices

1. **Label Naming**: Use consistent label names across services
2. **Metric Names**: Follow Prometheus naming conventions
3. **Recording Rules**: Pre-compute expensive queries
4. **Retention**: Balance storage vs. historical data needs
5. **Alerting**: Alert on symptoms, not causes
6. **Dashboards**: Keep dashboards focused and actionable

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

---

*For questions or issues, refer to the [Developer Guide](../docs/DEVELOPER_GUIDE.md) or [Runbooks](../docs/RUNBOOKS.md)*
