/**
 * Simple test to verify generate_params_root.js works correctly
 */

const { generateParamsRoot, validateParams } = require('./generate_params_root.js');

console.log('Testing ULP Sacralis PARAMS_ROOT Generator...\n');

// Test 1: Valid parameters
console.log('Test 1: Valid parameters');
try {
    const validParams = {
        floorPrice: 10.0,
        proactiveThreshold: 10.55,
        stabilizationFeeBps: 10,
        splitRestitution: 4000,
        splitCounter: 3000,
        splitBurn: 3000,
        multisigType: '7-of-9',
        tre: 0.3
    };
    
    validateParams(validParams);
    const hash = generateParamsRoot(validParams);
    console.log('✓ Validation passed');
    console.log('✓ Generated hash:', hash);
    console.log('✓ Expected hash: 0x1cc75e6684bac14d7607ce228c730a424821ffdda186db89777c4e9e526b6089');
    
    if (hash === '0x1cc75e6684bac14d7607ce228c730a424821ffdda186db89777c4e9e526b6089') {
        console.log('✓ Hash matches expected value!\n');
    } else {
        console.log('✗ Hash does NOT match expected value!\n');
        process.exit(1);
    }
} catch (error) {
    console.log('✗ Test failed:', error.message);
    process.exit(1);
}

// Test 2: Invalid parameters - proactive threshold too low
console.log('Test 2: Invalid parameters (proactive < floor)');
try {
    const invalidParams = {
        floorPrice: 10.0,
        proactiveThreshold: 9.0, // Invalid: should be > floor
        stabilizationFeeBps: 10,
        splitRestitution: 4000,
        splitCounter: 3000,
        splitBurn: 3000,
        multisigType: '7-of-9',
        tre: 0.3
    };
    
    validateParams(invalidParams);
    console.log('✗ Validation should have failed but passed!');
    process.exit(1);
} catch (error) {
    console.log('✓ Validation correctly rejected invalid parameters');
    console.log('✓ Error message:', error.message, '\n');
}

// Test 3: Invalid parameters - fee split doesn't sum to 100%
console.log('Test 3: Invalid parameters (fee split != 100%)');
try {
    const invalidParams = {
        floorPrice: 10.0,
        proactiveThreshold: 10.55,
        stabilizationFeeBps: 10,
        splitRestitution: 5000,
        splitCounter: 3000,
        splitBurn: 3000, // Sum = 11000 (110%), should be 10000
        multisigType: '7-of-9',
        tre: 0.3
    };
    
    validateParams(invalidParams);
    console.log('✗ Validation should have failed but passed!');
    process.exit(1);
} catch (error) {
    console.log('✓ Validation correctly rejected invalid fee split');
    console.log('✓ Error message:', error.message, '\n');
}

console.log('='.repeat(70));
console.log('All tests passed! ✓');
console.log('='.repeat(70));
