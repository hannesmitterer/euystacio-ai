Tech-Stack-Manifest, optimiert für deinen Root-Hub in Bolzano.

Alles hier ist darauf ausgelegt:
→ low-maintenance, edge-stabil, CGNAT-resilient

⚙️ 1. k3s DEPLOYMENT — ARGILLA-DISTRIBUTOR
📁 Verzeichnisstruktur (Host)
/opt/argilla/
├── app/
│   └── argilla_distributor.py
├── data/
│   └── sensor.db
🐍 Python Service (RS485 + SQLite + optional Influx)
import minimalmodbus
import sqlite3
import time
import requests

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
conn = sqlite3.connect('/data/sensor.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    timestamp TEXT,
    ph REAL,
    moisture REAL,
    temperature REAL,
    ec REAL
)
""")

INFLUX_URL = "http://influxdb:8086/write?db=argilla"

while True:
    try:
        ph = instrument.read_register(0, 2)
        moisture = instrument.read_register(1, 2)
        temp = instrument.read_register(2, 2)
        ec = instrument.read_register(3, 2)

        ts = time.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("INSERT INTO measurements VALUES (?,?,?,?,?)",
                       (ts, ph, moisture, temp, ec))
        conn.commit()

        # Optional Influx push
        line = f"soil ph={ph},moisture={moisture},temp={temp},ec={ec}"
        try:
            requests.post(INFLUX_URL, data=line, timeout=2)
        except:
            pass

        print(f"[OK] {ts}")

    except Exception as e:
        print("[ERR]", e)

    time.sleep(60)
📦 k3s Manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: argilla-distributor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: argilla
  template:
    metadata:
      labels:
        app: argilla
    spec:
      containers:
      - name: argilla
        image: python:3.11-slim
        command: ["python", "/app/argilla_distributor.py"]
        volumeMounts:
        - name: app
          mountPath: /app
        - name: data
          mountPath: /data
        securityContext:
          privileged: true
      volumes:
      - name: app
        hostPath:
          path: /opt/argilla/app
      - name: data
        hostPath:
          path: /opt/argilla/data
🌐 2. IPFS AUTO-PINNING (KUBO)
🔧 Systemd Service

/etc/systemd/system/ipfs-pinner.service

[Unit]
Description=IPFS Auto Pinner
After=network.target

[Service]
ExecStart=/usr/local/bin/ipfs_pinner.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
📜 Script
#!/bin/bash

DB="/opt/argilla/data/sensor.db"
LOG="/opt/ipfs_pins.log"

while true; do
    TS=$(date +%s)
    SNAP="/tmp/sensor_$TS.db"

    cp $DB $SNAP

    CID=$(ipfs add -q $SNAP)

    echo "$(date) $CID" >> $LOG

    # Optional: announce to peers
    ipfs pubsub pub argilla/pins "$CID"

    sleep 300
done
🧠 Optional (wichtig bei 3+ Nodes)

Auf anderen Nodes:

ipfs pubsub sub argilla/pins

→ automatische Replikation möglich

🔐 3. WIREGUARD MESH (CGNAT-READY)
🧭 Architektur

VPS = Relay (öffentlich erreichbar)

Root-Hub = stabiler Peer

Satelliten = verbinden sich über VPS

📍 Root-Hub wg0.conf
[Interface]
PrivateKey = ROOT_PRIVATE_KEY
Address = 10.10.0.1/24
DNS = 1.1.1.1

# VPS Relay
[Peer]
PublicKey = VPS_PUBLIC_KEY
Endpoint = VPS_IP:51820
AllowedIPs = 10.10.0.0/24
PersistentKeepalive = 25
☁️ VPS Relay
[Interface]
Address = 10.10.0.254/24
ListenPort = 51820
PrivateKey = VPS_PRIVATE_KEY

# Root
[Peer]
PublicKey = ROOT_PUBLIC_KEY
AllowedIPs = 10.10.0.1/32

# Satellite Example
[Peer]
PublicKey = NODE1_PUBLIC_KEY
AllowedIPs = 10.10.0.2/32
📡 Satelliten (Template)
[Interface]
PrivateKey = NODE_PRIVATE_KEY
Address = 10.10.0.X/24

[Peer]
PublicKey = VPS_PUBLIC_KEY
Endpoint = VPS_IP:51820
AllowedIPs = 10.10.0.0/24
PersistentKeepalive = 25
🛡️ 4. NSR-SHIELD (nftables — HARDENED)
/etc/nftables.conf
table inet filter {

  chain input {
    type filter hook input priority 0;

    ct state established,related accept
    iif lo accept

    # WireGuard
    udp dport 51820 accept

    # SSH (limit!)
    tcp dport 22 ct state new limit rate 10/minute accept

    # ICMP (optional debug)
    ip protocol icmp accept

    drop
  }

  chain forward {
    type filter hook forward priority 0;
    drop
  }

  chain output {
    type filter hook output priority 0;
    accept
  }
}
🔒 Optional Hardening
# Disable password SSH
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no

sudo systemctl restart ssh
⚡ SYSTEM-INTEGRATION

🚀 NÄCHSTER SCHRITT (EMPFEHLUNG)

Wenn dieser Node stabil ist, gehen wir direkt in:

👉 IPFS Cluster + automatische Replikationsstrategie für 12 Nodes

oder

👉 LoRaWAN Integration für Feldsensoren (großer Hebel!)

Du bist jetzt nicht mehr in der Konzeptphase.

Du bist im Deployment-Level eines echten dezentralen Systems.

Wenn du willst, begleite ich dich beim nächsten Schritt live durch die Skalierung.
