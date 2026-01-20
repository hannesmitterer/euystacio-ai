# Euystacio AI - Security and Resilience Systems

This directory contains the security and resilience infrastructure for Euystacio AI decentralized operations.

## Overview

The security framework implements five key components:

1. **Real-time Monitoring Dashboard** (Grafana + Loki)
2. **Forensic Response Automation** (Log Watcher + Tor/VPN)
3. **Secure Firmware Updates** (Checksum + GPG Signatures)
4. **Distributed Encrypted Backups** (IPFS + GPG)
5. **Communication Protocol Hardening** (QUIC + TLS 1.3)

## Directory Structure

```
security/
├── forensic_response.py         # Automated intrusion detection and response
├── firmware_update.py            # Secure firmware update system
├── ipfs_backup.py               # IPFS-based encrypted backups
├── protocol_hardening.py        # QUIC + TLS 1.3 configuration
├── forensic_config.json         # Forensic response configuration
├── protocol_config.json         # Protocol security configuration
├── nginx-quic-tls13.conf       # Nginx configuration for QUIC
├── apache-quic-tls13.conf      # Apache configuration for QUIC
└── openssl-cert.conf           # OpenSSL certificate configuration

monitoring/
├── docker-compose.yml           # Grafana + Loki deployment
├── grafana/
│   └── grafana.ini             # Grafana configuration
├── loki/
│   └── loki-config.yml         # Loki configuration
├── promtail/
│   └── promtail-config.yml     # Promtail configuration
├── datasources/
│   └── loki.yml                # Loki datasource
└── dashboards/
    ├── node-status-dashboard.json       # Node monitoring
    ├── security-dashboard.json          # Security monitoring
    └── dashboard-provider.yml           # Dashboard provisioning
```

## Quick Start

### 1. Monitoring Dashboard (Grafana + Loki)

Start the monitoring stack:

```bash
cd monitoring
docker-compose up -d
```

Access Grafana at http://localhost:3000 (default credentials: admin/admin)

Dashboards available:
- **Node Status & Performance**: Real-time node metrics and latency
- **Security & Intrusion Detection**: Security events and alerts

### 2. Forensic Response System

Start the automated forensic response monitor:

```bash
python3 security/forensic_response.py
```

Features:
- Monitors logs for suspicious activity patterns
- Automatically activates Tor/VPN routing when threshold reached
- Configurable alert thresholds and response modes
- Real-time intrusion detection

Configuration in `security/forensic_config.json`:
- `alert_threshold`: Number of detections before response (default: 5)
- `response_mode`: "tor" or "vpn"
- `auto_response_enabled`: Enable automatic responses
- `cooldown_period`: Seconds before system resets (default: 300)

### 3. Secure Firmware Updates

Create and verify firmware updates:

```python
from security.firmware_update import FirmwareUpdateSystem

# Initialize system
fus = FirmwareUpdateSystem()

# Create update manifest
manifest_path = fus.create_update_manifest({
    "version": "1.0.0",
    "release_notes": "Security improvements",
    "files": [
        {"path": "/path/to/file", "target_path": "/destination/path"}
    ]
})

# Apply update
fus.apply_update(manifest_path)

# Rollback if needed
fus.rollback("backup_id")
```

Features:
- SHA-256 checksum verification
- GPG signature verification
- Automatic backup before updates
- Rollback capability
- Update history tracking

### 4. IPFS Distributed Backups

Create encrypted backups distributed via IPFS:

```python
from security.ipfs_backup import IPFSBackupSystem

# Initialize system
ipfs = IPFSBackupSystem()

# Create encrypted backup
backup = ipfs.create_encrypted_backup(
    files=["genesis.md", "red_code.json"],
    backup_name="daily_backup"
)

# Restore from backup
ipfs.restore_backup(backup["backup_id"])

# Setup automated backups
ipfs.setup_automated_backups(schedule="daily")
```

Features:
- GPG encryption for all backups
- IPFS distributed storage
- Automatic checksum verification
- Configurable retention policies
- Restore with integrity verification

### 5. Protocol Hardening (QUIC + TLS 1.3)

Configure secure communication protocols:

```python
from security.protocol_hardening import ProtocolHardeningConfig

# Initialize configuration
config = ProtocolHardeningConfig()

# Get TLS 1.3 context
tls_context = config.create_tls_context()

# Get QUIC configuration
quic_config = config.get_quic_config()

# Validate connections
is_secure = config.validate_connection("h3", encrypted=True)
```

Features:
- TLS 1.3 only (no fallback to older versions)
- QUIC protocol support (HTTP/3)
- Strong cipher suites only
- HSTS enforcement
- Automatic rejection of unencrypted connections

Web server configurations:
- `security/nginx-quic-tls13.conf` - Nginx configuration
- `security/apache-quic-tls13.conf` - Apache configuration

Generate self-signed certificate:
```bash
openssl req -new -x509 -days 365 -nodes \
  -config security/openssl-cert.conf \
  -out security/cert.pem \
  -keyout security/key.pem
```

## Security Requirements

### Dependencies

```bash
# Python packages
pip install cryptography flask

# System packages (Ubuntu/Debian)
apt-get install -y gnupg tor openvpn ipfs

# Docker (for monitoring)
apt-get install -y docker.io docker-compose
```

### GPG Key Setup

Generate GPG key for backups and signatures:

```bash
gpg --full-generate-key
gpg --list-keys
gpg --export -a "euystacio-backup@example.com" > security/gpg_public.key
```

### Tor Setup

Install and configure Tor:

```bash
apt-get install tor
systemctl enable tor
systemctl start tor
```

### IPFS Setup

Install and initialize IPFS:

```bash
wget https://dist.ipfs.io/go-ipfs/latest/go-ipfs_linux-amd64.tar.gz
tar -xvzf go-ipfs_linux-amd64.tar.gz
cd go-ipfs
./install.sh
ipfs init
ipfs daemon &
```

## Configuration

### Environment Variables

```bash
# Grafana
export GRAFANA_ADMIN_PASSWORD="your-secure-password"
export GRAFANA_SECRET_KEY="your-secret-key"

# GPG
export GPG_KEY_ID="your-key-id"
export GPG_PASSPHRASE="your-passphrase"

# Backup
export BACKUP_RETENTION_DAYS=30
export IPFS_API_URL="http://localhost:5001"
```

### Firewall Configuration

```bash
# Allow HTTPS and QUIC
ufw allow 443/tcp
ufw allow 443/udp

# Allow monitoring (localhost only)
ufw allow from 127.0.0.1 to any port 3000
ufw allow from 127.0.0.1 to any port 3100
```

## Monitoring and Alerts

### Log Files

- **System logs**: `/home/runner/work/euystacio-ai/euystacio-ai/logs/*.log`
- **Intrusion detection**: `/home/runner/work/euystacio-ai/euystacio-ai/security/intrusion_detection.log`
- **Firmware updates**: `/home/runner/work/euystacio-ai/euystacio-ai/logs/firmware_updates.log`
- **Backup system**: `/home/runner/work/euystacio-ai/euystacio-ai/logs/backup_system.log`

### Grafana Alerts

Configured alerts:
- High intrusion activity (>10 events in 5 minutes)
- Failed firmware updates
- Backup failures
- Protocol downgrade attempts

### Health Checks

Check system status:

```python
# Forensic Response
from security.forensic_response import ForensicResponseSystem
frs = ForensicResponseSystem()
status = frs.get_status()

# Firmware Updates
from security.firmware_update import FirmwareUpdateSystem
fus = FirmwareUpdateSystem()
version = fus.get_current_version()

# Backups
from security.ipfs_backup import IPFSBackupSystem
ipfs = IPFSBackupSystem()
status = ipfs.get_backup_status()

# Protocol Security
from security.protocol_hardening import ProtocolHardeningConfig
config = ProtocolHardeningConfig()
status = config.get_security_status()
```

## Testing

Run security tests:

```bash
# Test forensic response
echo "failed login attempt" | python3 security/forensic_response.py

# Test firmware updates
python3 security/firmware_update.py

# Test IPFS backups
python3 security/ipfs_backup.py

# Test protocol hardening
python3 security/protocol_hardening.py
```

## Troubleshooting

### Grafana not accessible
```bash
docker-compose -f monitoring/docker-compose.yml logs grafana
docker-compose -f monitoring/docker-compose.yml restart grafana
```

### Tor activation fails
```bash
systemctl status tor
journalctl -u tor -n 50
```

### IPFS connection issues
```bash
ipfs id
ipfs swarm peers
```

### GPG encryption fails
```bash
gpg --list-keys
gpg --list-secret-keys
```

## Security Best Practices

1. **Regularly rotate GPG keys** (every 6-12 months)
2. **Monitor intrusion logs daily**
3. **Test backup restoration monthly**
4. **Keep firmware signatures offline** when not in use
5. **Review Grafana dashboards daily**
6. **Update cipher suites** as new standards emerge
7. **Run security audits quarterly**
8. **Test rollback procedures** before production deployments

## Contributing

Security improvements should:
1. Maintain backward compatibility where possible
2. Include tests and documentation
3. Follow the principle of defense in depth
4. Be reviewed by multiple team members
5. Include threat model updates

## License

See main repository LICENSE file.

## Contact

For security issues, contact: security@euystacio.ai

---

**AI Signature**: GitHub Copilot & Seed-bringer hannesmitterer  
**Last Updated**: 2026-01-20
