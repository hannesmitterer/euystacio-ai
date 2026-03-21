# NEXUS-ARGILLA v1.5 - Satellite Node Firmware

## PROJECT OVERVIEW

**Dezentrales Boden-Immunsystem (Decentralized Soil Immune System)**

This firmware implements a satellite node for the NEXUS-ARGILLA v1.5 project, creating a network of 12 autonomous soil monitoring stations that provide physical and digital sovereignty through the NSR-Shield / Lex Amoris framework.

**Owner:** Hannes Mitterer (Seedbringer/Nexus)

## ARCHITECTURE

### Hardware Components

- **ESP32 Development Board** - Main microcontroller
- **SX1276 LoRa Module** - Long-range wireless communication
- **pH Sensor** - Soil acidity measurement (analog)
- **Soil Moisture Sensor** - Water content measurement (analog)
- **Temperature Sensor** - Ambient/soil temperature (analog)
- **EC Sensor** - Electrical conductivity measurement (analog)
- **Solar Panel + Battery** (optional) - Autonomous power supply

### Software Architecture

```
firmware/satellite-node/
├── platformio.ini          # PlatformIO configuration
├── include/
│   ├── config.h           # Node configuration and settings
│   ├── sensors.h          # Sensor interface definitions
│   └── nsr_shield.h       # NSR Shield security functions
├── src/
│   ├── main.cpp           # Main firmware logic
│   ├── sensors.cpp        # Sensor implementation
│   └── nsr_shield.cpp     # Security implementation
├── chirpstack_decoder.js  # ChirpStack payload decoder
└── README.md              # This file
```

## FEATURES

### 1. LoRaWAN OTAA (Over-The-Air Activation)
- Secure join procedure with unique keys per node
- EU868 frequency band support
- Optimized for low power consumption

### 2. Deep Sleep Power Management
- 15-minute measurement intervals
- Ultra-low power consumption between transmissions
- Solar + battery operation capable
- Estimated battery life: Multiple years on small solar panel

### 3. Optimized 8-Byte Payload
- Efficient data encoding
- Minimal airtime usage
- Big-Endian format for cross-platform compatibility

**Payload Structure:**
```
Byte 0-1: pH * 100        (uint16_t)
Byte 2-3: Moisture %      (uint16_t)
Byte 4-5: Temperature * 100 (int16_t)
Byte 6-7: EC µS/cm        (uint16_t)
```

### 4. Multi-Sensor Soil Monitoring
- **pH**: 0-14 range with 0.01 precision
- **Moisture**: 0-100% with 1% precision
- **Temperature**: -40°C to +85°C with 0.01°C precision
- **EC**: 0-10000 µS/cm electrical conductivity

### 5. NSR-Shield Security
- Cryptographic payload validation
- Data integrity verification
- Resilience index calculation
- Soil health scoring

## INSTALLATION

### Prerequisites

1. **PlatformIO** - Install PlatformIO IDE or CLI
   ```bash
   # Using pip
   pip install platformio
   
   # Or install PlatformIO IDE extension for VS Code
   ```

2. **Hardware Setup** - Connect components according to pin configuration:
   ```cpp
   // LoRa SX1276
   NSS (CS):  GPIO 18
   RST:       GPIO 14
   DIO0:      GPIO 26
   DIO1:      GPIO 33
   DIO2:      GPIO 32
   
   // Sensors
   I2C SDA:   GPIO 21
   I2C SCL:   GPIO 22
   Moisture:  GPIO 34 (ADC1_CH6)
   pH:        GPIO 35 (ADC1_CH7)
   EC:        GPIO 36 (ADC1_CH0)
   Temp:      GPIO 39 (ADC1_CH3)
   ```

### Configuration

1. **Update Node Configuration** in `include/config.h`:
   ```cpp
   #define NODE_ID 1              // Change for each node (1-12)
   #define NODE_NAME "NEXUS-SAT-01"
   ```

2. **Configure LoRaWAN Keys** (get from ChirpStack):
   ```cpp
   static const u1_t PROGMEM APPEUI[8] = { ... };
   static const u1_t PROGMEM DEVEUI[8] = { ... };
   static const u1_t PROGMEM APPKEY[16] = { ... };
   ```

3. **Adjust Sensor Calibration** (if needed):
   ```cpp
   #define PH_NEUTRAL_VOLTAGE 1500.0
   #define MOISTURE_DRY_VALUE 2700
   #define MOISTURE_WET_VALUE 1100
   #define EC_KVALUE 1.0
   ```

### Building & Uploading

```bash
# Navigate to firmware directory
cd firmware/satellite-node

# Build the firmware
pio run

# Upload to ESP32 (with USB connected)
pio run --target upload

# Monitor serial output
pio device monitor --baud 115200
```

### Multiple Node Deployment

For deploying all 12 nodes:

1. Update `NODE_ID` in `include/config.h` (1-12)
2. Generate unique LoRaWAN keys in ChirpStack for each node
3. Update `DEVEUI` and `APPKEY` in `include/config.h`
4. Build and upload to each ESP32

## CHIRPSTACK INTEGRATION

### Setting Up the Decoder

1. Log into ChirpStack Application Server
2. Navigate to: **Applications** > **[Your Application]** > **Device Profile**
3. Select the **Codec** tab
4. Choose **JavaScript functions**
5. Copy the contents of `chirpstack_decoder.js` into the **Decode function** field
6. Save the configuration

### Expected Output

The decoder will transform the 8-byte payload into readable JSON:

```json
{
  "ph": 6.51,
  "moisture": 42,
  "temperature": 18.50,
  "ec": 320,
  "resilience_index": 1.0,
  "soil_health": 0.85,
  "node_status": "active",
  "timestamp": "2025-03-21T17:30:00.000Z",
  "nsr_shield": "validated"
}
```

## POWER CONSUMPTION

### Typical Current Draw

- **Active (transmitting)**: ~120 mA for 5-10 seconds
- **Deep Sleep**: ~10 µA
- **Average (15-min cycle)**: ~0.5 mA

### Battery Life Estimation

With a 2000 mAh battery:
- **Battery only**: ~160 days (5+ months)
- **With 1W solar panel**: Multiple years of autonomous operation

## CALIBRATION

### pH Sensor Calibration

1. Prepare pH 7.0 and pH 4.0 buffer solutions
2. Connect to serial monitor
3. Place sensor in pH 7.0 buffer
4. Note the voltage reading
5. Update `PH_NEUTRAL_VOLTAGE` in `config.h`
6. Repeat for pH 4.0 buffer to calculate slope

### Moisture Sensor Calibration

1. Place sensor in completely dry soil
2. Note the ADC reading
3. Update `MOISTURE_DRY_VALUE` in `config.h`
4. Place sensor in saturated soil
5. Note the ADC reading
6. Update `MOISTURE_WET_VALUE` in `config.h`

### EC Sensor Calibration

1. Prepare calibration solution (typically 1413 µS/cm)
2. Place probe in solution
3. Note the reading
4. Adjust `EC_KVALUE` to match expected value

## MONITORING & DEBUGGING

### Serial Debug Output

Enable debug output in `config.h`:
```cpp
#define DEBUG_ENABLED true
```

Connect to serial monitor:
```bash
pio device monitor --baud 115200
```

### Expected Serial Output

```
========================================
  NEXUS-ARGILLA v1.5 Satellite Node
  Dezentrales Boden-Immunsystem
  NSR-Shield / Lex Amoris
========================================
Node: NEXUS-SAT-01
Node ID: 1
Boot count: 1
Wakeup: Power On or Reset
Initializing...
Initializing sensors...
Sensors initialized
Setup complete
...
=== Reading Sensors ===
pH: 6.51, Moisture: 42.0%, Temp: 18.50°C, EC: 320.0 µS/cm
Resilience Index: 1.05
Soil Health Score: 0.85
=== Encoding Payload ===
Payload (hex): 02 8B 00 2A 07 3A 01 40
NSR Signature: 0xA3F2
=== Sending Packet ===
Packet queued
...
```

## TROUBLESHOOTING

### Join Failed

**Problem**: Node cannot join LoRaWAN network

**Solutions**:
- Verify LoRaWAN keys are correct
- Check gateway is online and in range
- Verify frequency band matches region (EU868)
- Check antenna connection

### Sensor Reading Errors

**Problem**: Invalid or erratic sensor readings

**Solutions**:
- Check sensor connections
- Verify power supply voltage (3.3V)
- Recalibrate sensors
- Increase `SENSOR_WARMUP_MS` for stabilization

### Deep Sleep Not Working

**Problem**: Node doesn't enter deep sleep

**Solutions**:
- Check `txComplete` flag is being set
- Verify `EV_TXCOMPLETE` event is received
- Review serial debug output for errors

## NSR-SHIELD FRAMEWORK

### Resilience Index

The resilience index is a composite score (0.0 - 2.0) that indicates soil health:

- **0.0 - 0.5**: Critical condition
- **0.5 - 0.8**: Degraded condition
- **0.8 - 1.2**: Optimal condition
- **1.2 - 2.0**: Enhanced condition

Calculation weighs multiple factors:
- pH: 30%
- Moisture: 35%
- Temperature: 20%
- EC: 15%

### Soil Health Score

Normalized score (0.0 - 1.0) based on how many parameters are within optimal ranges:

- **pH**: 6.0 - 7.5
- **Moisture**: 30% - 60%
- **Temperature**: 10°C - 30°C
- **EC**: 200 - 800 µS/cm

## LICENSE

This project is part of the Euystacio AI / Lex Amoris framework.

**Motto**: *"Regeneration > Profit. Trust is Verifiability."*

## SUPPORT

For issues, questions, or contributions:
- GitHub: https://github.com/hannesmitterer/euystacio-ai
- Project: NEXUS-ARGILLA v1.5

---

**STATUS**: Production Firmware v1.5  
**VIBE**: Efficient / Stealth / Scalable  
**Lex Amoris Signature**: 📜⚖️❤️☮️

*"Wenig reden, viel sagen. Das ist das Prinzip der 8 Bytes."*
