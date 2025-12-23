# Protocollo Meta Salvage - Developer Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Getting Started](#getting-started)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Monitoring & Observability](#monitoring--observability)
6. [Policy Enforcement](#policy-enforcement)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Contributing](#contributing)

## Introduction

The Protocollo Meta Salvage is an automated framework for ethical risk monitoring, symbiosis score tracking, and adaptive policy enforcement within the Euystacio AI ecosystem.

### Key Features

- **Automated CI/CD Pipeline**: Comprehensive testing and deployment automation
- **Real-time Monitoring**: Prometheus and Grafana integration for metrics tracking
- **Ethical Metrics**: QEK (Quantum Ethical Kernel), H-VAR (Harmonic Volatility Ratio), and Symbiosis Score monitoring
- **Policy Enforcement**: Open Policy Agent (OPA) with adaptive Peace Bonds
- **Scalable Infrastructure**: Kubernetes and Terraform for infrastructure as code

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Euystacio AI Platform                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Core API   │  │  Threshold   │  │   Reflector  │      │
│  │   (Flask)    │  │   Monitor    │  │   System     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│         └──────────────────┴──────────────────┘              │
│                           │                                   │
│                           ▼                                   │
│                  ┌────────────────┐                          │
│                  │  Metrics API   │                          │
│                  └────────┬───────┘                          │
│                           │                                   │
├───────────────────────────┼───────────────────────────────────┤
│                           │                                   │
│  ┌────────────────────────┴────────────────────────┐        │
│  │           Monitoring & Observability             │        │
│  ├──────────────────────────────────────────────────┤        │
│  │                                                   │        │
│  │  ┌─────────────┐  ┌──────────────┐             │        │
│  │  │ Prometheus  │→ │   Grafana    │             │        │
│  │  │  (Metrics)  │  │ (Dashboards) │             │        │
│  │  └─────────────┘  └──────────────┘             │        │
│  │                                                   │        │
│  └───────────────────────────────────────────────────┘        │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────┐          │
│  │          Policy Enforcement (OPA)              │          │
│  ├───────────────────────────────────────────────┤          │
│  │                                                 │          │
│  │  • Peace Bonds Policies                        │          │
│  │  • Adaptive Enforcement                        │          │
│  │  • Risk-based Decisions                        │          │
│  │                                                 │          │
│  └─────────────────────────────────────────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 14+ (for ULP Sacralis scripts)
- Docker (optional, for local development)
- kubectl (for Kubernetes deployments)
- Terraform (for infrastructure management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hannesmitterer/euystacio-ai.git
cd euystacio-ai
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Verify installation:
```bash
python -c "from core.threshold_monitor import ThresholdMonitor; print('✓ Installation successful')"
```

## CI/CD Pipeline

### Workflow Overview

The Meta Salvage CI/CD pipeline consists of four main jobs:

1. **test-symbiosis-metrics**: Validates Symbiosis Score calculations and ethical metrics
2. **test-risk-detection**: Tests risk detection and logging mechanisms
3. **integration-tests**: Runs comprehensive integration tests
4. **deployment-readiness**: Validates deployment configuration

### Running CI Tests Locally

```bash
# Run all tests
pytest -v

# Run specific test categories
pytest -v -m symbiosis
pytest -v -m risk
pytest -v -m policy

# Run with coverage
pytest --cov=core --cov=analytics --cov-report=html
```

### Triggering Workflows

The CI/CD pipeline automatically runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via GitHub Actions UI

## Monitoring & Observability

### Prometheus Configuration

Prometheus is configured to scrape metrics from multiple sources:

- **Euystacio Core API** (`/metrics`)
- **Symbiosis Metrics** (`/api/metrics/symbiosis`)
- **Threshold Monitor** (`/api/metrics/thresholds`)
- **Risk Detection** (`/api/metrics/risk`)
- **OPA Policy Engine** (`/metrics`)

### Key Metrics

#### Symbiosis Score
- `symbiosis_score`: Current symbiosis score (0-1)
- `symbiosis_score:avg_5m`: 5-minute average
- `symbiosis_score:rate_5m`: Rate of change

#### Ethical Metrics
- `qek_value`: Quantum Ethical Kernel (ideal: 0.938)
- `hvar_value`: Harmonic Volatility Ratio (ideal: 0.043)
- `ethisches_ideal_value`: Ethical Ideal compliance (ideal: 1.0)

#### Risk Metrics
- `risk_score`: Overall risk score
- `risk_events:rate_5m`: Risk event rate
- `risk_events:high_severity_rate`: High-severity risk event rate

#### Peace Bonds Metrics
- `peace_bonds:policy_evaluations_total`: Total policy evaluations
- `peace_bonds:violations_rate`: Policy violation rate
- `peace_bonds:enforcement_actions_total`: Enforcement actions taken

### Grafana Dashboards

Access the Meta Salvage Overview dashboard at:
- Local: `http://localhost:3000/d/meta-salvage-overview`
- Production: Configure in your Grafana instance

Dashboard panels include:
1. Symbiosis Score (time series)
2. QEK gauge
3. H-VAR gauge
4. Ethisches Ideal compliance
5. Risk event rates
6. Peace Bonds status
7. TFM-1 equilibrium balance
8. System availability
9. Adaptive adjustments
10. Active alerts table

### Setting Up Monitoring

#### Local Development

```bash
# Start Prometheus
docker run -d -p 9090:9090 \
  -v $(pwd)/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Start Grafana
docker run -d -p 3000:3000 \
  -v $(pwd)/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources \
  -v $(pwd)/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards \
  grafana/grafana
```

#### Production Deployment

Use Terraform to deploy the monitoring stack:

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## Policy Enforcement

### Open Policy Agent (OPA)

OPA provides policy-as-code for Peace Bonds enforcement.

#### Policy Structure

```rego
package euystacio.peace_bonds

# Risk score calculation
risk_score := score if {
    provider := input.provider
    score := (
        provider.trust_weight * 0.4 +
        provider.compliance_score * 0.3 +
        provider.ethical_alignment * 0.3
    )
}

# Allow/deny decisions
allow if {
    risk_level in ["low", "medium"]
    symbiosis_check_passed
}
```

#### Testing Policies

```bash
# Install OPA
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa

# Test policy
./opa test infrastructure/kubernetes/opa-peace-bonds.yaml
```

### Adaptive Enforcement

Peace Bonds policies adapt dynamically based on:
- System load (CPU, memory)
- Current ethical metrics (QEK, H-VAR)
- Real-time symbiosis scores

The adjustment multiplier increases thresholds when the system is under load, providing graceful degradation.

## Testing

### Test Structure

```
tests/
├── test_symbiosis_metrics.py    # Symbiosis score tests
├── test_risk_detection.py       # Risk monitoring tests
└── test_peace_bonds.py          # Policy enforcement tests
```

### Test Categories

Tests are marked with pytest markers:
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.symbiosis`: Symbiosis-related tests
- `@pytest.mark.risk`: Risk detection tests
- `@pytest.mark.policy`: Policy enforcement tests

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Specific test file
pytest tests/test_risk_detection.py -v

# With coverage report
pytest --cov=core --cov-report=html
open htmlcov/index.html
```

### Writing Tests

Follow the existing test patterns:

```python
import pytest

@pytest.mark.unit
@pytest.mark.symbiosis
def test_symbiosis_calculation():
    """Test symbiosis score calculation"""
    score = calculate_symbiosis(0.8, 0.9, 0.7)
    assert 0.0 <= score <= 1.0
```

## Deployment

### Infrastructure as Code

#### Terraform

Deploy infrastructure:

```bash
cd infrastructure/terraform

# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan
```

#### Kubernetes

Deploy applications:

```bash
# Apply configurations
kubectl apply -f infrastructure/kubernetes/euystacio-deployment.yaml
kubectl apply -f infrastructure/kubernetes/opa-peace-bonds.yaml

# Verify deployments
kubectl get deployments -n euystacio-ai
kubectl get pods -n euystacio-ai

# Check logs
kubectl logs -f deployment/euystacio-api -n euystacio-ai
```

### Horizontal Pod Autoscaling

The system automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)
- Symbiosis score (custom metric)

View HPA status:

```bash
kubectl get hpa -n euystacio-ai
kubectl describe hpa euystacio-api-hpa -n euystacio-ai
```

### Rolling Updates

Deploy new versions with zero downtime:

```bash
# Update image
kubectl set image deployment/euystacio-api \
  euystacio-api=euystacio-ai:v2.0.0 \
  -n euystacio-ai

# Monitor rollout
kubectl rollout status deployment/euystacio-api -n euystacio-ai

# Rollback if needed
kubectl rollout undo deployment/euystacio-api -n euystacio-ai
```

## Contributing

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and small

### Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Run tests locally: `pytest -v`
5. Update documentation if needed
6. Submit PR with clear description
7. Address review feedback

### Commit Messages

Follow conventional commits:
- `feat: Add new monitoring dashboard`
- `fix: Correct symbiosis calculation`
- `docs: Update deployment guide`
- `test: Add risk detection tests`

## Troubleshooting

### Common Issues

**Issue**: Tests fail with import errors
```bash
# Solution: Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**Issue**: Prometheus not scraping metrics
```bash
# Check targets
curl http://localhost:9090/api/v1/targets

# Verify metrics endpoint
curl http://euystacio-api:8000/metrics
```

**Issue**: OPA policies not loading
```bash
# Check OPA logs
kubectl logs -f deployment/opa-peace-bonds -n euystacio-ai

# Verify ConfigMap
kubectl get configmap peace-bonds-policies -n euystacio-ai -o yaml
```

## Resources

- [GitHub Repository](https://github.com/hannesmitterer/euystacio-ai)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OPA Documentation](https://www.openpolicyagent.org/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Documentation](https://www.terraform.io/docs/)

## Support

For questions or issues:
1. Check existing GitHub issues
2. Review documentation
3. Open a new issue with details

---

*"Rigenerazione > Profitto. La fiducia è verificabilità."*
