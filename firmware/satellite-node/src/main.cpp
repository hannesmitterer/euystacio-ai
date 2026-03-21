/**
 * NEXUS-ARGILLA v1.5 - Satellite Node Main Firmware
 * Dezentrales Boden-Immunsystem (12 Satellite Nodes)
 * 
 * PROJECT: Decentralized Soil Immune System
 * GOAL: Physical & Digital Sovereignty (NSR-Shield / Lex Amoris)
 * OWNER: Hannes Mitterer (Seedbringer/Nexus)
 * 
 * This firmware implements:
 * - LoRaWAN OTAA authentication
 * - Deep sleep power management (15-minute intervals)
 * - 8-byte optimized payload transmission
 * - Multi-sensor soil monitoring (pH, moisture, temperature, EC)
 * - NSR-Shield cryptographic validation
 * 
 * Hardware Requirements:
 * - ESP32 development board
 * - SX1276 LoRa module
 * - pH sensor (analog)
 * - Soil moisture sensor (analog)
 * - Temperature sensor (analog)
 * - EC sensor (analog)
 * - Solar panel + battery (optional, for autonomous operation)
 */

#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include "config.h"
#include "sensors.h"
#include "nsr_shield.h"

// ==================== GLOBAL VARIABLES ====================

// Payload buffer (8 bytes as per specification)
static uint8_t mydata[PAYLOAD_SIZE];

// Job scheduler
static osjob_t sendjob;

// Transmission complete flag
static bool txComplete = false;

// Boot count (stored in RTC memory to survive deep sleep)
RTC_DATA_ATTR int bootCount = 0;

// ==================== LMIC CALLBACKS ====================

/**
 * Callback: Get Application EUI
 */
void os_getArtEui(u1_t* buf) {
    memcpy_P(buf, APPEUI, 8);
}

/**
 * Callback: Get Device EUI
 */
void os_getDevEui(u1_t* buf) {
    memcpy_P(buf, DEVEUI, 8);
}

/**
 * Callback: Get Application Key
 */
void os_getDevKey(u1_t* buf) {
    memcpy_P(buf, APPKEY, 16);
}

/**
 * Callback: LMIC Event Handler
 */
void onEvent(ev_t ev) {
    DEBUG_PRINT(os_getTime());
    DEBUG_PRINT(": ");
    
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            DEBUG_PRINTLN(F("EV_SCAN_TIMEOUT"));
            break;
            
        case EV_BEACON_FOUND:
            DEBUG_PRINTLN(F("EV_BEACON_FOUND"));
            break;
            
        case EV_BEACON_MISSED:
            DEBUG_PRINTLN(F("EV_BEACON_MISSED"));
            break;
            
        case EV_BEACON_TRACKED:
            DEBUG_PRINTLN(F("EV_BEACON_TRACKED"));
            break;
            
        case EV_JOINING:
            DEBUG_PRINTLN(F("EV_JOINING"));
            break;
            
        case EV_JOINED:
            DEBUG_PRINTLN(F("EV_JOINED"));
            {
                u4_t netid = 0;
                devaddr_t devaddr = 0;
                u1_t nwkKey[16];
                u1_t artKey[16];
                LMIC_getSessionKeys(&netid, &devaddr, nwkKey, artKey);
                DEBUG_PRINT(F("netid: "));
                DEBUG_PRINTLN(netid);
                DEBUG_PRINT(F("devaddr: "));
                DEBUG_PRINTLN(devaddr);
                DEBUG_PRINT(F("AppSKey: "));
                for (size_t i = 0; i < sizeof(artKey); ++i) {
                    if (i != 0) DEBUG_PRINT("-");
                    DEBUG_PRINTF("%02X", artKey[i]);
                }
                DEBUG_PRINTLN();
                DEBUG_PRINT(F("NwkSKey: "));
                for (size_t i = 0; i < sizeof(nwkKey); ++i) {
                    if (i != 0) DEBUG_PRINT("-");
                    DEBUG_PRINTF("%02X", nwkKey[i]);
                }
                DEBUG_PRINTLN();
            }
            // Disable link check validation (automatically enabled after join)
            LMIC_setLinkCheckMode(0);
            break;
            
        case EV_JOIN_FAILED:
            DEBUG_PRINTLN(F("EV_JOIN_FAILED"));
            break;
            
        case EV_REJOIN_FAILED:
            DEBUG_PRINTLN(F("EV_REJOIN_FAILED"));
            break;
            
        case EV_TXCOMPLETE:
            DEBUG_PRINTLN(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            if (LMIC.txrxFlags & TXRX_ACK) {
                DEBUG_PRINTLN(F("Received ack"));
            }
            if (LMIC.dataLen) {
                DEBUG_PRINT(F("Received "));
                DEBUG_PRINT(LMIC.dataLen);
                DEBUG_PRINTLN(F(" bytes of payload"));
            }
            // Mark transmission as complete
            txComplete = true;
            break;
            
        case EV_LOST_TSYNC:
            DEBUG_PRINTLN(F("EV_LOST_TSYNC"));
            break;
            
        case EV_RESET:
            DEBUG_PRINTLN(F("EV_RESET"));
            break;
            
        case EV_RXCOMPLETE:
            DEBUG_PRINTLN(F("EV_RXCOMPLETE"));
            break;
            
        case EV_LINK_DEAD:
            DEBUG_PRINTLN(F("EV_LINK_DEAD"));
            break;
            
        case EV_LINK_ALIVE:
            DEBUG_PRINTLN(F("EV_LINK_ALIVE"));
            break;
            
        case EV_TXSTART:
            DEBUG_PRINTLN(F("EV_TXSTART"));
            break;
            
        case EV_TXCANCELED:
            DEBUG_PRINTLN(F("EV_TXCANCELED"));
            break;
            
        case EV_RXSTART:
            break;
            
        case EV_JOIN_TXCOMPLETE:
            DEBUG_PRINTLN(F("EV_JOIN_TXCOMPLETE: no JoinAccept"));
            break;
            
        default:
            DEBUG_PRINT(F("Unknown event: "));
            DEBUG_PRINTLN((unsigned) ev);
            break;
    }
}

// ==================== DATA TRANSMISSION ====================

/**
 * Prepare and send sensor data
 */
void do_send(osjob_t* j) {
    // Check if there is not a current TX/RX job running
    if (LMIC.opmode & OP_TXRXPEND) {
        DEBUG_PRINTLN(F("OP_TXRXPEND, not sending"));
        return;
    }
    
    DEBUG_PRINTLN(F("=== Reading Sensors ==="));
    
    // Read all sensor values
    SensorData sensorData = readSensors();
    
    // Validate sensor data
    if (!validateSensorData(sensorData)) {
        DEBUG_PRINTLN(F("Sensor validation failed!"));
        // Still send, but mark as invalid in logs
    }
    
    // Calculate resilience index
    float resilience = calculateResilienceIndex(sensorData);
    DEBUG_PRINT(F("Resilience Index: "));
    DEBUG_PRINTLN(resilience);
    
    // Calculate soil health
    float soilHealth = calculateSoilHealth(sensorData);
    DEBUG_PRINT(F("Soil Health Score: "));
    DEBUG_PRINTLN(soilHealth);
    
    DEBUG_PRINTLN(F("=== Encoding Payload ==="));
    
    // Pack data into 8-byte payload (Big-Endian format)
    // Bytes 0-1: pH (uint16_t, value * 100)
    mydata[0] = (sensorData.ph >> 8) & 0xFF;
    mydata[1] = sensorData.ph & 0xFF;
    
    // Bytes 2-3: Moisture (uint16_t, percentage)
    mydata[2] = (sensorData.moisture >> 8) & 0xFF;
    mydata[3] = sensorData.moisture & 0xFF;
    
    // Bytes 4-5: Temperature (int16_t, value * 100)
    mydata[4] = (sensorData.temperature >> 8) & 0xFF;
    mydata[5] = sensorData.temperature & 0xFF;
    
    // Bytes 6-7: EC (uint16_t, µS/cm)
    mydata[6] = (sensorData.ec >> 8) & 0xFF;
    mydata[7] = sensorData.ec & 0xFF;
    
    // Print payload in hex
    DEBUG_PRINT(F("Payload (hex): "));
    for (int i = 0; i < PAYLOAD_SIZE; i++) {
        if (mydata[i] < 0x10) DEBUG_PRINT("0");
        DEBUG_PRINT(mydata[i], HEX);
        DEBUG_PRINT(" ");
    }
    DEBUG_PRINTLN();
    
    // Generate NSR Shield signature (optional validation layer)
    if (NSR_SHIELD_ENABLED) {
        uint16_t signature = generateNSRSignature(mydata, PAYLOAD_SIZE);
        DEBUG_PRINT(F("NSR Signature: 0x"));
        DEBUG_PRINTLN(signature, HEX);
    }
    
    DEBUG_PRINTLN(F("=== Sending Packet ==="));
    
    // Prepare upstream data transmission at the next possible time
    // Port 1, unconfirmed transmission (for low airtime usage)
    LMIC_setTxData2(LORAWAN_PORT, mydata, sizeof(mydata), 0);
    
    DEBUG_PRINTLN(F("Packet queued"));
}

// ==================== SETUP & MAIN LOOP ====================

/**
 * Setup function - runs once at boot
 */
void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    delay(1000); // Wait for serial to initialize
    
    DEBUG_PRINTLN();
    DEBUG_PRINTLN(F("========================================"));
    DEBUG_PRINTLN(F("  NEXUS-ARGILLA v1.5 Satellite Node"));
    DEBUG_PRINTLN(F("  Dezentrales Boden-Immunsystem"));
    DEBUG_PRINTLN(F("  NSR-Shield / Lex Amoris"));
    DEBUG_PRINTLN(F("========================================"));
    DEBUG_PRINT(F("Node: "));
    DEBUG_PRINTLN(NODE_NAME);
    DEBUG_PRINT(F("Node ID: "));
    DEBUG_PRINTLN(NODE_ID);
    
    // Increment boot count
    bootCount++;
    DEBUG_PRINT(F("Boot count: "));
    DEBUG_PRINTLN(bootCount);
    
    // Print wakeup reason
    esp_sleep_wakeup_cause_t wakeup_reason = esp_sleep_get_wakeup_cause();
    switch(wakeup_reason) {
        case ESP_SLEEP_WAKEUP_TIMER:
            DEBUG_PRINTLN(F("Wakeup: Timer"));
            break;
        case ESP_SLEEP_WAKEUP_EXT0:
            DEBUG_PRINTLN(F("Wakeup: External (RTC_IO)"));
            break;
        default:
            DEBUG_PRINTLN(F("Wakeup: Power On or Reset"));
            break;
    }
    
    DEBUG_PRINTLN(F("Initializing..."));
    
    // Initialize sensors
    initSensors();
    
    // Initialize LMIC
    os_init();
    
    // Reset LMIC state
    LMIC_reset();
    
    // Set clock error (helps with timing accuracy)
    // Default is 10% = 4000, reduce to 1% for better accuracy
    LMIC_setClockError(MAX_CLOCK_ERROR * 1 / 100);
    
    // Start job (sending automatically starts join)
    do_send(&sendjob);
    
    DEBUG_PRINTLN(F("Setup complete"));
}

/**
 * Main loop - runs continuously
 */
void loop() {
    // Execute LMIC scheduler
    os_runloop_once();
    
    // Check if transmission is complete
    if (txComplete) {
        DEBUG_PRINTLN(F("========================================"));
        DEBUG_PRINTLN(F("Transmission complete"));
        DEBUG_PRINTLN(F("Entering deep sleep..."));
        DEBUG_PRINT(F("Next transmission in "));
        DEBUG_PRINT(SLEEP_INTERVAL_SEC);
        DEBUG_PRINTLN(F(" seconds"));
        DEBUG_PRINTLN(F("========================================"));
        
        // Small delay to allow serial output to complete
        delay(100);
        
        // Configure deep sleep timer
        esp_sleep_enable_timer_wakeup(SLEEP_INTERVAL_SEC * uS_TO_S_FACTOR);
        
        // Enter deep sleep
        esp_deep_sleep_start();
        
        // Never reaches here - ESP32 will reset after deep sleep
    }
}
