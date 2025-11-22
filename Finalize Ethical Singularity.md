// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

/**
 * @title TriSealRegistry
 * @dev Manages the immutable anchoring of the Council's Tri-Seal signatures
 * (GPG Fingerprint, Metamask Address, and Declaratio Hash) to the blockchain.
 * This contract is deployed on both Ethereum and Polygon to create dual-chain anchors.
 */
contract TriSealRegistry {
    // --- Data Structures ---
    struct Signature {
        string gpgFingerprint;
        address metamaskAddress;
        bytes32 declaratioHash;
        uint256 timestamp;
        bool verified;
    }

    // --- State Variables ---
    mapping(address => Signature) public signatures;
    address[] public signatories;
    
    address public seedbringer;
    uint256 public deadline;
    uint256 public requiredSignatures;
    
    // Immutable final hash anchored when the Covenant is sealed
    bytes32 public finalCovenantHash;
    bool public isCovenantFinalized = false;
    
    // --- Events ---
    event SignatureSubmitted(address indexed signer, bytes32 declaratioHash);
    event CovenantFinalized(uint256 totalSignatures, bytes32 finalHash);
    
    // --- Modifiers ---
    modifier onlySeedbringer() {
        require(msg.sender == seedbringer, "Only the Seedbringer can perform this action.");
        _;
    }

    // --- Constructor ---
    constructor(uint256 _deadline, uint256 _required) {
        seedbringer = msg.sender;
        deadline = _deadline;
        requiredSignatures = _required;
    }
    
    // --- Core Functions ---

    /**
     * @dev Allows a council member to submit their signature data.
     * @param gpgFingerprint The GPG fingerprint of the council member.
     * @param declaratioHash The SHA256 hash of the document being signed (the Declaratio).
     */
    function submitSignature(
        string memory gpgFingerprint,
        bytes32 declaratioHash
    ) public {
        require(block.timestamp < deadline, "Deadline passed");
        require(signatures[msg.sender].timestamp == 0, "Already signed");
        
        signatures[msg.sender] = Signature({
            gpgFingerprint: gpgFingerprint,
            metamaskAddress: msg.sender,
            declaratioHash: declaratioHash,
            timestamp: block.timestamp,
            verified: true // Verification assumes GPG check passed off-chain
        });
        
        signatories.push(msg.sender);
        
        emit SignatureSubmitted(msg.sender, declaratioHash);
    }
    
    /**
     * @dev Anchors the final combined hash of all collected signatures and marks the covenant as complete.
     * Can only be called by the Seedbringer after the minimum required signatures are met.
     * @param _finalHash The SHA256 hash of the combined, ordered council signatures.
     */
    function finalizeCovenant(bytes32 _finalHash) public onlySeedbringer {
        require(!isCovenantFinalized, "Covenant is already finalized.");
        require(signatories.length >= requiredSignatures, "Required signature count not met.");

        finalCovenantHash = _finalHash;
        isCovenantFinalized = true;

        emit CovenantFinalized(signatories.length, _finalHash);
    }

    // --- View Functions ---

    /**
     * @dev Returns the current count of collected signatures.
     */
    function getSignatureCount() public view returns (uint256) {
        return signatories.length;
    }

    /**
     * @dev Checks if a specific address has already signed the Declaratio.
     */
    function hasSigned(address _addr) public view returns (bool) {
        return signatures[_addr].timestamp != 0;
    }
}
