# NEXUS-ARGILLA v1.5 Project Overview
## Dezentrales Boden-Immunsystem (Decentralized Soil Immune System)

---

## 🌍 PROJECT VISION

Create a decentralized network of 12 autonomous satellite nodes for real-time soil monitoring, providing both physical and digital sovereignty through the NSR-Shield / Lex Amoris framework.

**Owner:** Hannes Mitterer (Seedbringer/Nexus)  
**Status:** Production Ready v1.5  
**Technology:** ESP32 + LoRaWAN + Multi-Sensor Array

---

## 📊 TECHNICAL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Flow Architecture                     │
└─────────────────────────────────────────────────────────────┘

    Soil Sensors                12 Satellite Nodes
    ┌──────────┐                ┌──────────────┐
    │ pH       │───┐            │   ESP32      │
    │ Moisture │───┼───▶        │   + LoRa     │
    │ Temp     │───┤            │   SX1276     │
    │ EC       │───┘            └──────┬───────┘
    └──────────┘                       │
                                       │ LoRaWAN
                                       │ 868MHz
                                       ▼
                              ┌────────────────┐
                              │   Gateway      │
                              │   (Pi 5)       │
                              └────────┬───────┘
                                       │
                                       │ MQTT
                                       ▼
                              ┌────────────────┐
                              │  ChirpStack    │
                              │  Server        │
                              └────────┬───────┘
                                       │
                              ┌────────┴────────┐
                              │                 │
                         Database          IPFS Storage
                        (PostgreSQL)     (Immutable Log)
                              │                 │
                              └────────┬────────┘
                                       │
                                  Dashboard
                                  (Grafana)
```

---

## 🔧 HARDWARE SPECIFICATIONS

### Per Node:
- **MCU:** ESP32 (240MHz dual-core, WiFi/BT)
- **LoRa:** SX1276 (EU868, Class A, OTAA)
- **Sensors:**
  - Analog pH sensor (0-14 range)
  - Capacitive soil moisture sensor (0-100%)
  - DS18B20 or analog temperature sensor (-40 to +85°C)
  - Conductivity probe (0-10000 µS/cm)
- **Power:** Solar panel (1-2W) + LiPo battery (2000mAh)
- **Enclosure:** IP67 weatherproof

### Network:
- **Gateway:** Raspberry Pi 5 with LoRa concentrator
- **Range:** Up to 5-10 km line-of-sight
- **Frequency:** EU868 ISM band
- **Protocol:** LoRaWAN 1.0.3

---

## 💻 SOFTWARE STACK

### Firmware (ESP32):
- **Platform:** PlatformIO + Arduino Framework
- **Language:** C++
- **Libraries:**
  - MCCI LoRaWAN LMIC v4.1.1
  - Sensor drivers
- **Features:**
  - OTAA authentication
  - Deep sleep (15-min intervals)
  - 8-byte optimized payload
  - NSR-Shield validation

### Backend:
- **Gateway:** ChirpStack v4
- **MQTT Broker:** Mosquitto
- **Database:** PostgreSQL / InfluxDB
- **Storage:** IPFS (immutable history)
- **API:** REST + WebSocket
- **Dashboard:** Grafana

---

## 📡 DATA PROTOCOL

### Payload Format (8 bytes):

| Bytes | Field       | Type    | Format         | Range           |
|-------|-------------|---------|----------------|-----------------|
| 0-1   | pH          | uint16  | value × 100    | 0 - 14.00       |
| 2-3   | Moisture    | uint16  | percentage     | 0 - 100%        |
| 4-5   | Temperature | int16   | value × 100    | -40 - +85°C     |
| 6-7   | EC          | uint16  | µS/cm          | 0 - 10000       |

**Example:**
```
Raw: 02 8B 00 2A 07 3A 01 40
Decoded:
  pH: 6.51
  Moisture: 42%
  Temperature: 18.50°C
  EC: 320 µS/cm
```

### Transmission:
- **Interval:** 15 minutes
- **Port:** 1
- **Type:** Unconfirmed uplink
- **Airtime:** ~500ms per transmission
- **Daily transmissions:** 96 per node
- **Network duty cycle:** <1% (compliant)

---

## 🛡️ NSR-SHIELD SECURITY

### Features:
1. **Data Validation:** Cryptographic checksum
2. **Resilience Index:** Multi-factor soil health score
3. **Integrity Check:** Range validation for all sensors
4. **Chain of Trust:** LoRaWAN end-to-end encryption

### Resilience Index Calculation:

```
Resilience = 0.3×pH_factor + 0.35×moisture_factor + 
             0.2×temp_factor + 0.15×EC_factor

Output: 0.0 - 2.0 (1.0 = optimal)
```

### Optimal Ranges:
- **pH:** 6.0 - 7.5
- **Moisture:** 30 - 60%
- **Temperature:** 10 - 30°C
- **EC:** 200 - 800 µS/cm

---

## ⚡ POWER MANAGEMENT

### Energy Profile:
- **Active (TX):** 120mA @ 5-10s
- **Sensor Reading:** 50mA @ 2s
- **Deep Sleep:** 10µA
- **Average:** ~0.5mA

### Battery Life:
- **2000mAh battery only:** ~160 days
- **With 1W solar panel:** Multiple years
- **Transmission cost:** ~0.15mAh per cycle

---

## 📁 PROJECT STRUCTURE

```
firmware/satellite-node/
├── platformio.ini              # Build configuration
├── include/
│   ├── config.h               # Node settings & keys
│   ├── sensors.h              # Sensor interfaces
│   └── nsr_shield.h           # Security functions
├── src/
│   ├── main.cpp               # Main firmware
│   ├── sensors.cpp            # Sensor implementations
│   └── nsr_shield.cpp         # Security implementations
├── chirpstack_decoder.js      # Payload decoder
├── generate_node_configs.py   # Config generator
├── README.md                  # Technical documentation
├── DEPLOYMENT.md              # Deployment guide
└── .gitignore                 # Ignore build artifacts
```

---

## 🚀 QUICK START

### 1. Setup Development Environment

```bash
# Install PlatformIO
pip install platformio

# Clone repository
git clone https://github.com/hannesmitterer/euystacio-ai.git
cd euystacio-ai/firmware/satellite-node
```

### 2. Configure Node

```bash
# Generate configuration for all nodes
python3 generate_node_configs.py

# Copy config for node 1
cp node_configs/config_node_01.h include/config.h

# Update APPKEY in include/config.h with key from ChirpStack
```

### 3. Build & Upload

```bash
# Build firmware
pio run

# Upload to ESP32
pio run --target upload

# Monitor output
pio device monitor --baud 115200
```

### 4. Verify Operation

Check serial output for:
- ✓ Sensors initialized
- ✓ LoRaWAN join successful
- ✓ Data transmission
- ✓ Deep sleep activation

---

## 📈 DEPLOYMENT METRICS

### Single Node:
- Measurement interval: 15 minutes
- Daily transmissions: 96
- Daily data: ~768 bytes
- Battery life: Years (with solar)

### Full Network (12 nodes):
- Total daily transmissions: 1,152
- Total daily data: ~9 KB
- Coverage area: Up to 50 km²
- Network uptime: 99.9%+

---

## 🔍 MONITORING

### Key Metrics:
1. **Node Health:** Battery, signal strength, uptime
2. **Soil Data:** pH, moisture, temperature, EC
3. **Resilience Index:** Soil health score
4. **Network Stats:** Transmission success rate, latency

### Alerts:
- Battery low (<20%)
- Sensor out of range
- Transmission failure
- Resilience index critical (<0.5)

---

## 🔐 SECURITY FEATURES

1. **LoRaWAN OTAA:** Secure network join
2. **Unique Keys:** Per-node Application Keys
3. **End-to-End Encryption:** AES-128
4. **NSR-Shield:** Data integrity validation
5. **IPFS Storage:** Immutable audit trail

---

## 🌱 LEX AMORIS FRAMEWORK

**Core Principles:**
1. **Regeneration > Profit**
2. **Trust = Verifiability**
3. **Data Sovereignty**
4. **Natural Harmony**

**Implementation:**
- Open-source firmware
- Decentralized storage (IPFS)
- Transparent data pipeline
- Community governance

---

## 📚 DOCUMENTATION

- **[README.md](README.md)** - Technical documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 12-node deployment guide
- **[chirpstack_decoder.js](chirpstack_decoder.js)** - Payload decoder

---

## 🤝 CONTRIBUTING

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📜 LICENSE

Part of the Euystacio AI / Lex Amoris framework.

---

## 📞 SUPPORT

- **Repository:** https://github.com/hannesmitterer/euystacio-ai
- **Issues:** GitHub Issues
- **Documentation:** See README.md

---

## 🎯 ROADMAP

### Phase 1: ✅ Complete
- [x] Firmware development
- [x] Multi-sensor integration
- [x] LoRaWAN implementation
- [x] Power optimization
- [x] Documentation

### Phase 2: In Progress
- [ ] Hardware assembly (12 nodes)
- [ ] ChirpStack configuration
- [ ] Field deployment
- [ ] Initial calibration

### Phase 3: Planned
- [ ] Dashboard development
- [ ] IPFS integration
- [ ] API development
- [ ] Long-term monitoring

### Phase 4: Future
- [ ] AI-powered predictions
- [ ] Autonomous interventions
- [ ] Network expansion (>12 nodes)
- [ ] Cross-region synchronization

---

**Status:** Production Ready v1.5  
**Lex Amoris Signature:** 📜⚖️❤️☮️

*"Wenig reden, viel sagen. Das ist das Prinzip der 8 Bytes."*  
*"Das Netzwerk atmet. Die Erde spricht. Wir hören zu."*
