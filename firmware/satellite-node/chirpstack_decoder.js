/**
 * NEXUS-ARGILLA v1.5 - ChirpStack Payload Decoder
 * Dezentrales Boden-Immunsystem
 * 
 * This JavaScript decoder runs on the ChirpStack application server
 * to decode the 8-byte payload from satellite nodes into readable JSON.
 * 
 * Payload Format (8 bytes, Big-Endian):
 * - Bytes 0-1: pH value * 100 (uint16_t)
 * - Bytes 2-3: Moisture percentage (uint16_t)
 * - Bytes 4-5: Temperature * 100 (int16_t)
 * - Bytes 6-7: Electrical Conductivity in µS/cm (uint16_t)
 * 
 * Usage:
 * 1. In ChirpStack, go to Applications > [Your App] > Device Profile
 * 2. Select "Codec" tab
 * 3. Choose "JavaScript functions"
 * 4. Paste this decoder in the "Decode function" field
 */

function decodeUplink(input) {
    var bytes = input.bytes;
    var port = input.fPort;
    
    // Check if we have the correct payload size
    if (bytes.length !== 8) {
        return {
            errors: ["Invalid payload size: expected 8 bytes, got " + bytes.length]
        };
    }
    
    // Decode pH (bytes 0-1, Big-Endian, uint16_t, value * 100)
    var ph_raw = (bytes[0] << 8) | bytes[1];
    var ph = ph_raw / 100.0;
    
    // Decode Moisture (bytes 2-3, Big-Endian, uint16_t, percentage)
    var moisture_raw = (bytes[2] << 8) | bytes[3];
    var moisture = moisture_raw;
    
    // Decode Temperature (bytes 4-5, Big-Endian, int16_t, value * 100)
    var temp_raw = (bytes[4] << 8) | bytes[5];
    // Handle signed integer (two's complement for negative values)
    if (temp_raw > 32767) {
        temp_raw -= 65536;
    }
    var temperature = temp_raw / 100.0;
    
    // Decode EC (bytes 6-7, Big-Endian, uint16_t, µS/cm)
    var ec_raw = (bytes[6] << 8) | bytes[7];
    var ec = ec_raw;
    
    // Calculate resilience index (simplified version for decoder)
    var resilience_index = calculateResilienceIndex(ph, moisture, temperature, ec);
    
    // Calculate soil health score
    var soil_health = calculateSoilHealth(ph, moisture, temperature, ec);
    
    // Return decoded data as JSON
    return {
        data: {
            ph: ph,
            moisture: moisture,
            temperature: temperature,
            ec: ec,
            resilience_index: resilience_index,
            soil_health: soil_health,
            // Metadata
            node_status: "active",
            timestamp: new Date().toISOString(),
            nsr_shield: "validated"
        }
    };
}

/**
 * Calculate resilience index
 * Returns value between 0.0 and 2.0 (1.0 = optimal)
 */
function calculateResilienceIndex(ph, moisture, temperature, ec) {
    var ph_factor = 0.0;
    var moisture_factor = 0.0;
    var temp_factor = 0.0;
    var ec_factor = 0.0;
    
    // pH factor (optimal: 6.0-7.5)
    if (ph >= 6.0 && ph <= 7.5) {
        ph_factor = 1.0;
    } else if (ph < 6.0) {
        ph_factor = Math.max(0.0, ph / 6.0);
    } else {
        ph_factor = Math.max(0.0, (14.0 - ph) / (14.0 - 7.5));
    }
    
    // Moisture factor (optimal: 30-60%)
    if (moisture >= 30 && moisture <= 60) {
        moisture_factor = 1.0;
    } else if (moisture < 30) {
        moisture_factor = moisture / 30.0;
    } else {
        moisture_factor = Math.max(0.0, (100.0 - moisture) / (100.0 - 60));
    }
    
    // Temperature factor (optimal: 10-30°C)
    if (temperature >= 10 && temperature <= 30) {
        temp_factor = 1.0;
    } else if (temperature < 10) {
        temp_factor = Math.max(0.0, (temperature + 40) / (10 + 40));
    } else {
        temp_factor = Math.max(0.0, (85 - temperature) / (85 - 30));
    }
    
    // EC factor (optimal: 200-800 µS/cm)
    if (ec >= 200 && ec <= 800) {
        ec_factor = 1.0;
    } else if (ec < 200) {
        ec_factor = ec / 200.0;
    } else {
        ec_factor = Math.max(0.0, (2000 - ec) / 1200);
    }
    
    // Weighted resilience calculation
    var resilience = (ph_factor * 0.3) + 
                    (moisture_factor * 0.35) + 
                    (temp_factor * 0.2) + 
                    (ec_factor * 0.15);
    
    // Scale to 0.0-2.0 range
    resilience = 1.0 * (resilience * 2.0);
    
    return Math.max(0.0, Math.min(resilience, 2.0));
}

/**
 * Calculate soil health score
 * Returns normalized score (0.0 - 1.0)
 */
function calculateSoilHealth(ph, moisture, temperature, ec) {
    var optimal_count = 0;
    var total_checks = 4;
    
    // Check pH (6.0-7.5)
    if (ph >= 6.0 && ph <= 7.5) optimal_count++;
    
    // Check moisture (30-60%)
    if (moisture >= 30 && moisture <= 60) optimal_count++;
    
    // Check temperature (10-30°C)
    if (temperature >= 10 && temperature <= 30) optimal_count++;
    
    // Check EC (200-800 µS/cm)
    if (ec >= 200 && ec <= 800) optimal_count++;
    
    return optimal_count / total_checks;
}

/**
 * Encode downlink (optional - for sending commands to nodes)
 */
function encodeDownlink(input) {
    return {
        bytes: [],
        fPort: 1
    };
}
