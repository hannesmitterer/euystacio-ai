/**
 * NEXUS-ARGILLA v1.5 - Sensor Interface
 * Soil monitoring sensors for satellite nodes
 */

#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include "config.h"

// Sensor data structure
struct SensorData {
    uint16_t ph;          // pH value * 100 (e.g., 651 = pH 6.51)
    uint16_t moisture;    // Moisture percentage (0-100)
    int16_t temperature;  // Temperature * 100 (e.g., 1850 = 18.50°C)
    uint16_t ec;          // Electrical conductivity in µS/cm
};

// Initialize all sensors
void initSensors();

// Read all sensor values
SensorData readSensors();

// Individual sensor reading functions
float readPH();
float readMoisture();
float readTemperature();
float readEC(float temperature);

// Sensor calibration functions
void calibratePH();
void calibrateMoisture();
void calibrateEC();

// Utility functions
float mapFloat(float x, float in_min, float in_max, float out_min, float out_max);
uint16_t readAnalogAverage(uint8_t pin, uint8_t samples = 10);

#endif // SENSORS_H
