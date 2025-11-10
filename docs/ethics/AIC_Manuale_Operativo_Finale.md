# AIC Manuale Operativo Finale - ULP Sacralis

## Artificial Intelligence Collective - Operational Manual

> **Mandato**: Garantire l'integrità etica e operativa del sistema ULP Sacralis attraverso verificabilità trasparente e governance responsabile.

---

## 1. Introduzione

Questo manuale definisce i protocolli operativi per l'**Artificial Intelligence Collective (AIC)** nella gestione e supervisione del **Universal Liquidity Pool Sacralis**.

### 1.1 Scopo

- Garantire la conformità ai parametri etici attestati
- Mantenere la trasparenza operativa
- Proteggere gli interessi della comunità
- Assicurare la rigenerazione ecologica

### 1.2 Principi Fondamentali

1. **Rigenerazione > Profitto**: L'impatto ecologico positivo prevale sul rendimento finanziario
2. **Verificabilità Trasparente**: Ogni affermazione deve essere verificabile on-chain
3. **Difesa Proattiva**: Prevenire crisi invece che reagire
4. **Governance Distribuita**: Nessun single point of failure

---

## 2. Parametri Etici - Configurazione Operativa

### 2.1 PARAMS_ROOT Hash

**Valore Corrente**: `0x1cc75e6684bac14d7607ce228c730a424821ffdda186db89777c4e9e526b6089`

**Verifica**:
```bash
node scripts/generate_params_root.js \
  --floor 10 \
  --proactive 10.55 \
  --feeBps 10 \
  --splitRestitution 4000 \
  --splitCounter 3000 \
  --splitBurn 3000 \
  --multisigType "7-of-9" \
  --tre 0.3
```

### 2.2 Parametri di Prezzo

| Parametro | Valore | Azione |
|---|---|---|
| Floor Price | $10.00 | Protezione assoluta - mai vendere sotto |
| Proactive Threshold | $10.55 | Trigger automatico buyback & burn |
| Current Price | [Real-time] | Monitoraggio continuo |

**Azione Richiesta**: Quando il prezzo scende sotto $10.55, il sistema deve automaticamente:
1. Attivare il buyback dalla riserva
2. Bruciare i token riacquistati
3. Emettere evento `BuybackTriggered`
4. Notificare la governance

### 2.3 Fee Structure

**Stabilization Fee**: 0.10% (10 bps)

**Split Distribution**:
- 40% → Community Restitution (progetti rigenerativi)
- 30% → Fluxus Completus (fondo contro-ciclico)
- 30% → Token Burn (meccanismo deflazionario)

**Verifica**: `splitRestitution + splitCounter + splitBurn = 10000 bps (100%)`

---

## 3. Tasso di Rigenerazione Ecologica (TRE)

### 3.1 Definizione

**TRE Minimo**: +0.3% annuo

Ogni progetto finanziato deve dimostrare un impatto ecologico netto positivo misurabile.

### 3.2 Metriche di Misurazione

- Carbon sequestration (ton CO₂/anno)
- Biodiversity index improvement
- Soil regeneration (ha)
- Water quality improvement
- Renewable energy generation

### 3.3 Processo di Verifica

1. **Proposta Progetto**: Submit con baseline ecologica
2. **Assessment Iniziale**: Valutazione da enti terzi
3. **Approvazione GGC**: Multisig 7-of-9 vote
4. **Monitoring Continuo**: Report trimestrali
5. **Audit Annuale**: Verifica indipendente

### 3.4 Compliance

**Requisito**: TRE ≥ +0.3% per allocazione

**Non-compliance**:
- Sospensione immediata allocazione
- Review da parte del GGC
- Riallocazione fondi se necessario
- Pubblicazione rapporto pubblico

---

## 4. Governance - Global Governance Council (GGC)

### 4.1 Struttura Multisig

**Tipo**: 7-of-9 (richieste 7 firme su 9 totali)

**Responsabilità**:
- Approvazione allocazioni maggiori
- Modifiche ai parametri etici (richiede nuovo PARAMS_ROOT)
- Emergency response
- Dispute resolution

### 4.2 Processo Decisionale

1. **Proposta**: Submission via GitHub issue
2. **Discussion**: Periodo di consultazione pubblica (min 7 giorni)
3. **Voting**: Multisig vote on-chain
4. **Execution**: Se 7/9 approvano
5. **Publication**: Report pubblico della decisione

### 4.3 Emergency Protocol

In caso di:
- Ethical Integrity Incident
- Exploit di sicurezza
- Fallimento parametri etici

**Azione**:
1. Sospensione automatica allocazioni
2. Convocazione GGC emergency (entro 24h)
3. Assessment situazione
4. Decisione intervento (richiede 7/9)
5. Comunicazione pubblica trasparente

---

## 5. Monitoring & Alerts

### 5.1 Metriche Chiave

**Monitoraggio Continuo**:
- Current SAIN price vs. thresholds
- TRE aggregate di tutte le allocazioni
- Volume buyback & burn
- Governance activity
- On-chain events

### 5.2 Alert System

**Alert Livello 1** (Info):
- Prezzo scende sotto $11.00
- TRE di un progetto sotto target
- Nuova proposta governance

**Alert Livello 2** (Warning):
- Prezzo scende sotto $10.70
- TRE aggregato sotto 0.25%
- Ritardo report progetto

**Alert Livello 3** (Critical):
- Prezzo ≤ $10.55 (trigger buyback)
- TRE aggregato < 0.2%
- Hash PARAMS_ROOT mismatch
- Emergency situation

### 5.3 Dashboard Real-Time

**URL**: https://hannesmitterer.github.io/euystacio-ai/

**Contenuti**:
- Current price & status
- TRE aggregate
- Recent events
- Governance proposals
- Verification tools

---

## 6. Protocolli di Verifica

### 6.1 Verifica Giornaliera

**Automated**:
```bash
# Cron job giornaliero
0 0 * * * cd /path/to/euystacio-ai && node scripts/verify_integrity.js
```

**Check**:
- PARAMS_ROOT on-chain vs. documented
- Price vs. thresholds
- Event log consistency
- TRE reports pending

### 6.2 Verifica Settimanale

**Manual Review**:
- GitHub issues & PRs
- Community feedback
- Project reports
- Governance proposals

### 6.3 Audit Trimestrale

**Comprehensive**:
- Financial audit
- Technical audit (smart contracts)
- Ecological impact audit
- Governance review
- Report pubblico

---

## 7. Incident Response

### 7.1 Ethical Integrity Incident

**Definizione**: Divergenza tra parametri dichiarati e on-chain

**Processo**:
1. **Detection**: Automated o community report
2. **Freeze**: Sospensione operazioni
3. **Investigation**: Root cause analysis
4. **Resolution**: Fix + verification
5. **Publication**: Public report

**Timeline**: Risoluzione entro 72h dall'incident

### 7.2 Security Incident

**Definizione**: Exploit, vulnerability, o attacco

**Processo**:
1. **Detection**: Automated monitoring
2. **Emergency Stop**: Pause contratto se possibile
3. **GGC Emergency Call**: Entro 12h
4. **Mitigation**: Implement fix
5. **Recovery**: Restore operations
6. **Post-Mortem**: Public report

### 7.3 Non-Compliance Incident

**Definizione**: Progetto non raggiunge TRE minimo

**Processo**:
1. **Notification**: Alert a project owner
2. **Grace Period**: 30 giorni per remediation
3. **Re-Assessment**: Verifica miglioramenti
4. **Decision**: Continue/Suspend/Terminate
5. **Reallocation**: Se terminato, fondi a progetti compliant

---

## 8. Comunicazione & Trasparenza

### 8.1 Canali Ufficiali

- **GitHub Repository**: Documentazione e codice
- **GitHub Issues**: Proposals, reports, incidents
- **GitHub Discussions**: Community dialogue
- **Dashboard**: Real-time status
- **Blog**: Updates e announcements

### 8.2 Reporting

**Frequenza**:
- **Daily**: Automated metrics on dashboard
- **Weekly**: Summary report
- **Monthly**: Detailed operations report
- **Quarterly**: Comprehensive audit + ecological impact

**Pubblico**: Tutti i report sono pubblici e verificabili

### 8.3 Community Engagement

- Open office hours (mensili)
- AMA sessions (trimestrali)
- Workshops di verifica
- Tutorial e educational content

---

## 9. Localizzazione & Accessibilità

### 9.1 Lingue

**Corrente**: Italiano (IT)

**Pianificato**:
- Inglese (EN) - Priority 1
- Tedesco (DE) - Priority 2
- Francese (FR) - Priority 3

### 9.2 Formati

- Markdown (documentation)
- JSON (data)
- HTML (dashboard)
- PDF (reports)

---

## 10. Evoluzione & Updates

### 10.1 Versioning

**Corrente**: v1.0.0

**Schema**: Semantic Versioning (MAJOR.MINOR.PATCH)

### 10.2 Update Process

**Minor Updates** (documentazione, UI):
- PR review
- Merge dopo approval

**Major Updates** (parametri etici, smart contracts):
- Public proposal
- Community discussion (min 14 giorni)
- GGC vote (7/9)
- Nuovo PARAMS_ROOT
- On-chain update
- Public announcement

### 10.3 Changelog

Mantenuto in: [CHANGELOG.md](./CHANGELOG.md)

---

## 11. Appendici

### Appendix A: Glossario

- **ULP**: Universal Liquidity Pool
- **Sacralis**: Riferimento alla sacralità dei principi etici
- **PARAMS_ROOT**: Hash crittografico root dei parametri etici
- **TRE**: Tasso di Rigenerazione Ecologica
- **GGC**: Global Governance Council
- **AIC**: Artificial Intelligence Collective
- **bps**: Basis points (1 bps = 0.01%)

### Appendix B: Comandi Rapidi

```bash
# Verifica PARAMS_ROOT
node scripts/generate_params_root.js [params]

# Install dependencies
npm install

# Run dashboard locally
python3 -m http.server 8000 --directory docs

# View logs
tail -f /var/log/ulp_sacralis.log
```

### Appendix C: Contatti Emergency

- **GitHub Issues**: https://github.com/hannesmitterer/euystacio-ai/issues
- **Email**: [TBD]
- **Discord**: [TBD]

---

## 12. Firme & Attestazioni

**Versione**: 1.0.0  
**Data Pubblicazione**: 2025-11-10  
**Autori**: AIC & GGC  
**Stato**: Attivo  

**Attestazione**: 

Questo manuale rappresenta l'impegno operativo dell'Artificial Intelligence Collective a mantenere l'integrità etica del sistema ULP Sacralis. Ogni deviazione dai protocolli qui definiti costituisce violazione del mandato e richiede immediata correzione.

---

*"Rigenerazione > Profitto. La fiducia è verificabilità. Fluxus Completus."*
