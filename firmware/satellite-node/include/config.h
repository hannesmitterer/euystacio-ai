/**
 * NEXUS-ARGILLA v1.5 - Satellite Node Configuration
 * Dezentrales Boden-Immunsystem (12 Satellite Nodes)
 * 
 * NSR-Shield / Lex Amoris
 * Owner: Hannes Mitterer (Seedbringer/Nexus)
 */

#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ==================== NODE CONFIGURATION ====================
// Each node has a unique ID (1-12)
// Update this for each satellite node deployment
#define NODE_ID 1

// Node naming convention: NEXUS-SAT-XX
#define NODE_NAME "NEXUS-SAT-01"

// ==================== LORAWAN OTAA KEYS ====================
// IMPORTANT: These keys must be unique per node
// Generate new keys in ChirpStack for each deployment

// Application EUI (MSB format)
static const u1_t PROGMEM APPEUI[8] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

// Device EUI (MSB format) - MUST BE UNIQUE PER NODE
// Example: Node 1 = { 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 }
static const u1_t PROGMEM DEVEUI[8] = { 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, NODE_ID };

// Application Key (MSB format) - MUST BE UNIQUE PER NODE
// This is a placeholder - REPLACE with actual key from ChirpStack
static const u1_t PROGMEM APPKEY[16] = { 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

// ==================== HARDWARE CONFIGURATION ====================
// LoRa SX1276 Pin Mapping for ESP32
const lmic_pinmap lmic_pins = {
    .nss = 18,                  // CS pin
    .rxtx = LMIC_UNUSED_PIN,    // Not connected
    .rst = 14,                  // Reset pin
    .dio = {26, 33, 32},        // DIO0, DIO1, DIO2 pins
};

// Sensor I2C Configuration
#define I2C_SDA 21
#define I2C_SCL 22

// Analog Sensor Pins
#define MOISTURE_PIN 34
#define PH_PIN 35
#define EC_PIN 36
#define TEMP_PIN 39

// ==================== TIMING CONFIGURATION ====================
// Deep sleep interval (15 minutes = 900 seconds)
#define SLEEP_INTERVAL_SEC 900
#define uS_TO_S_FACTOR 1000000ULL

// Sensor stabilization time (milliseconds)
#define SENSOR_WARMUP_MS 2000

// ==================== SENSOR CALIBRATION ====================
// pH Sensor Calibration (adjust based on your sensor)
#define PH_NEUTRAL_VOLTAGE 1500.0  // mV at pH 7.0
#define PH_ACID_VOLTAGE 2030.0     // mV at pH 4.0
#define PH_VOLTAGE_SLOPE 177.0     // mV per pH unit

// Moisture Sensor Calibration
#define MOISTURE_DRY_VALUE 2700    // ADC value in dry soil
#define MOISTURE_WET_VALUE 1100    // ADC value in wet soil

// EC Sensor Calibration
#define EC_KVALUE 1.0              // Cell constant

// Temperature compensation for EC
#define TEMP_COEFFICIENT 0.019     // 1.9% per °C

// ==================== PAYLOAD CONFIGURATION ====================
// LoRaWAN Port
#define LORAWAN_PORT 1

// Payload size (8 bytes as per specification)
#define PAYLOAD_SIZE 8

// ==================== NSR-SHIELD CONFIGURATION ====================
// NSR Shield enables cryptographic validation
#define NSR_SHIELD_ENABLED true

// Shield signature validation key
#define NSR_SHIELD_KEY 0xDEADBEEF

// ==================== DEBUG CONFIGURATION ====================
// Enable serial debug output
#define DEBUG_ENABLED true

// Debug macros
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
// Base resilience index for NSR Shield validation
#define BASE_RESILIENCE_INDEX 1.0

// Thresholds for soil health assessment
#define OPTIMAL_PH_MIN 6.0
#define OPTIMAL_PH_MAX 7.5
#define OPTIMAL_MOISTURE_MIN 30
#define OPTIMAL_MOISTURE_MAX 60
#define OPTIMAL_TEMP_MIN 10.0
#define OPTIMAL_TEMP_MAX 30.0

#endif // CONFIG_H
