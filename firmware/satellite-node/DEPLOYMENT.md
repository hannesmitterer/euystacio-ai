# 12-Node Deployment Guide
## NEXUS-ARGILLA v1.5 - Dezentrales Boden-Immunsystem

This guide helps you deploy all 12 satellite nodes for complete soil monitoring coverage.

## DEPLOYMENT OVERVIEW

### Network Architecture

```
                    ┌──────────────────┐
                    │  ChirpStack      │
                    │  Application     │
                    │  Server          │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  LoRaWAN         │
                    │  Gateway         │
                    │  (Pi 5)          │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │ SAT-01  │        │ SAT-02  │   ...  │ SAT-12  │
    │ Node 1  │        │ Node 2  │        │ Node 12 │
    └─────────┘        └─────────┘        └─────────┘
```

## PRE-DEPLOYMENT CHECKLIST

### Hardware Preparation (Per Node)

- [ ] ESP32 development board
- [ ] SX1276 LoRa module
- [ ] pH sensor (analog)
- [ ] Soil moisture sensor (analog)
- [ ] Temperature sensor (analog)
- [ ] EC sensor (analog)
- [ ] Weatherproof enclosure
- [ ] Solar panel (1-2W) + battery (optional)
- [ ] Antenna for LoRa module

### Software Setup

- [ ] PlatformIO installed
- [ ] ChirpStack application server configured
- [ ] LoRaWAN gateway operational
- [ ] MQTT broker running (for data pipeline)

## STEP 1: CHIRPSTACK CONFIGURATION

### Create Device Profile

1. Log into ChirpStack
2. Go to **Device Profiles** > **Create**
3. Configure:
   - Name: `NEXUS-ARGILLA-Profile`
   - LoRaWAN MAC version: `1.0.3`
   - Region: `EU868`
   - Regional parameters revision: `A`
   - ADR: Enabled
   - Class: `A`
   - Device supports OTAA: Yes

### Add Payload Decoder

1. In Device Profile, go to **Codec** tab
2. Select **JavaScript functions**
3. Copy decoder from `chirpstack_decoder.js`
4. Save configuration

### Create Application

1. Go to **Applications** > **Create**
2. Name: `NEXUS-ARGILLA`
3. Description: `Dezentrales Boden-Immunsystem`

## STEP 2: NODE CONFIGURATION

### Generate Unique Keys for Each Node

For each of the 12 nodes, generate unique LoRaWAN credentials in ChirpStack:

#### Node 1 Example:
```
Device Name: NEXUS-SAT-01
Device EUI:  0100000000000001
Application Key: [Generate in ChirpStack]
```

#### Complete Node List:

| Node | Name        | Device EUI         | Status |
|------|-------------|--------------------|--------|
| 1    | NEXUS-SAT-01| 0100000000000001  | ⬜     |
| 2    | NEXUS-SAT-02| 0100000000000002  | ⬜     |
| 3    | NEXUS-SAT-03| 0100000000000003  | ⬜     |
| 4    | NEXUS-SAT-04| 0100000000000004  | ⬜     |
| 5    | NEXUS-SAT-05| 0100000000000005  | ⬜     |
| 6    | NEXUS-SAT-06| 0100000000000006  | ⬜     |
| 7    | NEXUS-SAT-07| 0100000000000007  | ⬜     |
| 8    | NEXUS-SAT-08| 0100000000000008  | ⬜     |
| 9    | NEXUS-SAT-09| 0100000000000009  | ⬜     |
| 10   | NEXUS-SAT-10| 010000000000000A  | ⬜     |
| 11   | NEXUS-SAT-11| 010000000000000B  | ⬜     |
| 12   | NEXUS-SAT-12| 010000000000000C  | ⬜     |

### Add Devices to ChirpStack

For each node:

1. Go to **Applications** > **NEXUS-ARGILLA** > **Devices** > **Create**
2. Fill in:
   - Device name: (e.g., `NEXUS-SAT-01`)
   - Device description: `Satellite Node 1`
   - Device EUI: (from table above)
   - Device profile: `NEXUS-ARGILLA-Profile`
3. Click **Create Device**
4. Go to **Keys (OTAA)** tab
5. Enter/Generate **Application Key**
6. Save the Application Key for firmware configuration

## STEP 3: FIRMWARE CONFIGURATION

### For Each Node:

1. **Update Node ID** in `include/config.h`:
   ```cpp
   #define NODE_ID 1  // Change: 1, 2, 3, ..., 12
   #define NODE_NAME "NEXUS-SAT-01"  // Update accordingly
   ```

2. **Update LoRaWAN Keys**:
   ```cpp
   // Application EUI (same for all nodes)
   static const u1_t PROGMEM APPEUI[8] = { 
       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 
   };
   
   // Device EUI (unique per node, MSB format)
   static const u1_t PROGMEM DEVEUI[8] = { 
       0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, NODE_ID 
   };
   
   // Application Key (from ChirpStack, MSB format)
   static const u1_t PROGMEM APPKEY[16] = { 
       0xXX, 0xXX, ... // Get from ChirpStack
   };
   ```

3. **Build Firmware**:
   ```bash
   cd firmware/satellite-node
   pio run
   ```

4. **Upload to ESP32**:
   ```bash
   pio run --target upload
   ```

5. **Verify Operation**:
   ```bash
   pio device monitor --baud 115200
   ```

6. **Check for successful join** in serial output and ChirpStack

## STEP 4: PHYSICAL DEPLOYMENT

### Installation Guidelines

1. **Site Selection**:
   - Choose representative soil locations
   - Ensure LoRa signal coverage (test with RF tool)
   - Spacing: 50-200m apart depending on field size
   - Consider solar panel orientation (south-facing in northern hemisphere)

2. **Sensor Installation**:
   - Insert sensors at consistent depth (10-20cm recommended)
   - Ensure good soil contact
   - Protect connections from moisture
   - Route cables to weatherproof enclosure

3. **Power Setup**:
   - Connect solar panel (if used)
   - Install battery in protected location
   - Verify voltage levels before final assembly

4. **Enclosure**:
   - Mount ESP32 and LoRa module securely
   - Ensure antenna has clear path (not blocked by metal)
   - Seal cable entry points
   - Add desiccant pack for moisture control

5. **Testing**:
   - Power on node
   - Monitor serial output for 1-2 cycles
   - Verify data appears in ChirpStack
   - Check payload decoding

## STEP 5: MONITORING & MAINTENANCE

### Dashboard Setup

Create monitoring dashboard in Grafana or similar:

- **Real-time Data**: Latest readings from all 12 nodes
- **Historical Trends**: pH, moisture, temperature, EC over time
- **Health Indicators**: Resilience index, soil health scores
- **Alerts**: Battery low, sensor malfunction, missed transmissions
- **Geographic View**: Map overlay with node locations

### Maintenance Schedule

| Task | Frequency | Description |
|------|-----------|-------------|
| Visual Inspection | Weekly | Check enclosures, connections |
| Sensor Cleaning | Monthly | Remove soil buildup |
| Calibration Check | Quarterly | Verify sensor accuracy |
| Battery Check | Monthly | Test voltage levels |
| Firmware Update | As needed | Bug fixes, new features |

### Troubleshooting Common Issues

#### Node Not Joining Network

1. Check ChirpStack device status
2. Verify LoRaWAN keys are correct
3. Test gateway reception
4. Check antenna connection
5. Verify node is in gateway range

#### Erratic Sensor Readings

1. Check sensor connections
2. Inspect for corrosion
3. Recalibrate sensors
4. Test with known samples

#### Battery Drain

1. Check solar panel output
2. Verify deep sleep is working
3. Review transmission frequency
4. Inspect for water ingress

## STEP 6: DATA PIPELINE INTEGRATION

### MQTT Bridge to Database

1. **Subscribe to ChirpStack MQTT**:
   ```python
   import paho.mqtt.client as mqtt
   
   broker = "localhost"
   topic = "application/+/device/+/event/up"
   
   client = mqtt.Client()
   client.connect(broker, 1883, 60)
   client.subscribe(topic)
   client.loop_forever()
   ```

2. **Store in Database** (SQLite/InfluxDB/PostgreSQL)

3. **IPFS Pinning** (for immutable history):
   ```bash
   # Snapshot database daily
   ipfs add --pin db_snapshot_$(date +%Y%m%d).db
   ```

### API Endpoints

Create REST API for data access:

```
GET /api/nodes              - List all nodes
GET /api/nodes/:id          - Get specific node data
GET /api/nodes/:id/latest   - Latest reading
GET /api/nodes/:id/history  - Historical data
GET /api/health             - Overall system health
```

## DEPLOYMENT VERIFICATION

After all nodes are deployed, verify:

- [ ] All 12 nodes appear in ChirpStack
- [ ] All nodes successfully joined network
- [ ] Data is being received regularly (every 15 minutes)
- [ ] Payload decoding works correctly
- [ ] Database is storing data
- [ ] Dashboard displays all nodes
- [ ] Alerts are configured
- [ ] Documentation is complete

## EXPECTED METRICS

### Per Node:
- **Transmission Interval**: 15 minutes
- **Payload Size**: 8 bytes
- **Airtime**: ~0.5 seconds per transmission
- **Daily Transmissions**: 96 per node
- **Daily Network Traffic**: ~9 KB per node

### Full Network (12 Nodes):
- **Daily Transmissions**: 1,152
- **Daily Data Volume**: ~108 KB
- **Monthly Data Volume**: ~3.2 MB
- **Battery Life** (with solar): Years
- **LoRaWAN Duty Cycle**: <1% (compliant)

## SECURITY CONSIDERATIONS

1. **LoRaWAN Security**:
   - Unique Application Keys per node
   - End-to-end encryption
   - OTAA for secure join

2. **NSR-Shield**:
   - Cryptographic payload validation
   - Data integrity verification
   - Resilience scoring

3. **Physical Security**:
   - Tamper-evident enclosures
   - Secure mounting
   - Hidden/protected antennas

## SCALING BEYOND 12 NODES

If expanding the network:

1. Additional nodes follow same process
2. Update NODE_ID (13, 14, 15...)
3. Generate new Device EUIs
4. Consider additional gateways for coverage
5. Monitor LoRaWAN duty cycle compliance
6. Review database scaling needs

---

**Deployment Support**: See main README.md for troubleshooting  
**Project Status**: Production Ready v1.5  
**Lex Amoris**: 📜⚖️❤️☮️

*"Das Netzwerk atmet. Die Erde spricht. Wir hören zu."*
