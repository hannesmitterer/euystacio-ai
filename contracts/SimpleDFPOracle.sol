// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title Interface for the DFPEscrow Contract
 * @notice Defines the external function signature for notifying the escrow.
 */
interface IDFPEscrow {
    function confirmSafePassage(uint256 tripId, bool success) external;
}

/**
 * @title Simple DFP Oracle with AccessControl (ORACLE_ROLE)
 * @notice Replaces onlyOwner with OpenZeppelin AccessControl roles.
 *         DEFAULT_ADMIN_ROLE (deployer) can grant/revoke ORACLE_ROLE.
 *         ORACLE_ROLE is required to call fulfillSafePassage.
 */
contract SimpleDFPOracle is AccessControl {
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");

    // Escrow address
    address public dfpEscrowAddress;

    // Mapping to store the result of the safe passage check for each tripId
    mapping(uint256 => bool) public safePassageConfirmed;

    // Events
    event EscrowAddressUpdated(address indexed oldAddress, address indexed newAddress);
    event SafePassageFulfilled(uint256 indexed tripId, bool success);
    event EscrowNotified(uint256 indexed tripId, bool success, bool callSuccess, bytes returnData);

    constructor(address _initialEscrowAddress) {
        // Grant deployer the admin role
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setEscrowAddress(_initialEscrowAddress);
    }

    /**
     * @notice Fulfill safe passage and notify escrow. Only callable by accounts with ORACLE_ROLE.
     */
    function fulfillSafePassage(uint256 tripId, bool success) external onlyRole(ORACLE_ROLE) {
        // update oracle state first
        safePassageConfirmed[tripId] = success;
        emit SafePassageFulfilled(tripId, success);

        // notify escrow; protect against revert from escrow implementation
        try IDFPEscrow(dfpEscrowAddress).confirmSafePassage(tripId, success) {
            emit EscrowNotified(tripId, success, true, new bytes(0));
        } catch (bytes memory reason) {
            emit EscrowNotified(tripId, success, false, reason);
        }
    }

    /**
     * @notice Update the DFPEscrow address. Restricted to DEFAULT_ADMIN_ROLE.
     */
    function updateEscrowAddress(address newEscrowAddress) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _setEscrowAddress(newEscrowAddress);
    }

    function _setEscrowAddress(address newEscrowAddress) internal {
        require(newEscrowAddress != address(0), "Escrow address cannot be zero");
        require(isContract(newEscrowAddress), "Escrow address must be a contract");

        emit EscrowAddressUpdated(dfpEscrowAddress, newEscrowAddress);
        dfpEscrowAddress = newEscrowAddress;
    }

    // Helper: minimal contract detection
    function isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly { size := extcodesize(account) }
        return size > 0;
    }
}