/**
 * NEXUS-ARGILLA v1.5 - Sensor Implementation
 * Soil monitoring sensors for satellite nodes
 * 
 * Implements sensor reading and calibration functions
 */

#include "sensors.h"
#include <Wire.h>

/**
 * Initialize all sensors
 */
void initSensors() {
    DEBUG_PRINTLN(F("Initializing sensors..."));
    
    // Initialize I2C for digital sensors
    Wire.begin(I2C_SDA, I2C_SCL);
    
    // Configure analog pins
    pinMode(MOISTURE_PIN, INPUT);
    pinMode(PH_PIN, INPUT);
    pinMode(EC_PIN, INPUT);
    pinMode(TEMP_PIN, INPUT);
    
    // Set ADC resolution (ESP32 supports 12-bit)
    analogReadResolution(12);
    
    // Allow sensors to stabilize
    delay(SENSOR_WARMUP_MS);
    
    DEBUG_PRINTLN(F("Sensors initialized"));
}

/**
 * Read all sensor values and return structured data
 */
SensorData readSensors() {
    SensorData data;
    
    DEBUG_PRINTLN(F("Reading sensors..."));
    
    // Read temperature first (needed for EC compensation)
    float temp = readTemperature();
    
    // Read all sensors
    float ph = readPH();
    float moisture = readMoisture();
    float ec = readEC(temp);
    
    // Convert to transmission format
    data.ph = (uint16_t)(ph * 100);              // pH * 100
    data.moisture = (uint16_t)moisture;          // Percentage
    data.temperature = (int16_t)(temp * 100);    // Temp * 100
    data.ec = (uint16_t)ec;                      // µS/cm
    
    DEBUG_PRINTF("pH: %.2f, Moisture: %.1f%%, Temp: %.2f°C, EC: %.1f µS/cm\n", 
                 ph, moisture, temp, ec);
    
    return data;
}

/**
 * Read pH value from analog sensor
 * Returns pH value (0-14)
 */
float readPH() {
    // Read analog value and average multiple samples
    uint16_t analogValue = readAnalogAverage(PH_PIN, 10);
    
    // Convert to voltage (ESP32 ADC: 12-bit, 0-3.3V, but typically calibrated to 0-3.0V)
    float voltage = (analogValue / 4095.0) * 3300.0; // mV
    
    // Calculate pH using linear calibration
    // pH = 7.0 + (voltage - neutral_voltage) / slope
    float ph = 7.0 + (voltage - PH_NEUTRAL_VOLTAGE) / PH_VOLTAGE_SLOPE;
    
    // Constrain to valid pH range
    ph = constrain(ph, 0.0, 14.0);
    
    return ph;
}

/**
 * Read soil moisture percentage
 * Returns moisture percentage (0-100)
 */
float readMoisture() {
    // Read analog value and average multiple samples
    uint16_t analogValue = readAnalogAverage(MOISTURE_PIN, 10);
    
    // Map analog value to percentage
    // Lower value = wetter soil, higher value = drier soil
    float moisture = mapFloat(analogValue, 
                              MOISTURE_WET_VALUE, MOISTURE_DRY_VALUE,
                              100.0, 0.0);
    
    // Constrain to valid range
    moisture = constrain(moisture, 0.0, 100.0);
    
    return moisture;
}

/**
 * Read temperature from analog sensor
 * Returns temperature in Celsius
 */
float readTemperature() {
    // Read analog value and average multiple samples
    uint16_t analogValue = readAnalogAverage(TEMP_PIN, 10);
    
    // Convert to voltage
    float voltage = (analogValue / 4095.0) * 3.3;
    
    // For typical analog temperature sensors (e.g., LM35, TMP36)
    // LM35: 10mV/°C, TMP36: offset 500mV, 10mV/°C
    // This assumes TMP36-like sensor
    float temperature = (voltage - 0.5) * 100.0;
    
    // Constrain to reasonable range
    temperature = constrain(temperature, -40.0, 85.0);
    
    return temperature;
}

/**
 * Read electrical conductivity with temperature compensation
 * Returns EC in µS/cm
 */
float readEC(float temperature) {
    // Read analog value and average multiple samples
    uint16_t analogValue = readAnalogAverage(EC_PIN, 10);
    
    // Convert to voltage
    float voltage = (analogValue / 4095.0) * 3.3;
    
    // Convert voltage to EC (sensor-specific calibration)
    // This is a simplified model - adjust based on your EC probe
    float ec_raw = voltage * 1000.0; // Basic conversion
    
    // Temperature compensation (25°C reference)
    float ec_compensated = ec_raw / (1.0 + TEMP_COEFFICIENT * (temperature - 25.0));
    
    // Apply K-value calibration
    ec_compensated *= EC_KVALUE;
    
    // Constrain to reasonable range
    ec_compensated = constrain(ec_compensated, 0.0, 10000.0);
    
    return ec_compensated;
}

/**
 * Read analog pin with averaging for stability
 */
uint16_t readAnalogAverage(uint8_t pin, uint8_t samples) {
    uint32_t sum = 0;
    
    for (uint8_t i = 0; i < samples; i++) {
        sum += analogRead(pin);
        delay(10); // Small delay between readings
    }
    
    return sum / samples;
}

/**
 * Map float values (like Arduino map but for floats)
 */
float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

/**
 * Calibrate pH sensor (interactive via serial)
 */
void calibratePH() {
    DEBUG_PRINTLN(F("pH Calibration Mode"));
    DEBUG_PRINTLN(F("Place sensor in pH 7.0 buffer solution"));
    // Implementation would involve reading values and storing calibration
    // This is a placeholder for the interactive calibration process
}

/**
 * Calibrate moisture sensor (interactive via serial)
 */
void calibrateMoisture() {
    DEBUG_PRINTLN(F("Moisture Calibration Mode"));
    DEBUG_PRINTLN(F("Place sensor in completely dry soil for dry calibration"));
    // Implementation would involve reading values and storing calibration
}

/**
 * Calibrate EC sensor (interactive via serial)
 */
void calibrateEC() {
    DEBUG_PRINTLN(F("EC Calibration Mode"));
    DEBUG_PRINTLN(F("Place sensor in calibration solution"));
    // Implementation would involve reading values and storing calibration
}
