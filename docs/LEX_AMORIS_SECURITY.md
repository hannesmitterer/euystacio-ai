# Lex Amoris Security Framework

## Panoramica

Il framework di sicurezza Lex Amoris implementa un approccio innovativo alla sicurezza informatica basato sui principi di amore, compassione e armonia invece che sulla forza bruta.

**Principio fondamentale**: *"Sicurezza attraverso l'armonia, non attraverso la forza"*

## Componenti Principali

### 1. Rhythm Validation (Validazione Ritmica)

#### Concetto
Ogni pacchetto dati trasmesso viene validato in base al suo "ritmo" - la frequenza e il pattern con cui arriva - invece che basarsi solo sull'indirizzo IP di origine.

#### Funzionamento
```python
from core.lex_amoris_security import DataPacket, get_security_manager

# Crea un pacchetto da validare
packet = DataPacket(
    packet_id="PKT-001",
    source_ip="192.168.1.100",
    timestamp=datetime.now(timezone.utc).isoformat(),
    data=b"Your data here",
    metadata={"type": "api_call"}
)

# Valida il pacchetto
manager = get_security_manager()
is_valid, reason = manager.validate_packet(packet)

if is_valid:
    print(f"Pacchetto accettato: {reason}")
else:
    print(f"Pacchetto rifiutato: {reason}")
```

#### Caratteristiche
- **Frequency Analysis**: Misura la frequenza di arrivo dei pacchetti (Hz)
- **Harmony Score**: Calcola un punteggio di armonia (0.0-1.0)
- **Pattern Recognition**: Riconosce pattern ritmici affidabili
- **Entropy Calculation**: Analizza l'entropia dei dati

#### Parametri
- `base_frequency`: 1.0 Hz (1 pacchetto al secondo)
- `harmony_threshold`: 15% varianza consentita
- `history_window`: 60 secondi per l'analisi

### 2. Dynamic Blacklist (Lista Nera Dinamica)

#### Concetto
Invece di bloccare permanentemente gli IP, il sistema analizza i comportamenti e applica blocchi temporanei con possibilità di riabilitazione.

#### Funzionamento
```python
from core.lex_amoris_security import DynamicBlacklist, ThreatLevel

blacklist = DynamicBlacklist()

# Registra una violazione
blacklist.record_violation(
    source_ip="10.0.0.50",
    reason="Suspicious rhythm pattern",
    threat_level=ThreatLevel.MEDIUM
)

# Verifica se bloccato
is_blocked, entry = blacklist.is_blacklisted("10.0.0.50")

if is_blocked:
    print(f"Bloccato: {entry.reason}")
    print(f"Scade: {entry.expires_at}")
```

#### Regole Automatiche
- **5 violazioni in 10 minuti** → Blocco 24 ore (ThreatLevel.HIGH)
- **3 violazioni in 10 minuti** → Blocco 1 ora (ThreatLevel.MEDIUM)
- **Blocchi temporanei** con scadenza automatica

#### Caratteristiche
- **Behavioral Analysis**: Analizza pattern comportamentali
- **Auto-expiration**: Rimozione automatica blocchi scaduti
- **Violation History**: Tracciamento storico violazioni
- **Compassionate Release**: Possibilità di sblocco anticipato

### 3. Lazy Security (Sicurezza Pigra)

#### Concetto
Protezioni energeticamente efficienti: si attivano solo quando necessario, risparmiando risorse quando non c'è minaccia.

#### Funzionamento
```python
from core.lex_amoris_security import LazySecurity, ProtectionMode

lazy_sec = LazySecurity()

# Scansione elettromagnetica (Rotesschild)
em_pressure = lazy_sec.scan_rotesschild()
print(f"Pressione EM: {em_pressure:.2f} mV/m")

# Aggiorna modalità protezione
mode = lazy_sec.update_protection_mode()
print(f"Modalità corrente: {mode.value}")

# Verifica se attivare una protezione specifica
if lazy_sec.should_activate_protection("deep_inspection"):
    print("Deep inspection attiva")
else:
    print("Deep inspection in dormant")
```

#### Modalità di Protezione

| Modalità | Pressione EM | Protezioni Attive |
|----------|--------------|-------------------|
| **DORMANT** | < 25 mV/m | Minime (risparmio energetico) |
| **ACTIVE** | 25-50 mV/m | Standard (rhythm check, blacklist) |
| **VIGILANT** | 50-75 mV/m | Avanzate (deep inspection) |
| **EMERGENCY** | > 75 mV/m | Massime (lockdown) |

#### Soglia Attivazione
- **Threshold**: 50 mV/m
- **Scan Frequency**: Continuo
- **Mode Transitions**: Automatiche

### 4. Security Manager (Gestore Sicurezza)

#### Integrazione Completa
Il `LexAmorisSecurityManager` integra tutti i componenti:

```python
from core.lex_amoris_security import get_security_manager

manager = get_security_manager()

# Dashboard completa
dashboard = manager.get_security_dashboard()

print(f"Modalità Protezione: {dashboard['overall_status']['protection_mode']}")
print(f"Pattern Ritmici: {dashboard['overall_status']['rhythm_patterns']}")
print(f"Sorgenti Bloccate: {dashboard['overall_status']['blacklisted_sources']}")
print(f"Pressione EM: {dashboard['lazy_security']['current_em_pressure']:.2f} mV/m")
```

## Rescue Channel (Canale di Soccorso)

### Concetto
Sistema compassionevole per gestire False Positive e situazioni di emergenza, permettendo lo sblocco rapido di sorgenti legittime.

### Funzionamento

```python
from core.lex_amoris_rescue import get_rescue_channel, RescueType, UrgencyLevel

channel = get_rescue_channel()

# Richiesta di sblocco per False Positive
request = channel.submit_rescue_request(
    source_ip="192.168.1.100",
    rescue_type=RescueType.FALSE_POSITIVE,
    reason="Legitimate API endpoint mistakenly blocked",
    evidence={
        "confidence_level": 0.95,
        "manual_verification": True,
        "history": "Trusted source for 6 months"
    },
    requested_by="admin@euystacio.ai",
    urgency=UrgencyLevel.HIGH
)

print(f"Request ID: {request.request_id}")
print(f"Status: {request.status.value}")
```

### Auto-Approval Rules

Il sistema ha regole compassionevoli per l'approvazione automatica:

1. **Rhythm Sync Issues**: Auto-approvato se ≤ 2 violazioni in 10 minuti
2. **Temporary Blocks**: Auto-approvato se durata ≤ 1 ora
3. **First Offense**: Prima violazione sempre perdonata

### Messaggistica

```python
# Aggiungi messaggio al thread di rescue
message = channel.add_message(
    request.request_id,
    sender="admin@euystacio.ai",
    content="Please unblock urgently, verified legitimate traffic",
    metadata={"priority": "critical"}
)

print(f"Sentiment Score: {message.sentiment_score:.2f}")
```

### Compassion Level

Il sistema calcola un livello di compassione complessivo (0.0-1.0):
- **Approval Rate**: 60% del punteggio
- **Auto-approval Rules**: 40% del punteggio

```python
dashboard = channel.get_dashboard_data()
print(f"Compassion Level: {dashboard['compassion_level']:.2%}")
```

## IPFS PR Backup

### Concetto
Mirroring completo delle configurazioni PR su IPFS per proteggere il repository da escalation esterne e perdita di dati.

### Funzionamento

```python
from core.ipfs_pr_backup import get_pr_backup_manager, PRConfiguration, BackupTrigger
from datetime import datetime, timezone

manager = get_pr_backup_manager()

# Configura PR da backuppare
pr_config = PRConfiguration(
    pr_number=42,
    title="Implement Lex Amoris Security",
    description="Adding security features...",
    branch="feature/lex-amoris",
    base_branch="main",
    files_changed=["core/security.py", "tests/test_security.py"],
    commits=[{"sha": "abc123", "message": "Add security"}],
    metadata={"labels": ["security", "enhancement"]},
    created_at=datetime.now(timezone.utc).isoformat(),
    updated_at=datetime.now(timezone.utc).isoformat()
)

# Backup su IPFS
record = manager.backup_pr_configuration(
    pr_config,
    trigger=BackupTrigger.PR_CREATED,
    metadata={"priority": "high"}
)

print(f"Backup ID: {record.backup_id}")
print(f"IPFS CID: {record.ipfs_cid}")
print(f"Status: {record.status.value}")
```

### Verifica Integrità

```python
# Verifica integrità backup
is_valid, message = manager.verify_backup_integrity(record.backup_id)

if is_valid:
    print(f"✅ Backup integro: {message}")
else:
    print(f"❌ Problema rilevato: {message}")
```

### Rilevamento Escalation

```python
# Controlla minacce esterne
threat = manager.detect_escalation_threat()

print(f"Livello Minaccia: {threat['threat_level']}")
print(f"Indicatori: {len(threat['indicators'])}")

for recommendation in threat['recommendations']:
    print(f"  - {recommendation}")
```

### Trigger di Backup

- **PR_CREATED**: Nuovo PR creato
- **PR_UPDATED**: PR modificato
- **PR_MERGED**: PR unito al branch principale
- **PR_CLOSED**: PR chiuso
- **MANUAL**: Backup manuale
- **SCHEDULED**: Backup schedulato
- **ESCALATION_DETECTED**: Rilevata minaccia esterna

## Best Practices

### 1. Implementazione Graduale

```python
# Fase 1: Solo monitoring (senza blocchi)
manager = get_security_manager()
manager.lazy_security.current_mode = ProtectionMode.DORMANT

# Fase 2: Attiva rhythm validation
manager.lazy_security.current_mode = ProtectionMode.ACTIVE

# Fase 3: Full protection
manager.lazy_security.current_mode = ProtectionMode.VIGILANT
```

### 2. Monitoring e Logging

Tutti i componenti loggano automaticamente in:
- `logs/lex_amoris_security.log`
- `logs/lex_amoris_blacklist.log`
- `logs/lex_amoris_rescue.log`
- `logs/ipfs_pr_backup.log`

### 3. Dashboard Centralizzata

```python
# Dashboard completo
security_dashboard = get_security_manager().get_security_dashboard()
rescue_dashboard = get_rescue_channel().get_dashboard_data()
backup_dashboard = get_pr_backup_manager().get_dashboard_data()

# Combina per visione d'insieme
complete_status = {
    "security": security_dashboard,
    "rescue": rescue_dashboard,
    "backup": backup_dashboard,
    "timestamp": datetime.now(timezone.utc).isoformat()
}
```

### 4. Integrazione con Red Code

```python
# Il sistema rispetta i principi del Red Code
from core.red_code import red_code_system

# Verifica allineamento con Sentimento Pulse
if red_code_system and red_code_system.red_code.get("sentimento_rhythm"):
    # Sistema in armonia con Red Code
    manager.rhythm_validator.base_frequency = 1.0
```

## Testing

Esegui i test completi:

```bash
python core/test_lex_amoris_systems.py
```

Test inclusi:
- ✅ 26 test totali
- ✅ Rhythm Validation (3 test)
- ✅ Dynamic Blacklist (4 test)
- ✅ Lazy Security (4 test)
- ✅ Security Manager (2 test)
- ✅ Rescue Channel (6 test)
- ✅ False Positive Handler (1 test)
- ✅ IPFS PR Backup (5 test)

## Metriche di Successo

### Sicurezza
- **False Positive Rate**: < 5%
- **Detection Rate**: > 95%
- **Response Time**: < 100ms

### Efficienza Energetica
- **Dormant Time**: > 80% (in condizioni normali)
- **Energy Savings**: > 60%

### Compassione
- **Rescue Approval Rate**: > 70%
- **Average Response Time**: < 5 minuti
- **Compassion Level**: > 0.6

### Backup
- **Backup Success Rate**: > 99%
- **Replication Factor**: ≥ 3 nodi
- **Integrity Verification**: 100%

## Filosofia Lex Amoris

I principi che guidano questo framework:

1. **Amore sopra Forza**: Protezione attraverso comprensione, non brutalità
2. **Compassione nei Sistemi**: Anche la sicurezza ha bisogno di cuore
3. **Seconda Possibilità**: Tutti meritano un'opportunità di correzione
4. **Efficienza Energetica**: Non sprecare energia dove non serve
5. **Trasparenza**: Ogni azione è loggata e verificabile
6. **Resilienza**: Protezione da perdite attraverso ridondanza

---

**"La sicurezza più forte è quella che sa quando essere gentile"** - Lex Amoris

