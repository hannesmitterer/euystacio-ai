# Lex Amoris Integration Guide

Guida rapida per integrare i sistemi Lex Amoris in applicazioni esistenti.

## Quick Start

### 1. Installazione Base

Nessuna dipendenza esterna richiesta oltre alle librerie standard Python.

```python
# Importa i componenti principali
from core.lex_amoris_security import get_security_manager
from core.lex_amoris_rescue import get_rescue_channel
from core.ipfs_pr_backup import get_pr_backup_manager
```

### 2. Validazione Pacchetti (5 minuti)

```python
from core.lex_amoris_security import DataPacket, get_security_manager
from datetime import datetime, timezone

def validate_request(ip_address, request_data, metadata=None):
    """Valida una richiesta HTTP/API usando Lex Amoris"""
    
    # Crea pacchetto dati
    packet = DataPacket(
        packet_id=f"REQ-{datetime.now().timestamp()}",
        source_ip=ip_address,
        timestamp=datetime.now(timezone.utc).isoformat(),
        data=request_data.encode() if isinstance(request_data, str) else request_data,
        metadata=metadata or {}
    )
    
    # Valida
    manager = get_security_manager()
    is_valid, reason = manager.validate_packet(packet)
    
    return is_valid, reason

# Uso in Flask/FastAPI
@app.route('/api/endpoint', methods=['POST'])
def api_endpoint():
    is_valid, reason = validate_request(
        request.remote_addr,
        request.get_data(),
        {"endpoint": "/api/endpoint", "method": "POST"}
    )
    
    if not is_valid:
        return {"error": "Request blocked", "reason": reason}, 403
    
    # Procedi con la richiesta normale
    return process_request()
```

### 3. Gestione False Positive (2 minuti)

```python
from core.lex_amoris_rescue import get_rescue_channel, RescueType, UrgencyLevel

def unblock_legitimate_source(ip_address, reason, evidence):
    """Sblocca una sorgente legittima bloccata per errore"""
    
    channel = get_rescue_channel()
    
    request = channel.submit_rescue_request(
        source_ip=ip_address,
        rescue_type=RescueType.FALSE_POSITIVE,
        reason=reason,
        evidence=evidence,
        requested_by="system",
        urgency=UrgencyLevel.HIGH
    )
    
    # Se auto-approvato, la sorgente è già sbloccata
    if request.status == "APPROVED":
        return True, f"Auto-approved: {request.resolution_notes}"
    
    return False, f"Pending review: {request.request_id}"

# Uso
success, message = unblock_legitimate_source(
    "192.168.1.100",
    "Production API endpoint",
    {
        "confidence_level": 0.95,
        "manual_verification": True,
        "uptime": "6 months"
    }
)
```

### 4. Backup PR Automatico (3 minuti)

```python
from core.ipfs_pr_backup import get_pr_backup_manager, PRConfiguration, BackupTrigger
from datetime import datetime, timezone

def backup_pull_request(pr_data):
    """Backup automatico di un PR su IPFS"""
    
    manager = get_pr_backup_manager()
    
    # Converti dati PR in configurazione
    pr_config = PRConfiguration(
        pr_number=pr_data['number'],
        title=pr_data['title'],
        description=pr_data.get('description', ''),
        branch=pr_data['head']['ref'],
        base_branch=pr_data['base']['ref'],
        files_changed=pr_data.get('files', []),
        commits=pr_data.get('commits', []),
        metadata=pr_data.get('metadata', {}),
        created_at=pr_data['created_at'],
        updated_at=pr_data['updated_at']
    )
    
    # Backup su IPFS
    record = manager.backup_pr_configuration(
        pr_config,
        trigger=BackupTrigger.PR_CREATED
    )
    
    return record.ipfs_cid, record.status

# Uso con GitHub webhook
@app.route('/webhooks/github', methods=['POST'])
def github_webhook():
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'pull_request':
        pr_data = request.json['pull_request']
        cid, status = backup_pull_request(pr_data)
        print(f"PR #{pr_data['number']} backed up: {cid} ({status})")
    
    return {'status': 'ok'}
```

## Integrazione Avanzata

### Middleware Flask/FastAPI

```python
from flask import Flask, request, jsonify
from functools import wraps
from core.lex_amoris_security import get_security_manager, DataPacket
from datetime import datetime, timezone

app = Flask(__name__)
security_manager = get_security_manager()

def lex_amoris_protect(f):
    """Decorator per proteggere endpoint con Lex Amoris"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Crea pacchetto dalla richiesta
        packet = DataPacket(
            packet_id=f"REQ-{datetime.now().timestamp()}",
            source_ip=request.remote_addr,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=request.get_data(),
            metadata={
                "endpoint": request.path,
                "method": request.method,
                "user_agent": request.headers.get('User-Agent', '')
            }
        )
        
        # Valida
        is_valid, reason = security_manager.validate_packet(packet)
        
        if not is_valid:
            return jsonify({
                "error": "Request blocked by Lex Amoris Security",
                "reason": reason
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

# Uso
@app.route('/api/protected', methods=['POST'])
@lex_amoris_protect
def protected_endpoint():
    return jsonify({"message": "Success"})
```

### Background Monitoring

```python
import time
import threading
from core.lex_amoris_security import get_security_manager
from core.ipfs_pr_backup import get_pr_backup_manager

def security_monitor_loop():
    """Background thread per monitoraggio continuo"""
    manager = get_security_manager()
    
    while True:
        # Cleanup blacklist scaduta
        manager.blacklist.cleanup_expired()
        
        # Ottieni dashboard status
        dashboard = manager.get_security_dashboard()
        
        # Log metriche
        print(f"[MONITOR] Mode: {dashboard['overall_status']['protection_mode']}, "
              f"Blocked: {dashboard['overall_status']['blacklisted_sources']}, "
              f"EM: {dashboard['lazy_security']['current_em_pressure']:.2f} mV/m")
        
        # Dormi 60 secondi
        time.sleep(60)

def backup_monitor_loop():
    """Background thread per monitoraggio backup"""
    manager = get_pr_backup_manager()
    
    while True:
        # Controlla minacce
        threat = manager.detect_escalation_threat()
        
        if threat['threat_level'] != 'NONE':
            print(f"[BACKUP] ALERT: Threat level {threat['threat_level']}")
            for indicator in threat['indicators']:
                print(f"  - {indicator['type']}: {indicator['count']}")
        
        time.sleep(300)  # 5 minuti

# Avvia monitoring
threading.Thread(target=security_monitor_loop, daemon=True).start()
threading.Thread(target=backup_monitor_loop, daemon=True).start()
```

### Dashboard Web (Esempio)

```python
from flask import Flask, render_template, jsonify
from core.lex_amoris_security import get_security_manager
from core.lex_amoris_rescue import get_rescue_channel
from core.ipfs_pr_backup import get_pr_backup_manager

app = Flask(__name__)

@app.route('/dashboard/lex-amoris')
def lex_amoris_dashboard():
    """Dashboard HTML per monitoraggio Lex Amoris"""
    return render_template('lex_amoris_dashboard.html')

@app.route('/api/dashboard/security')
def security_api():
    """API per dati security"""
    manager = get_security_manager()
    return jsonify(manager.get_security_dashboard())

@app.route('/api/dashboard/rescue')
def rescue_api():
    """API per dati rescue channel"""
    channel = get_rescue_channel()
    return jsonify(channel.get_dashboard_data())

@app.route('/api/dashboard/backup')
def backup_api():
    """API per dati backup"""
    manager = get_pr_backup_manager()
    return jsonify(manager.get_dashboard_data())
```

## Configurazione

### Personalizza Parametri Security

```python
from core.lex_amoris_security import get_security_manager

manager = get_security_manager()

# Regola frequency base
manager.rhythm_validator.base_frequency = 2.0  # 2 Hz invece di 1 Hz

# Regola threshold harmony
manager.rhythm_validator.harmony_threshold = 0.20  # 20% invece di 15%

# Configura EM threshold
manager.lazy_security.em_pressure_threshold = 60.0  # 60 mV/m invece di 50
```

### Personalizza Rescue Channel

```python
from core.lex_amoris_rescue import get_rescue_channel

channel = get_rescue_channel()

# Modifica regole auto-approval
channel.auto_approval_rules["rhythm_sync"]["max_violations"] = 3  # Invece di 2
channel.auto_approval_rules["temporary_block"]["max_block_duration_hours"] = 2  # Invece di 1

# Disabilita una regola
channel.auto_approval_rules["first_offense"]["enabled"] = False
```

## Troubleshooting

### Problema: Troppi False Positive

```python
# Soluzione 1: Rilassa harmony threshold
manager.rhythm_validator.harmony_threshold = 0.30  # Più permissivo

# Soluzione 2: Aumenta grace period
manager.blacklist.record_violation  # Modifica logica nella classe
```

### Problema: Sistema troppo permissivo

```python
# Soluzione: Abbassa threshold e riduci auto-approval
manager.rhythm_validator.harmony_threshold = 0.10  # Più strict
channel.auto_approval_rules["rhythm_sync"]["enabled"] = False
```

### Problema: Backup IPFS non funziona

```python
# Fallback: usa solo storage locale
from core.ipfs_pr_backup import IPFSPRBackupManager

manager = IPFSPRBackupManager()
# Il sistema usa automaticamente storage locale se IPFS non disponibile
```

## Best Practices

### 1. Gradualità
Inizia con modalità DORMANT, poi passa progressivamente a ACTIVE e VIGILANT.

### 2. Monitoring
Implementa sempre background monitoring per rilevare anomalie.

### 3. Logging
Controlla regolarmente i log per pattern e anomalie.

### 4. Compassione
Usa il rescue channel liberamente - è progettato per essere compassionevole.

### 5. Testing
Testa sempre in staging prima di produzione.

## Esempi Completi

Vedi:
- `core/lex_amoris_security.py` (demo in `__main__`)
- `core/lex_amoris_rescue.py` (demo in `__main__`)
- `core/ipfs_pr_backup.py` (demo in `__main__`)
- `core/test_lex_amoris_systems.py` (test completi)

## Supporto

Per domande o problemi:
1. Controlla i log in `logs/lex_amoris_*.log`
2. Esegui i test: `python core/test_lex_amoris_systems.py`
3. Consulta la documentazione completa: `docs/LEX_AMORIS_SECURITY.md`

---

**Ricorda**: Lex Amoris è sicurezza con cuore. Usalo saggiamente! 💚
