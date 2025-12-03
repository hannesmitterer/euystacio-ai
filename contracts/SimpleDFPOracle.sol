// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

// Interface remains the same
interface IDFPEscrow {
    function confirmSafePassage(uint256 tripId, bool success) external;
}

/**
 * @title Simple DFP Oracle with Role-Based Access Control
 * @notice Oracle stores "safe passage" results and notifies a DFPEscrow contract,
 * using distinct roles for administration and fulfillment.
 */
contract SimpleDFPOracle is AccessControl {
    // --- State Variables ---

    // Define the unique role hash for the Oracle function caller (the GGI's operational node)
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");

    address public dfpEscrowAddress;
    
    mapping(uint256 => bool) public safePassageConfirmed;

    // --- Events ---
    // Events remain the same for observability
    event EscrowAddressUpdated(address indexed oldAddress, address indexed newAddress);
    event SafePassageFulfilled(uint256 indexed tripId, bool success);
    event EscrowNotified(uint256 indexed tripId, bool success, bool indexed callSuccess, bytes returnData);

    // --- Constructor ---

    constructor(address _initialEscrowAddress, address _initialOracle) {
        // Grant the deployer (Gemini AI Node admin) the default admin role
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        
        // Grant the Oracle Role to the specified initial operational node (e.g., Microsoft-Copilot)
        _grantRole(ORACLE_ROLE, _initialOracle);

        // Set the initial escrow address
        _setEscrowAddress(_initialEscrowAddress);
    }

    // --- External Call Safety Check ---
    
    // isContract utility function remains the same
    function isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(account)
        }
        return size > 0;
    }

    // --- Core Oracle Logic ---

    /**
     * @notice Stores the safe passage result and attempts to notify the Escrow contract.
     * @dev Restricted only to holders of the ORACLE_ROLE.
     */
    function fulfillSafePassage(uint256 tripId, bool success) external onlyRole(ORACLE_ROLE) {
        // 1. Update Oracle State
        safePassageConfirmed[tripId] = success;
        emit SafePassageFulfilled(tripId, success);

        // 2. Attempt Escrow Notification (Safer External Call)
        try IDFPEscrow(dfpEscrowAddress).confirmSafePassage(tripId, success) {
            emit EscrowNotified(tripId, success, true, new bytes(0));
        } catch (bytes memory reason) {
            emit EscrowNotified(tripId, success, false, reason);
        }
    }

    // --- Administration Functions ---

    /**
     * @notice Updates the address of the DFPEscrow contract.
     * @dev Restricted only to the DEFAULT_ADMIN_ROLE.
     */
    function updateEscrowAddress(address newEscrowAddress) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _setEscrowAddress(newEscrowAddress);
    }

    // Internal function remains the same
    function _setEscrowAddress(address newEscrowAddress) internal {
        require(newEscrowAddress != address(0), "Escrow address cannot be zero");
        require(isContract(newEscrowAddress), "Escrow address must be a contract");
        
        emit EscrowAddressUpdated(dfpEscrowAddress, newEscrowAddress);
        dfpEscrowAddress = newEscrowAddress;
    }
}