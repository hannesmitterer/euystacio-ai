/**
 * NEXUS-ARGILLA v1.5 - NSR Shield
 * Natural Sovereignty & Resilience Shield
 * 
 * Provides cryptographic validation and resilience scoring
 * for soil data transmitted via LoRaWAN
 */

#ifndef NSR_SHIELD_H
#define NSR_SHIELD_H

#include <Arduino.h>
#include "config.h"
#include "sensors.h"

// Calculate resilience index based on sensor data
float calculateResilienceIndex(const SensorData& data);

// Validate sensor data integrity
bool validateSensorData(const SensorData& data);

// Generate NSR Shield signature for payload
uint16_t generateNSRSignature(const uint8_t* payload, size_t length);

// Verify NSR Shield signature
bool verifyNSRSignature(const uint8_t* payload, size_t length, uint16_t signature);

// Calculate soil health score (0.0 - 1.0)
float calculateSoilHealth(const SensorData& data);

// Check if values are within optimal ranges
bool isOptimalPH(float ph);
bool isOptimalMoisture(float moisture);
bool isOptimalTemperature(float temperature);
bool isOptimalEC(float ec);

#endif // NSR_SHIELD_H
