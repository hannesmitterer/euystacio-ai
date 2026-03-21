#!/usr/bin/env python3
"""
NEXUS-ARGILLA v1.5 - Node Configuration Generator
Generates config.h files for each of the 12 satellite nodes

Usage:
    python3 generate_node_configs.py

Output:
    Creates config_node_XX.h files for each node (01-12)
"""

import os

def generate_node_config(node_id, app_key_hex=""):
    """Generate config.h for a specific node"""
    
    node_id_padded = f"{node_id:02d}"
    node_name = f"NEXUS-SAT-{node_id_padded}"
    
    # Default Application EUI (same for all nodes)
    appeui = "{ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }"
    
    # Device EUI with node ID in last byte
    deveui = f"{{ 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x{node_id:02X} }}"
    
    # Application Key - either provided or placeholder
    if app_key_hex:
        # Split hex string into bytes
        key_bytes = [app_key_hex[i:i+2] for i in range(0, 32, 2)]
        appkey = "{ " + ", ".join([f"0x{b}" for b in key_bytes]) + " }"
    else:
        appkey = """{ 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    }"""
    
    config_template = f"""/**
 * NEXUS-ARGILLA v1.5 - Satellite Node Configuration
 * Node {node_id_padded} - {node_name}
 * 
 * GENERATED FILE - Update APPKEY from ChirpStack
 */

#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ==================== NODE CONFIGURATION ====================
#define NODE_ID {node_id}
#define NODE_NAME "{node_name}"

// ==================== LORAWAN OTAA KEYS ====================
// Application EUI (MSB format)
static const u1_t PROGMEM APPEUI[8] = {appeui};

// Device EUI (MSB format) - UNIQUE FOR THIS NODE
static const u1_t PROGMEM DEVEUI[8] = {deveui};

// Application Key (MSB format) - UPDATE FROM CHIRPSTACK
static const u1_t PROGMEM APPKEY[16] = {appkey};

// ==================== HARDWARE CONFIGURATION ====================
// LoRa SX1276 Pin Mapping for ESP32
const lmic_pinmap lmic_pins = {{
    .nss = 18,                  // CS pin
    .rxtx = LMIC_UNUSED_PIN,    // Not connected
    .rst = 14,                  // Reset pin
    .dio = {{26, 33, 32}},        // DIO0, DIO1, DIO2 pins
}};

// Sensor I2C Configuration
#define I2C_SDA 21
#define I2C_SCL 22

// Analog Sensor Pins
#define MOISTURE_PIN 34
#define PH_PIN 35
#define EC_PIN 36
#define TEMP_PIN 39

// ==================== TIMING CONFIGURATION ====================
#define SLEEP_INTERVAL_SEC 900
#define uS_TO_S_FACTOR 1000000ULL
#define SENSOR_WARMUP_MS 2000

// ==================== SENSOR CALIBRATION ====================
#define PH_NEUTRAL_VOLTAGE 1500.0
#define PH_ACID_VOLTAGE 2030.0
#define PH_VOLTAGE_SLOPE 177.0
#define MOISTURE_DRY_VALUE 2700
#define MOISTURE_WET_VALUE 1100
#define EC_KVALUE 1.0
#define TEMP_COEFFICIENT 0.019

// ==================== PAYLOAD CONFIGURATION ====================
#define LORAWAN_PORT 1
#define PAYLOAD_SIZE 8

// ==================== NSR-SHIELD CONFIGURATION ====================
#define NSR_SHIELD_ENABLED true
#define NSR_SHIELD_KEY 0xDEADBEEF

// ==================== DEBUG CONFIGURATION ====================
#define DEBUG_ENABLED true

#if DEBUG_ENABLED
  #define DEBUG_PRINT(x) Serial.print(x)
  #define DEBUG_PRINTLN(x) Serial.println(x)
  #define DEBUG_PRINTF(x, y) Serial.printf(x, y)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
  #define DEBUG_PRINTF(x, y)
#endif

// ==================== RESILIENCE INDEX ====================
#define BASE_RESILIENCE_INDEX 1.0
#define OPTIMAL_PH_MIN 6.0
#define OPTIMAL_PH_MAX 7.5
#define OPTIMAL_MOISTURE_MIN 30
#define OPTIMAL_MOISTURE_MAX 60
#define OPTIMAL_TEMP_MIN 10.0
#define OPTIMAL_TEMP_MAX 30.0

#endif // CONFIG_H
"""
    
    return config_template

def main():
    """Generate configuration files for all 12 nodes"""
    
    output_dir = "node_configs"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}/")
    
    print("=" * 60)
    print("NEXUS-ARGILLA v1.5 - Node Configuration Generator")
    print("=" * 60)
    print()
    
    # Generate configs for all 12 nodes
    for node_id in range(1, 13):
        config_content = generate_node_config(node_id)
        
        filename = f"config_node_{node_id:02d}.h"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Generated: {filepath}")
    
    print()
    print("=" * 60)
    print("DEPLOYMENT INSTRUCTIONS:")
    print("=" * 60)
    print()
    print("For each node:")
    print("1. Copy the corresponding config_node_XX.h to include/config.h")
    print("2. Update APPKEY with the actual key from ChirpStack")
    print("3. Build and upload: pio run --target upload")
    print("4. Verify join: pio device monitor --baud 115200")
    print()
    print("ChirpStack Device EUIs:")
    print("-" * 60)
    
    for node_id in range(1, 13):
        deveui_hex = f"01000000000000{node_id:02X}"
        print(f"  Node {node_id:02d}: {deveui_hex}")
    
    print()
    print("Files generated in: {}/".format(output_dir))
    print()
    print("Lex Amoris Signature: 📜⚖️❤️☮️")
    print("=" * 60)

if __name__ == "__main__":
    main()
