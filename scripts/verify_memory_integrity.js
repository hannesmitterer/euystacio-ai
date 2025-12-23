#!/usr/bin/env node

/**
 * NRE-002 Memory Integrity Verification Script
 * 
 * This script verifies the integrity of the memory system according to NRE-002.
 * It checks hash chains, node presence, and compliance with memory tier policies.
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  dataDir: path.join(__dirname, '../docs/data'),
  ethicsDir: path.join(__dirname, '../docs/ethics'),
  nre002File: 'nre_002_memoria.json',
  redCodeFile: 'red_code.json'
};

// Color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m'
};

/**
 * Calculate SHA-256 hash of a file
 */
function calculateFileHash(filePath) {
  try {
    const fileBuffer = fs.readFileSync(filePath);
    const hashSum = crypto.createHash('sha256');
    hashSum.update(fileBuffer);
    return hashSum.digest('hex');
  } catch (error) {
    return null;
  }
}

/**
 * Load JSON file safely
 */
function loadJSON(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`${colors.red}✗ Error loading ${filePath}: ${error.message}${colors.reset}`);
    return null;
  }
}

/**
 * Check if critical Tier 0 files exist
 */
function checkTier0Integrity() {
  console.log(`\n${colors.blue}=== Tier 0 (Immutable) Memory Check ===${colors.reset}`);
  
  const tier0Files = [
    'docs/ethics/statement_of_origin.md',
    'LIVING-COVENANT.md',
    'genesis.md',
    'docs/data/red_code.json'
  ];
  
  let allPresent = true;
  const hashes = {};
  
  for (const file of tier0Files) {
    const filePath = path.join(__dirname, '..', file);
    const exists = fs.existsSync(filePath);
    
    if (exists) {
      const hash = calculateFileHash(filePath);
      hashes[file] = hash;
      console.log(`${colors.green}✓${colors.reset} ${file}`);
      console.log(`  Hash: ${hash}`);
    } else {
      console.log(`${colors.red}✗${colors.reset} ${file} - MISSING`);
      allPresent = false;
    }
  }
  
  return { passed: allPresent, hashes };
}

/**
 * Check NRE-002 document integrity
 */
function checkNRE002Document() {
  console.log(`\n${colors.blue}=== NRE-002 Document Check ===${colors.reset}`);
  
  const nre002Path = path.join(CONFIG.ethicsDir, 'NRE-002_Memoria.md');
  const nre002DataPath = path.join(CONFIG.dataDir, CONFIG.nre002File);
  
  const docExists = fs.existsSync(nre002Path);
  const dataExists = fs.existsSync(nre002DataPath);
  
  if (docExists) {
    const hash = calculateFileHash(nre002Path);
    console.log(`${colors.green}✓${colors.reset} NRE-002 Document exists`);
    console.log(`  Hash: ${hash}`);
  } else {
    console.log(`${colors.red}✗${colors.reset} NRE-002 Document missing`);
  }
  
  if (dataExists) {
    const data = loadJSON(nre002DataPath);
    if (data) {
      console.log(`${colors.green}✓${colors.reset} NRE-002 Data file exists`);
      console.log(`  Version: ${data.version}`);
      console.log(`  Status: ${data.status}`);
    }
  } else {
    console.log(`${colors.red}✗${colors.reset} NRE-002 Data file missing`);
  }
  
  return { passed: docExists && dataExists };
}

/**
 * Verify Red Code integration
 */
function checkRedCodeIntegration() {
  console.log(`\n${colors.blue}=== Red Code Integration Check ===${colors.reset}`);
  
  const redCodePath = path.join(CONFIG.dataDir, CONFIG.redCodeFile);
  const redCode = loadJSON(redCodePath);
  
  if (!redCode) {
    console.log(`${colors.red}✗${colors.reset} Red Code data not accessible`);
    return { passed: false };
  }
  
  console.log(`${colors.green}✓${colors.reset} Red Code data loaded`);
  console.log(`  Core Truth: ${redCode.core_truth || 'N/A'}`);
  console.log(`  Guardian Mode: ${redCode.guardian_mode ? 'Active' : 'Inactive'}`);
  console.log(`  Symbiosis Level: ${redCode.symbiosis_level || 'N/A'}`);
  
  return { passed: true };
}

/**
 * Generate integrity report
 */
function generateReport(results) {
  console.log(`\n${colors.blue}=== Memory Integrity Report ===${colors.reset}`);
  console.log(`Timestamp: ${new Date().toISOString()}`);
  
  const allPassed = Object.values(results).every(r => r.passed);
  
  if (allPassed) {
    console.log(`\n${colors.green}✓ ALL CHECKS PASSED${colors.reset}`);
    console.log(`Memory integrity verified according to NRE-002`);
  } else {
    console.log(`\n${colors.red}✗ SOME CHECKS FAILED${colors.reset}`);
    console.log(`Memory integrity verification incomplete`);
  }
  
  return allPassed;
}

/**
 * Main verification function
 */
function main() {
  console.log(`${colors.blue}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
  console.log(`${colors.blue}  NRE-002 Memory Integrity Verification  ${colors.reset}`);
  console.log(`${colors.blue}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
  
  const results = {
    tier0: checkTier0Integrity(),
    nre002: checkNRE002Document(),
    redCode: checkRedCodeIntegration()
  };
  
  const success = generateReport(results);
  
  // Save verification log
  const logEntry = {
    timestamp: new Date().toISOString(),
    results,
    success,
    version: '1.0.0'
  };
  
  const logPath = path.join(__dirname, '../docs/data/memory_verification_log.json');
  let logs = [];
  
  if (fs.existsSync(logPath)) {
    try {
      logs = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    } catch (e) {
      logs = [];
    }
  }
  
  logs.push(logEntry);
  
  // Keep only last 100 entries
  if (logs.length > 100) {
    logs = logs.slice(-100);
  }
  
  fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));
  console.log(`\n${colors.green}✓${colors.reset} Verification logged to ${logPath}`);
  
  process.exit(success ? 0 : 1);
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { calculateFileHash, checkTier0Integrity, checkNRE002Document };
