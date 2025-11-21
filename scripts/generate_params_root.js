#!/usr/bin/env node

/**
 * ULP Sacralis - Ethical Parameters Root Hash Generator
 * 
 * This script generates a cryptographic hash (PARAMS_ROOT) of all ethical
 * and financial parameters governing the ULP Sacralis contract on Polygon.
 * 
 * Usage:
 *   node scripts/generate_params_root.js --floor 10 --proactive 10.55 --feeBps 10 \
 *     --splitRestitution 4000 --splitCounter 3000 --splitBurn 3000 --multisigType "7-of-9"
 * 
 * The output hash can be verified against the on-chain PARAMS_ROOT value
 * to ensure contract integrity and ethical compliance.
 */

const { ethers } = require('ethers');
const minimist = require('minimist');

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = minimist(process.argv.slice(2), {
    string: ['multisigType'],
    default: {
      floor: 10.0,
      proactive: 10.55,
      feeBps: 10,
      splitRestitution: 4000,
      splitCounter: 3000,
      splitBurn: 3000,
      multisigType: '7-of-9',
      tre: 0.3 // Tasso di Rigenerazione Ecologica (%)
    }
  });

  return {
    floorPrice: parseFloat(args.floor),
    proactiveThreshold: parseFloat(args.proactive),
    stabilizationFeeBps: parseInt(args.feeBps),
    splitRestitution: parseInt(args.splitRestitution),
    splitCounter: parseInt(args.splitCounter),
    splitBurn: parseInt(args.splitBurn),
    multisigType: args.multisigType,
    tre: parseFloat(args.tre)
  };
}

/**
 * Validate parameters
 */
function validateParams(params) {
  const errors = [];

  // Floor price validation
  if (params.floorPrice <= 0) {
    errors.push('Floor price must be positive');
  }

  // Proactive threshold must be above floor
  if (params.proactiveThreshold <= params.floorPrice) {
    errors.push('Proactive threshold must be greater than floor price');
  }

  // Fee validation
  if (params.stabilizationFeeBps < 0 || params.stabilizationFeeBps > 10000) {
    errors.push('Stabilization fee must be between 0 and 10000 bps (0-100%)');
  }

  // Fee split validation (must sum to 10000 = 100%)
  const totalSplit = params.splitRestitution + params.splitCounter + params.splitBurn;
  if (totalSplit !== 10000) {
    errors.push(`Fee splits must sum to 10000 (100%), got ${totalSplit}`);
  }

  // TRE validation
  if (params.tre < 0) {
    errors.push('TRE (Tasso di Rigenerazione Ecologica) must be non-negative');
  }

  if (errors.length > 0) {
    throw new Error('Parameter validation failed:\n  - ' + errors.join('\n  - '));
  }

  return true;
}

/**
 * Generate the PARAMS_ROOT hash using Ethereum's keccak256
 * 
 * This creates a deterministic hash of all ethical parameters,
 * enabling cryptographic verification of contract configuration.
 */
function generateParamsRoot(params) {
  // Encode parameters using ABI encoding for consistency
  const encoded = ethers.AbiCoder.defaultAbiCoder().encode(
    [
      'uint256',  // floorPrice (in cents, 10.00 USD = 1000)
      'uint256',  // proactiveThreshold (in cents)
      'uint256',  // stabilizationFeeBps
      'uint256',  // splitRestitution
      'uint256',  // splitCounter
      'uint256',  // splitBurn
      'string',   // multisigType
      'uint256'   // tre (in basis points, 0.3% = 30)
    ],
    [
      Math.round(params.floorPrice * 100),        // Convert to cents
      Math.round(params.proactiveThreshold * 100), // Convert to cents
      params.stabilizationFeeBps,
      params.splitRestitution,
      params.splitCounter,
      params.splitBurn,
      params.multisigType,
      Math.round(params.tre * 100)                // Convert to basis points
    ]
  );

  // Generate keccak256 hash
  const hash = ethers.keccak256(encoded);
  return hash;
}

/**
 * Format output for display
 */
function formatOutput(params, paramsRoot) {
  const output = {
    PARAMS_ROOT_CALCULATED: paramsRoot,
    parameters: {
      floorPrice: `${params.floorPrice.toFixed(2)} USD`,
      proactiveThreshold: `${params.proactiveThreshold.toFixed(2)} USD`,
      stabilizationFeeBps: `${params.stabilizationFeeBps} bps (${(params.stabilizationFeeBps / 100).toFixed(2)}%)`,
      feeSplit: {
        restitution: `${params.splitRestitution} bps (${(params.splitRestitution / 100).toFixed(2)}%)`,
        fluxusCompletus: `${params.splitCounter} bps (${(params.splitCounter / 100).toFixed(2)}%)`,
        burn: `${params.splitBurn} bps (${(params.splitBurn / 100).toFixed(2)}%)`
      },
      multisigGovernance: params.multisigType,
      tre: `${params.tre.toFixed(2)}% annuo`
    },
    verification: {
      message: 'Compare PARAMS_ROOT_CALCULATED with on-chain PARAMS_ROOT',
      instructions: [
        '1. Visit Polygonscan at the ULP Sacralis contract address',
        '2. Call getEthicalConfig() function',
        '3. Compare returned PARAMS_ROOT with PARAMS_ROOT_CALCULATED above',
        '4. If they match, ethical integrity is verified ✓',
        '5. If they differ, open an "Ethical Integrity Incident" issue'
      ]
    },
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  };

  return output;
}

/**
 * Main execution
 */
function main() {
  try {
    console.log('='.repeat(70));
    console.log('ULP Sacralis - Ethical Parameters Root Hash Generator');
    console.log('='.repeat(70));
    console.log();

    // Parse and validate parameters
    const params = parseArgs();
    console.log('Input Parameters:');
    console.log(JSON.stringify(params, null, 2));
    console.log();

    validateParams(params);
    console.log('✓ Parameter validation passed');
    console.log();

    // Generate PARAMS_ROOT
    const paramsRoot = generateParamsRoot(params);
    console.log('✓ PARAMS_ROOT generated');
    console.log();

    // Format and display output
    const output = formatOutput(params, paramsRoot);
    console.log('='.repeat(70));
    console.log('VERIFICATION OUTPUT');
    console.log('='.repeat(70));
    console.log(JSON.stringify(output, null, 2));
    console.log();
    console.log('='.repeat(70));
    console.log('Fluxus Completus - Rigenerazione > Profitto');
    console.log('='.repeat(70));

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { generateParamsRoot, validateParams, parseArgs };
