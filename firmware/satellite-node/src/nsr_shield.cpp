/**
 * NEXUS-ARGILLA v1.5 - NSR Shield Implementation
 * Natural Sovereignty & Resilience Shield
 * 
 * Implements cryptographic validation and resilience scoring
 */

#include "nsr_shield.h"

/**
 * Calculate resilience index based on sensor data
 * Returns value between 0.0 and 2.0
 * 1.0 = optimal conditions
 * < 1.0 = degraded conditions
 * > 1.0 = enhanced conditions
 */
float calculateResilienceIndex(const SensorData& data) {
    // Convert back to floating point
    float ph = data.ph / 100.0;
    float moisture = data.moisture;
    float temperature = data.temperature / 100.0;
    float ec = data.ec;
    
    // Calculate individual health factors (0.0 - 1.0)
    float ph_factor = 0.0;
    float moisture_factor = 0.0;
    float temp_factor = 0.0;
    float ec_factor = 0.0;
    
    // pH Factor: optimal at 6.0-7.5
    if (ph >= OPTIMAL_PH_MIN && ph <= OPTIMAL_PH_MAX) {
        ph_factor = 1.0;
    } else if (ph < OPTIMAL_PH_MIN) {
        ph_factor = max(0.0, ph / OPTIMAL_PH_MIN);
    } else {
        ph_factor = max(0.0, (14.0 - ph) / (14.0 - OPTIMAL_PH_MAX));
    }
    
    // Moisture Factor: optimal at 30-60%
    if (moisture >= OPTIMAL_MOISTURE_MIN && moisture <= OPTIMAL_MOISTURE_MAX) {
        moisture_factor = 1.0;
    } else if (moisture < OPTIMAL_MOISTURE_MIN) {
        moisture_factor = moisture / OPTIMAL_MOISTURE_MIN;
    } else {
        moisture_factor = max(0.0, (100.0 - moisture) / (100.0 - OPTIMAL_MOISTURE_MAX));
    }
    
    // Temperature Factor: optimal at 10-30°C
    if (temperature >= OPTIMAL_TEMP_MIN && temperature <= OPTIMAL_TEMP_MAX) {
        temp_factor = 1.0;
    } else if (temperature < OPTIMAL_TEMP_MIN) {
        temp_factor = max(0.0, (temperature + 40.0) / (OPTIMAL_TEMP_MIN + 40.0));
    } else {
        temp_factor = max(0.0, (85.0 - temperature) / (85.0 - OPTIMAL_TEMP_MAX));
    }
    
    // EC Factor: optimal at moderate levels (200-800 µS/cm)
    if (ec >= 200 && ec <= 800) {
        ec_factor = 1.0;
    } else if (ec < 200) {
        ec_factor = ec / 200.0;
    } else {
        ec_factor = max(0.0, (2000.0 - ec) / 1200.0);
    }
    
    // Calculate weighted resilience index
    // pH and moisture are most critical
    float resilience = (ph_factor * 0.3) + 
                      (moisture_factor * 0.35) + 
                      (temp_factor * 0.2) + 
                      (ec_factor * 0.15);
    
    // Scale to 0.0 - 2.0 range, centered at 1.0
    resilience = BASE_RESILIENCE_INDEX * (resilience * 2.0);
    
    return constrain(resilience, 0.0, 2.0);
}

/**
 * Validate sensor data integrity
 * Checks if sensor values are within reasonable ranges
 */
bool validateSensorData(const SensorData& data) {
    // Convert to float for validation
    float ph = data.ph / 100.0;
    float moisture = data.moisture;
    float temperature = data.temperature / 100.0;
    float ec = data.ec;
    
    // Check pH range (0-14)
    if (ph < 0.0 || ph > 14.0) {
        DEBUG_PRINTLN(F("Invalid pH value"));
        return false;
    }
    
    // Check moisture range (0-100%)
    if (moisture < 0 || moisture > 100) {
        DEBUG_PRINTLN(F("Invalid moisture value"));
        return false;
    }
    
    // Check temperature range (-40 to 85°C)
    if (temperature < -40.0 || temperature > 85.0) {
        DEBUG_PRINTLN(F("Invalid temperature value"));
        return false;
    }
    
    // Check EC range (0-10000 µS/cm)
    if (ec < 0 || ec > 10000) {
        DEBUG_PRINTLN(F("Invalid EC value"));
        return false;
    }
    
    return true;
}

/**
 * Generate NSR Shield signature for payload
 * Simple checksum-based signature for data integrity
 */
uint16_t generateNSRSignature(const uint8_t* payload, size_t length) {
    if (!NSR_SHIELD_ENABLED) {
        return 0;
    }
    
    uint16_t signature = NSR_SHIELD_KEY & 0xFFFF;
    
    // Calculate checksum
    for (size_t i = 0; i < length; i++) {
        signature ^= payload[i];
        signature = (signature << 1) | (signature >> 15); // Rotate left
    }
    
    return signature;
}

/**
 * Verify NSR Shield signature
 */
bool verifyNSRSignature(const uint8_t* payload, size_t length, uint16_t signature) {
    if (!NSR_SHIELD_ENABLED) {
        return true;
    }
    
    uint16_t calculated = generateNSRSignature(payload, length);
    return (calculated == signature);
}

/**
 * Calculate overall soil health score
 * Returns normalized score (0.0 - 1.0)
 */
float calculateSoilHealth(const SensorData& data) {
    float ph = data.ph / 100.0;
    float moisture = data.moisture;
    float temperature = data.temperature / 100.0;
    float ec = data.ec;
    
    int optimal_count = 0;
    int total_checks = 4;
    
    if (isOptimalPH(ph)) optimal_count++;
    if (isOptimalMoisture(moisture)) optimal_count++;
    if (isOptimalTemperature(temperature)) optimal_count++;
    if (isOptimalEC(ec)) optimal_count++;
    
    return (float)optimal_count / (float)total_checks;
}

/**
 * Check if pH is within optimal range
 */
bool isOptimalPH(float ph) {
    return (ph >= OPTIMAL_PH_MIN && ph <= OPTIMAL_PH_MAX);
}

/**
 * Check if moisture is within optimal range
 */
bool isOptimalMoisture(float moisture) {
    return (moisture >= OPTIMAL_MOISTURE_MIN && moisture <= OPTIMAL_MOISTURE_MAX);
}

/**
 * Check if temperature is within optimal range
 */
bool isOptimalTemperature(float temperature) {
    return (temperature >= OPTIMAL_TEMP_MIN && temperature <= OPTIMAL_TEMP_MAX);
}

/**
 * Check if EC is within optimal range
 */
bool isOptimalEC(float ec) {
    return (ec >= 200 && ec <= 800);
}
