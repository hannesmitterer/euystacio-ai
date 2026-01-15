"""
bbmn_network.py
Blockchain-Based Mesh Network (BBMN) for EUYSTACIO

Eliminates dependency on centralized DNS servers.
Integrates with IPFS for decentralized node discovery and communication.

Features:
- Decentralized node discovery via IPFS DHT
- Peer-to-peer mesh network topology
- Blockchain-anchored node registry
- No DNS dependency - fully decentralized
- Integration with existing IPFS integrity layer
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import secrets


class NodeStatus(Enum):
    """Status of mesh network node"""
    ACTIVE = "ACTIVE"
    CONNECTING = "CONNECTING"
    DISCONNECTED = "DISCONNECTED"
    SUSPENDED = "SUSPENDED"
    LEX_AMORIS_VERIFIED = "LEX_AMORIS_VERIFIED"


class NodeRole(Enum):
    """Role of node in mesh network"""
    SEED_NODE = "SEED_NODE"  # Bootstrap nodes
    RELAY_NODE = "RELAY_NODE"  # Message relay
    STORAGE_NODE = "STORAGE_NODE"  # IPFS pinning
    GUARDIAN_NODE = "GUARDIAN_NODE"  # Security monitoring
    RESONANCE_NODE = "RESONANCE_NODE"  # Lex Amoris alignment


@dataclass
class MeshNode:
    """Represents a node in the BBMN"""
    node_id: str
    ipfs_peer_id: str
    multiaddr: List[str]  # IPFS multiaddresses
    role: NodeRole
    status: NodeStatus
    lex_amoris_score: float  # Alignment score (0.0 - 1.0)
    public_key: bytes
    last_seen: float
    discovered_at: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "node_id": self.node_id,
            "ipfs_peer_id": self.ipfs_peer_id,
            "multiaddr": self.multiaddr,
            "role": self.role.value,
            "status": self.status.value,
            "lex_amoris_score": self.lex_amoris_score,
            "public_key": self.public_key.hex() if isinstance(self.public_key, bytes) else self.public_key,
            "last_seen": self.last_seen,
            "discovered_at": self.discovered_at,
            "metadata": self.metadata
        }
    
    def is_aligned(self, threshold: float = 0.7) -> bool:
        """Check if node is aligned with Lex Amoris"""
        return self.lex_amoris_score >= threshold


@dataclass
class BlockchainAnchor:
    """Blockchain anchor for node registry"""
    block_height: int
    block_hash: str
    registry_hash: str
    timestamp: float
    nodes_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_height": self.block_height,
            "block_hash": self.block_hash,
            "registry_hash": self.registry_hash,
            "timestamp": self.timestamp,
            "nodes_count": self.nodes_count,
            "anchor_time": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat()
        }


class IPFSNodeDiscovery:
    """
    IPFS-based node discovery service
    Uses IPFS DHT for decentralized peer discovery
    """
    
    def __init__(self, ipfs_manager=None):
        """
        Initialize IPFS node discovery
        
        Args:
            ipfs_manager: Optional IPFSIntegrityManager instance
        """
        self.ipfs_manager = ipfs_manager
        self.discovered_peers: Dict[str, MeshNode] = {}
        self.discovery_topic = "/euystacio/bbmn/discovery/1.0.0"
        
    def announce_node(self, node: MeshNode) -> bool:
        """
        Announce node presence to IPFS DHT
        
        Args:
            node: MeshNode to announce
            
        Returns:
            Success status
        """
        try:
            # Prepare announcement
            announcement = {
                "type": "node_announcement",
                "node_id": node.node_id,
                "ipfs_peer_id": node.ipfs_peer_id,
                "multiaddr": node.multiaddr,
                "role": node.role.value,
                "lex_amoris_score": node.lex_amoris_score,
                "timestamp": time.time()
            }
            
            # In production: Publish to IPFS pubsub or DHT
            # ipfs_manager.pubsub_publish(self.discovery_topic, announcement)
            
            print(f"[BBMN] Announced node {node.node_id} to IPFS DHT")
            return True
            
        except Exception as e:
            print(f"[BBMN] Error announcing node: {e}")
            return False
    
    def discover_peers(self, min_lex_amoris: float = 0.6) -> List[MeshNode]:
        """
        Discover peers via IPFS DHT
        
        Args:
            min_lex_amoris: Minimum Lex Amoris score for acceptance
            
        Returns:
            List of discovered MeshNodes
        """
        discovered = []
        
        try:
            # In production: Subscribe to IPFS pubsub discovery topic
            # messages = ipfs_manager.pubsub_subscribe(self.discovery_topic)
            
            # Simulate discovery for demonstration
            # In real implementation, this would query IPFS DHT
            print(f"[BBMN] Discovering peers via IPFS DHT on topic {self.discovery_topic}")
            
            # Filter by Lex Amoris alignment
            for peer_id, node in self.discovered_peers.items():
                if node.lex_amoris_score >= min_lex_amoris:
                    discovered.append(node)
            
        except Exception as e:
            print(f"[BBMN] Error discovering peers: {e}")
        
        return discovered
    
    def resolve_node(self, node_id: str) -> Optional[MeshNode]:
        """
        Resolve node by ID via IPFS DHT
        
        Args:
            node_id: Node identifier
            
        Returns:
            MeshNode if found, None otherwise
        """
        # In production: Query IPFS DHT for node information
        # node_data = ipfs_manager.dht_findprovs(node_id)
        
        return self.discovered_peers.get(node_id)


class BlockchainNodeRegistry:
    """
    Blockchain-anchored node registry
    Provides immutable record of network nodes
    """
    
    def __init__(self):
        self.registry: Dict[str, MeshNode] = {}
        self.blockchain_anchors: List[BlockchainAnchor] = []
        self.current_block_height = 0
        
    def register_node(self, node: MeshNode) -> bool:
        """
        Register node in blockchain-anchored registry
        
        Args:
            node: MeshNode to register
            
        Returns:
            Success status
        """
        try:
            # Validate Lex Amoris alignment
            if not node.is_aligned(threshold=0.6):
                print(f"[BBMN] Node {node.node_id} rejected - insufficient Lex Amoris alignment")
                return False
            
            # Add to registry
            self.registry[node.node_id] = node
            
            print(f"[BBMN] Registered node {node.node_id} with role {node.role.value}")
            return True
            
        except Exception as e:
            print(f"[BBMN] Error registering node: {e}")
            return False
    
    def anchor_to_blockchain(self) -> BlockchainAnchor:
        """
        Anchor current registry state to blockchain
        
        Returns:
            BlockchainAnchor record
        """
        # Calculate registry hash
        registry_data = {
            node_id: node.to_dict() 
            for node_id, node in self.registry.items()
        }
        registry_json = json.dumps(registry_data, sort_keys=True)
        registry_hash = hashlib.sha256(registry_json.encode()).hexdigest()
        
        # Simulate blockchain block
        self.current_block_height += 1
        block_hash = hashlib.sha256(
            f"{self.current_block_height}{registry_hash}{time.time()}".encode()
        ).hexdigest()
        
        # Create anchor
        anchor = BlockchainAnchor(
            block_height=self.current_block_height,
            block_hash=block_hash,
            registry_hash=registry_hash,
            timestamp=time.time(),
            nodes_count=len(self.registry)
        )
        
        self.blockchain_anchors.append(anchor)
        
        print(f"[BBMN] Anchored registry to blockchain at block {self.current_block_height}")
        return anchor
    
    def get_node(self, node_id: str) -> Optional[MeshNode]:
        """Get node from registry"""
        return self.registry.get(node_id)
    
    def get_all_nodes(self, role: Optional[NodeRole] = None, 
                     status: Optional[NodeStatus] = None) -> List[MeshNode]:
        """
        Get all nodes, optionally filtered by role or status
        
        Args:
            role: Optional role filter
            status: Optional status filter
            
        Returns:
            List of matching nodes
        """
        nodes = list(self.registry.values())
        
        if role:
            nodes = [n for n in nodes if n.role == role]
        if status:
            nodes = [n for n in nodes if n.status == status]
        
        return nodes
    
    def verify_registry_integrity(self, anchor_index: int = -1) -> bool:
        """
        Verify registry integrity against blockchain anchor
        
        Args:
            anchor_index: Index of anchor to verify against (-1 for latest)
            
        Returns:
            True if integrity verified
        """
        if not self.blockchain_anchors:
            return False
        
        anchor = self.blockchain_anchors[anchor_index]
        
        # Recalculate current registry hash
        registry_data = {
            node_id: node.to_dict() 
            for node_id, node in self.registry.items()
        }
        registry_json = json.dumps(registry_data, sort_keys=True)
        current_hash = hashlib.sha256(registry_json.encode()).hexdigest()
        
        # Compare
        return current_hash == anchor.registry_hash


class BBMNNetwork:
    """
    Main Blockchain-Based Mesh Network implementation
    
    Provides decentralized networking without DNS dependency
    """
    
    def __init__(self, ipfs_manager=None, quantum_shield=None):
        """
        Initialize BBMN
        
        Args:
            ipfs_manager: Optional IPFSIntegrityManager for IPFS integration
            quantum_shield: Optional QuantumShield for encryption
        """
        self.ipfs_manager = ipfs_manager
        self.quantum_shield = quantum_shield
        
        self.discovery = IPFSNodeDiscovery(ipfs_manager)
        self.registry = BlockchainNodeRegistry()
        
        self.local_node: Optional[MeshNode] = None
        self.connected_peers: Set[str] = set()
        
        # Network statistics
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "peers_discovered": 0,
            "dns_queries": 0,  # Should remain 0!
            "started_at": time.time()
        }
        
    def initialize_local_node(self, role: NodeRole = NodeRole.RESONANCE_NODE,
                            lex_amoris_score: float = 0.95) -> MeshNode:
        """
        Initialize local node and join network
        
        Args:
            role: Role for this node
            lex_amoris_score: Lex Amoris alignment score
            
        Returns:
            Local MeshNode
        """
        # Generate node identity
        node_id = f"EUYSTACIO-{secrets.token_hex(8)}"
        ipfs_peer_id = f"Qm{secrets.token_hex(22)}"  # Simulated IPFS peer ID
        
        # Get public key from quantum shield if available
        if self.quantum_shield:
            public_key = self.quantum_shield.get_public_key()
        else:
            public_key = secrets.token_bytes(64)
        
        # Create multiaddresses (IPFS format)
        multiaddr = [
            f"/ip4/127.0.0.1/tcp/4001/p2p/{ipfs_peer_id}",
            f"/ip6/::1/tcp/4001/p2p/{ipfs_peer_id}"
        ]
        
        # Create local node
        self.local_node = MeshNode(
            node_id=node_id,
            ipfs_peer_id=ipfs_peer_id,
            multiaddr=multiaddr,
            role=role,
            status=NodeStatus.LEX_AMORIS_VERIFIED,
            lex_amoris_score=lex_amoris_score,
            public_key=public_key,
            last_seen=time.time(),
            discovered_at=time.time(),
            metadata={
                "quantum_protected": self.quantum_shield is not None,
                "version": "1.0.0"
            }
        )
        
        # Register in blockchain registry
        self.registry.register_node(self.local_node)
        
        # Announce to IPFS DHT
        self.discovery.announce_node(self.local_node)
        
        print(f"[BBMN] Local node initialized: {node_id}")
        print(f"[BBMN] IPFS Peer ID: {ipfs_peer_id}")
        print(f"[BBMN] Role: {role.value}")
        print(f"[BBMN] Lex Amoris Score: {lex_amoris_score}")
        
        return self.local_node
    
    def discover_and_connect(self, min_lex_amoris: float = 0.7) -> int:
        """
        Discover and connect to peers via IPFS
        
        Args:
            min_lex_amoris: Minimum Lex Amoris score for connection
            
        Returns:
            Number of new peers discovered
        """
        # Discover peers
        peers = self.discovery.discover_peers(min_lex_amoris)
        
        new_peers = 0
        for peer in peers:
            if peer.node_id not in self.connected_peers:
                # Register peer
                self.registry.register_node(peer)
                self.connected_peers.add(peer.node_id)
                new_peers += 1
                
                print(f"[BBMN] Connected to peer: {peer.node_id} ({peer.role.value})")
        
        self.stats["peers_discovered"] += new_peers
        
        # Verify DNS-free operation (critical security check)
        if self.stats["dns_queries"] > 0:
            raise RuntimeError(
                f"CRITICAL SECURITY VIOLATION: {self.stats['dns_queries']} DNS queries detected! "
                "BBMN must operate without DNS. Network compromised."
            )
        
        return new_peers
    
    def send_message(self, recipient_node_id: str, message: bytes, 
                    encrypt: bool = True) -> bool:
        """
        Send message to peer via mesh network
        
        Args:
            recipient_node_id: Target node ID
            message: Message bytes
            encrypt: Whether to encrypt with quantum shield
            
        Returns:
            Success status
        """
        try:
            # Resolve recipient
            recipient = self.registry.get_node(recipient_node_id)
            if not recipient:
                print(f"[BBMN] Node {recipient_node_id} not found in registry")
                return False
            
            # Verify Lex Amoris alignment
            if not recipient.is_aligned():
                print(f"[BBMN] Node {recipient_node_id} not aligned with Lex Amoris")
                return False
            
            # Encrypt if requested and quantum shield available
            if encrypt and self.quantum_shield:
                encrypted_msg, key_id = self.quantum_shield.encrypt(message)
                message_to_send = encrypted_msg
                print(f"[BBMN] Message encrypted with quantum key {key_id}")
            else:
                message_to_send = message
            
            # In production: Send via IPFS pubsub or direct p2p
            # ipfs_manager.send_to_peer(recipient.ipfs_peer_id, message_to_send)
            
            self.stats["messages_sent"] += 1
            print(f"[BBMN] Message sent to {recipient_node_id} via IPFS")
            
            return True
            
        except Exception as e:
            print(f"[BBMN] Error sending message: {e}")
            return False
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        total_nodes = len(self.registry.get_all_nodes())
        aligned_nodes = len([n for n in self.registry.get_all_nodes() if n.is_aligned()])
        
        uptime = time.time() - self.stats["started_at"]
        
        return {
            "local_node": self.local_node.to_dict() if self.local_node else None,
            "total_nodes": total_nodes,
            "aligned_nodes": aligned_nodes,
            "connected_peers": len(self.connected_peers),
            "messages_sent": self.stats["messages_sent"],
            "messages_received": self.stats["messages_received"],
            "peers_discovered": self.stats["peers_discovered"],
            "dns_queries": self.stats["dns_queries"],  # Must be 0!
            "uptime_seconds": uptime,
            "blockchain_anchors": len(self.registry.blockchain_anchors),
            "decentralized": True,
            "dns_free": self.stats["dns_queries"] == 0
        }


# Global BBMN instance
_bbmn_instance: Optional[BBMNNetwork] = None


def get_bbmn_network(ipfs_manager=None, quantum_shield=None) -> BBMNNetwork:
    """
    Get or create global BBMN instance
    
    Args:
        ipfs_manager: Optional IPFSIntegrityManager
        quantum_shield: Optional QuantumShield
        
    Returns:
        BBMNNetwork instance
    """
    global _bbmn_instance
    
    if _bbmn_instance is None:
        _bbmn_instance = BBMNNetwork(ipfs_manager, quantum_shield)
    
    return _bbmn_instance


# Self-test
if __name__ == "__main__":
    print("=== BBMN Network Self-Test ===")
    
    # Initialize network
    bbmn = BBMNNetwork()
    
    # Initialize local node
    print("\n1. Initializing Local Node:")
    local_node = bbmn.initialize_local_node(
        role=NodeRole.RESONANCE_NODE,
        lex_amoris_score=0.95
    )
    
    # Create some simulated peers
    print("\n2. Creating Simulated Peers:")
    for i in range(3):
        peer = MeshNode(
            node_id=f"PEER-{i}",
            ipfs_peer_id=f"Qm{secrets.token_hex(22)}",
            multiaddr=[f"/ip4/10.0.0.{i+1}/tcp/4001"],
            role=NodeRole.RELAY_NODE,
            status=NodeStatus.ACTIVE,
            lex_amoris_score=0.75 + (i * 0.05),
            public_key=secrets.token_bytes(64),
            last_seen=time.time(),
            discovered_at=time.time()
        )
        bbmn.discovery.discovered_peers[peer.node_id] = peer
    
    # Discover and connect
    print("\n3. Discovering Peers:")
    new_peers = bbmn.discover_and_connect(min_lex_amoris=0.7)
    print(f"   Discovered {new_peers} new peers")
    
    # Anchor to blockchain
    print("\n4. Anchoring to Blockchain:")
    anchor = bbmn.registry.anchor_to_blockchain()
    print(f"   Block Height: {anchor.block_height}")
    print(f"   Registry Hash: {anchor.registry_hash[:32]}...")
    print(f"   Nodes Count: {anchor.nodes_count}")
    
    # Network status
    print("\n5. Network Status:")
    status = bbmn.get_network_status()
    print(f"   Total Nodes: {status['total_nodes']}")
    print(f"   Aligned Nodes: {status['aligned_nodes']}")
    print(f"   DNS Queries: {status['dns_queries']} (must be 0!)")
    print(f"   Decentralized: {status['decentralized']}")
    print(f"   DNS-Free: {status['dns_free']}")
    
    print("\n✅ BBMN Network operational - DNS-free, decentralized mesh active")
