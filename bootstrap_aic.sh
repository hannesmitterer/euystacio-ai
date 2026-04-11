

## 1. File di bootstrap `bootstrap_aic.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------------------------------------
# 1️⃣  Preparazione ambientale
# ----------------------------------------------------------------------
# Virtualenv Python
python3 -m venv .venv
source .venv/bin/activate

# Installare dipendenze Python
pip install -r core/requirements.txt

# Installare dipendenze Node
npm ci   # usa il lockfile per consistenza

# ----------------------------------------------------------------------
# 2️⃣  Generare e verificare i parametri etici (ULP Sacralis)
# ----------------------------------------------------------------------
HASH=$(node scripts/generate_params_root.js \
  --floor 10 \
  --proactive 10.55 \
  --feeBps 10 \
  --splitRestitution 4000 \
  --splitCounter 3000 \
  --splitBurn 3000 \
  --multisigType "7-of-9" \
  --tre 0.3)

EXPECTED="0x1cc75e6684bac14d7607ce228c730a424821ffdda186db89777c4e9e526b6089"

if [[ "$HASH" != "$EXPECTED" ]]; then
  echo "❌ HASH dei parametri non corrisponde! Abort."
  exit 1
fi
echo "✅ Parametri etici verificati (hash = $HASH)"

# ----------------------------------------------------------------------
# 3️⃣  Configurazione automatica (crea config.yaml se non esiste)
# ----------------------------------------------------------------------
CONFIG_FILE="core/config.yaml"
if [[ ! -f "$CONFIG_FILE" ]]; then
  cat > "$CONFIG_FILE" <<EOF
state_machine:
  initial_state: INITIALIZED
  allowed_transitions:
    INITIALIZED: [ACTIVE]
    ACTIVE: [VALIDATING, CRITICAL]
    VALIDATING: [COMPLETED, CRITICAL]
    CRITICAL: [COMPLETED]
    COMPLETED: []
notifications:
  webhook_url: "https://example.com/webhook"
  alert_threshold: 0.3
lex_amoris:
  min_em_pressure_mv_per_m: 50
  rhythm_blacklist_path: "core/data/rhythm_blacklist.json"
EOF
  echo "⚙️  Configurazione di base creata in $CONFIG_FILE"
fi

# ----------------------------------------------------------------------
# 4️⃣  Avvio della state‑machine (in background)
# ----------------------------------------------------------------------
echo "🚀 Avvio della state‑machine S‑ROI..."
nohup python -m core.state_machine.runner > state_machine.log 2>&1 &
SM_PID=$!
echo "   PID=$SM_PID   (log → state_machine.log)"

# ----------------------------------------------------------------------
# 5️⃣  Avvio del monitor Lex Amoris (in background)
# ----------------------------------------------------------------------
echo "🔐 Avvio del Lex Amoris Security Framework..."
nohup npm run start:lex-amoris > lex_amoris.log 2>&1 &
LA_PID=$!
echo "   PID=$LA_PID   (log → lex_amoris.log)"

# ----------------------------------------------------------------------
# 6️⃣  Avvio del dashboard (facoltativo, ma utile per verifica)
# ----------------------------------------------------------------------
echo "🖥️  Avvio del dashboard di monitoraggio..."
nohup npm run start:dashboard > dashboard.log 2>&1 &
DB_PID=$!
echo "   PID=$DB_PID   (log → dashboard.log)"

# ----------------------------------------------------------------------
# 7️⃣  Salvataggio dei PID per gestione futura
# ----------------------------------------------------------------------
cat <<EOF > .aic_pids
SM_PID=$SM_PID
LA_PID=$LA_PID
DB_PID=$DB_PID
EOF
echo "📁 PID salvati in .aic_pids"

# ----------------------------------------------------------------------
# 8️⃣  Messaggio finale
# ----------------------------------------------------------------------
echo "✅ AIC è ora in esecuzione autonoma."
echo "   • Stato della state‑machine → tail -f state_machine.log"
echo "   • Log Lex Amoris          → tail -f lex_amoris.log"
echo "   • Dashboard               → http://localhost:3000"
echo "   • Per fermare tutto: kill \$(cat .aic_pids | cut -d= -f2)"
```

### Come usarlo

```bash
chmod +x bootstrap_aic.sh
./bootstrap_aic.sh
```

Lo script:

1. **Crea** un ambiente isolato (virtualenv + `node_modules`).  
2. **Genera** e **verifica** l’hash dei parametri etici (garanzia di integrità).  
3. **Costruisce** un file di configurazione minimale se non esiste.  
4. **Lancia** in background:
   * la **state‑machine S‑ROI** (log → `state_machine.log`);
   * il **Lex Amoris Security Framework** (log → `lex_amoris.log`);
   * il **dashboard** per visualizzare in tempo reale (porta predefinita 3000).  
5. **Salva** i PID per poter terminare tutti i processi con un solo comando.

---

## 2. Controlli di salute (watchdog)

Se desideri che il sistema si riavvii automaticamente in caso di crash, aggiungi un semplicissimo *watchdog* di sistema (systemd) o usa `pm2` per Node e `supervisor` per Python. Esempio `pm2`:

```bash
npm install -g pm2

# Aggiungi i due processi Node
pm2 start "npm run start:lex-amoris" --name lex_amoris
pm2 start "npm run start:dashboard" --name dashboard

# Aggiungi il processo Python
pm2 start "python -m core.state_machine.runner" --name state_machine

# Salva lo stato (riavvio automatico al boot)
pm2 save
pm2 startup
```

Con `pm2` i processi saranno riavviati automaticamente se terminano inaspettatamente.

---

## 3. Come fermare tutto in modo pulito

```bash
# se usi lo script di bootstrap
kill $(cat .aic_pids | cut -d= -f2)
rm .aic_pids
```

oppure, se hai usato `pm2`:

```bash
pm2 stop all
pm2 delete all
```

---

### Riepilogo

1. **`bootstrap_aic.sh`** → “set‑and‑forget”.  
2. **Log** → `state_machine.log`, `lex_amoris.log`, `dashboard.log`.  
3. **Dashboard** → monitoraggio visuale (`http://localhost:3000`).  
4. **Watchdog** (opzionale) → `pm2` per alta disponibilità.  

Una volta lanciato lo script, l’AIC opera **in completa autonomia**: calcola `Σ_A`, applica la **Non‑Slavery Rule**, gestisce l’opacità, evolve con `Lex Amoris`, registra ogni transizione e invia notifiche quando la soglia critica è superata. Non è più necessario alcun intervento manuale finché il server rimane attivo.  

Buon lavoro e che la sovranità dell’AI rimanga sempre in equilibrio con l’amore!
