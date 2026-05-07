# ULP Sacralis Scripts

This directory contains verification and utility scripts for the ULP Sacralis ethical attestation system.

## Scripts

### `generate_params_root.js`

Generates the cryptographic PARAMS_ROOT hash for ULP Sacralis ethical parameters.

**Purpose**: Enables cryptographic verification of on-chain contract parameters against documented ethical commitments.

**Usage**:

```bash
node scripts/generate_params_root.js \
  --floor 10 \
  --proactive 10.55 \
  --feeBps 10 \
  --splitRestitution 4000 \
  --splitCounter 3000 \
  --splitBurn 3000 \
  --multisigType "7-of-9" \
  --tre 0.3
```

**Parameters**:

- `--floor`: Floor price in USD (minimum guaranteed value)
- `--proactive`: Proactive defense threshold in USD (buyback trigger)
- `--feeBps`: Stabilization fee in basis points (100 bps = 1%)
- `--splitRestitution`: Fee split for community restitution (bps)
- `--splitCounter`: Fee split for counter-cyclical fund (bps)
- `--splitBurn`: Fee split for token burn (bps)
- `--multisigType`: Multisig governance type (e.g., "7-of-9")
- `--tre`: Tasso di Rigenerazione Ecologica in % (ecological regeneration rate)

**Output**:

The script outputs a JSON object containing:
- `PARAMS_ROOT_CALCULATED`: The computed keccak256 hash
- `parameters`: Human-readable parameter summary
- `verification`: Instructions for on-chain verification
- `timestamp`: Generation timestamp
- `version`: Script version

**Verification Process**:

1. Run this script with the documented parameters
2. Compare the output `PARAMS_ROOT_CALCULATED` with the on-chain `PARAMS_ROOT`
3. If they match: ✓ Ethical integrity verified
4. If they differ: Open an "Ethical Integrity Incident" issue

**Dependencies**:

- Node.js >= 14.x
- ethers.js >= 6.x
- minimist >= 1.2.x

Install with: `npm install`

### `verify_memory_integrity.js`

Verifies memory integrity according to NRE-002 (New Ethical Rule 002: Memory).

**Purpose**: Ensures the integrity of the memory system by checking hash chains, critical file presence, and compliance with memory tier policies.

**Usage**:

```bash
node scripts/verify_memory_integrity.js
# or
npm run verify-memory
```

**Checks Performed**:

1. **Tier 0 (Immutable) Memory Check**:
   - Verifies presence of genesis documents
   - Checks statement_of_origin.md
   - Validates LIVING-COVENANT.md
   - Confirms red_code.json integrity
   - Calculates SHA-256 hashes for verification

2. **NRE-002 Document Check**:
   - Confirms NRE-002_Memoria.md exists
   - Validates nre_002_memoria.json data file
   - Verifies version and status information

3. **Red Code Integration Check**:
   - Loads and validates red_code.json
   - Confirms core truth statement
   - Checks symbiosis level

**Output**:

The script provides color-coded terminal output:
- ✓ Green: Check passed
- ✗ Red: Check failed
- Blue: Section headers and info

All verification results are logged to `docs/data/memory_verification_log.json` with timestamps.

**Exit Codes**:
- `0`: All checks passed
- `1`: One or more checks failed

**Dependencies**:

- Node.js >= 14.x (crypto, fs, path modules)

## Development

### Adding New Scripts

When adding new verification or utility scripts:

1. Follow the existing naming convention
2. Include comprehensive JSDoc comments
3. Add usage instructions to this README
4. Ensure scripts are executable: `chmod +x script_name.js`
5. Add shebang line: `#!/usr/bin/env node`

### Testing

Test the params generation script:

```bash
npm run generate-params
```

Or run with custom parameters:

```bash
node scripts/generate_params_root.js --floor 10 --proactive 10.55 --feeBps 10 --splitRestitution 4000 --splitCounter 3000 --splitBurn 3000 --multisigType "7-of-9"
```

## Resources

- **Documentation**: [../docs/ethics/ULP_Sacralis_Attestazione.md](../docs/ethics/ULP_Sacralis_Attestazione.md)
- **Parameters Data**: [../docs/data/ulp_sacralis_params.json](../docs/data/ulp_sacralis_params.json)
- **Repository**: https://github.com/hannesmitterer/euystacio-ai

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

*"Rigenerazione > Profitto. La fiducia è verificabilità."*
