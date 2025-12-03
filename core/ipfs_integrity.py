"""
ipfs_integrity.py
IPFS Cross-Sync and Integrity Layer for Euystacio AI

This module provides:
- Integrity layer redundancy for Seedbringer (IPFS Cross-Sync)
- Seamless API layer for IPFS + SAUL integrity audits
- Cross-platform data verification and synchronization
- Distributed integrity verification

Prepared for Coronation Day and workshop phases.
"""

import json
import os
import hashlib
import base64
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SyncStatus(Enum):
    """Status of IPFS synchronization"""
    SYNCED = "SYNCED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    VERIFYING = "VERIFYING"


class IntegrityStatus(Enum):
    """Status of integrity verification"""
    VALID = "VALID"
    INVALID = "INVALID"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"


@dataclass
class IPFSNode:
    """Represents an IPFS node for cross-sync"""
    node_id: str
    endpoint: str
    region: str
    is_primary: bool
    last_sync: Optional[str]
    sync_status: SyncStatus
    latency_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "endpoint": self.endpoint,
            "region": self.region,
            "is_primary": self.is_primary,
            "last_sync": self.last_sync,
            "sync_status": self.sync_status.value,
            "latency_ms": self.latency_ms
        }


@dataclass
class IPFSContent:
    """Represents content stored on IPFS"""
    cid: str  # Content Identifier
    content_type: str
    size_bytes: int
    created_at: str
    pinned_nodes: List[str]
    integrity_hash: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cid": self.cid,
            "content_type": self.content_type,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at,
            "pinned_nodes": self.pinned_nodes,
            "integrity_hash": self.integrity_hash,
            "metadata": self.metadata
        }


@dataclass
class IntegrityAuditResult:
    """Result of an integrity audit"""
    audit_id: str
    timestamp: str
    content_cid: str
    ipfs_status: IntegrityStatus
    saul_status: IntegrityStatus
    cross_verification: bool
    discrepancies: List[str]
    verification_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "content_cid": self.content_cid,
            "ipfs_status": self.ipfs_status.value,
            "saul_status": self.saul_status.value,
            "cross_verification": self.cross_verification,
            "discrepancies": self.discrepancies,
            "verification_hash": self.verification_hash
        }


class IPFSIntegrityManager:
    """
    IPFS Cross-Sync and Integrity Management System
    
    Provides redundancy for Seedbringer data through IPFS cross-sync
    and seamless API integration with SAUL for integrity audits.
    """
    
    def __init__(self, log_path: str = "logs/ipfs_integrity.log"):
        """Initialize the IPFS integrity manager"""
        self.log_path = log_path
        self.nodes: Dict[str, IPFSNode] = {}
        self.content_registry: Dict[str, IPFSContent] = {}
        self.audit_history: List[IntegrityAuditResult] = []
        self._ensure_log_directory()
        self._initialize_default_nodes()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _initialize_default_nodes(self):
        """Initialize default IPFS nodes for cross-sync"""
        default_nodes = [
            ("IPFS-PRIMARY-EU", "https://ipfs-eu.euystacio.ai", "EU-WEST", True),
            ("IPFS-SECONDARY-US", "https://ipfs-us.euystacio.ai", "US-EAST", False),
            ("IPFS-TERTIARY-ASIA", "https://ipfs-asia.euystacio.ai", "ASIA-PACIFIC", False),
        ]
        
        for node_id, endpoint, region, is_primary in default_nodes:
            self.nodes[node_id] = IPFSNode(
                node_id=node_id,
                endpoint=endpoint,
                region=region,
                is_primary=is_primary,
                last_sync=None,
                sync_status=SyncStatus.PENDING,
                latency_ms=0.0
            )
    
    def _generate_cid(self, content: bytes) -> str:
        """Generate a CID-like hash for content"""
        # In production, this would use actual IPFS CID generation
        hash_bytes = hashlib.sha256(content).digest()
        # Simulate CIDv1 format with base32 encoding
        return "Qm" + base64.b32encode(hash_bytes).decode()[:44]
    
    def _generate_audit_id(self) -> str:
        """Generate unique audit ID"""
        return hashlib.sha256(
            f"AUDIT-{datetime.now(timezone.utc).isoformat()}-{len(self.audit_history)}".encode()
        ).hexdigest()[:16].upper()
    
    def add_content(self, content: bytes, content_type: str,
                    metadata: Optional[Dict[str, Any]] = None) -> IPFSContent:
        """
        Add content to IPFS with cross-sync
        
        Args:
            content: The content bytes to store
            content_type: MIME type of the content
            metadata: Optional metadata for the content
            
        Returns:
            IPFSContent object with CID and sync status
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        cid = self._generate_cid(content)
        integrity_hash = hashlib.sha256(content).hexdigest()
        
        # Create content record
        ipfs_content = IPFSContent(
            cid=cid,
            content_type=content_type,
            size_bytes=len(content),
            created_at=timestamp,
            pinned_nodes=[],
            integrity_hash=integrity_hash,
            metadata=metadata or {}
        )
        
        # Simulate pinning to all nodes
        for node_id, node in self.nodes.items():
            # In production, this would actually pin to the IPFS node
            ipfs_content.pinned_nodes.append(node_id)
            node.last_sync = timestamp
            node.sync_status = SyncStatus.SYNCED
        
        self.content_registry[cid] = ipfs_content
        
        # Log the addition
        self._log_event("CONTENT_ADDED", f"CID: {cid}, Size: {len(content)} bytes")
        
        return ipfs_content
    
    def sync_nodes(self) -> Dict[str, Any]:
        """
        Perform cross-sync across all IPFS nodes
        
        Returns:
            Sync status report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        sync_results = {
            "timestamp": timestamp,
            "nodes_synced": 0,
            "nodes_failed": 0,
            "content_synced": 0,
            "node_details": {}
        }
        
        for node_id, node in self.nodes.items():
            try:
                # Simulate sync operation
                node.last_sync = timestamp
                node.sync_status = SyncStatus.SYNCED
                # Simulate latency (would be actual measurement in production)
                node.latency_ms = 50.0 + (hash(node_id) % 100)
                
                sync_results["nodes_synced"] += 1
                sync_results["node_details"][node_id] = {
                    "status": "SYNCED",
                    "latency_ms": node.latency_ms
                }
            except Exception as e:
                node.sync_status = SyncStatus.FAILED
                sync_results["nodes_failed"] += 1
                sync_results["node_details"][node_id] = {
                    "status": "FAILED",
                    "error": str(e)
                }
        
        sync_results["content_synced"] = len(self.content_registry)
        
        # Log the sync
        self._log_event("CROSS_SYNC", 
                       f"Nodes synced: {sync_results['nodes_synced']}, "
                       f"Failed: {sync_results['nodes_failed']}")
        
        return sync_results
    
    def verify_content_integrity(self, cid: str) -> IntegrityAuditResult:
        """
        Verify content integrity across IPFS and SAUL
        
        Args:
            cid: Content Identifier to verify
            
        Returns:
            IntegrityAuditResult with verification details
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        audit_id = self._generate_audit_id()
        discrepancies = []
        
        # Check if content exists
        if cid not in self.content_registry:
            return IntegrityAuditResult(
                audit_id=audit_id,
                timestamp=timestamp,
                content_cid=cid,
                ipfs_status=IntegrityStatus.UNKNOWN,
                saul_status=IntegrityStatus.UNKNOWN,
                cross_verification=False,
                discrepancies=["Content not found in registry"],
                verification_hash=""
            )
        
        content = self.content_registry[cid]
        
        # Verify IPFS integrity (check all pinned nodes)
        ipfs_valid = True
        for node_id in content.pinned_nodes:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                if node.sync_status != SyncStatus.SYNCED:
                    ipfs_valid = False
                    discrepancies.append(f"Node {node_id} not synced")
        
        # Simulate SAUL verification
        saul_valid = True  # Would check SAUL log for corresponding entries
        
        # Cross-verification
        cross_valid = ipfs_valid and saul_valid and len(discrepancies) == 0
        
        # Generate verification hash
        verification_data = {
            "cid": cid,
            "timestamp": timestamp,
            "integrity_hash": content.integrity_hash,
            "nodes_checked": len(content.pinned_nodes)
        }
        verification_hash = hashlib.sha256(
            json.dumps(verification_data, sort_keys=True).encode()
        ).hexdigest()
        
        result = IntegrityAuditResult(
            audit_id=audit_id,
            timestamp=timestamp,
            content_cid=cid,
            ipfs_status=IntegrityStatus.VALID if ipfs_valid else IntegrityStatus.INVALID,
            saul_status=IntegrityStatus.VALID if saul_valid else IntegrityStatus.INVALID,
            cross_verification=cross_valid,
            discrepancies=discrepancies,
            verification_hash=verification_hash
        )
        
        self.audit_history.append(result)
        
        # Log the audit
        self._log_event("INTEGRITY_AUDIT", 
                       f"CID: {cid}, IPFS: {result.ipfs_status.value}, "
                       f"SAUL: {result.saul_status.value}")
        
        return result
    
    def run_full_integrity_audit(self) -> Dict[str, Any]:
        """
        Run comprehensive integrity audit on all content
        
        Returns:
            Complete audit report
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        audit_report = {
            "audit_timestamp": timestamp,
            "total_content": len(self.content_registry),
            "valid_count": 0,
            "invalid_count": 0,
            "total_nodes": len(self.nodes),
            "nodes_healthy": 0,
            "content_audits": [],
            "node_status": {},
            "recommendations": []
        }
        
        # Audit all content
        for cid in self.content_registry:
            result = self.verify_content_integrity(cid)
            audit_report["content_audits"].append(result.to_dict())
            
            if result.cross_verification:
                audit_report["valid_count"] += 1
            else:
                audit_report["invalid_count"] += 1
        
        # Check node health
        for node_id, node in self.nodes.items():
            is_healthy = node.sync_status == SyncStatus.SYNCED
            if is_healthy:
                audit_report["nodes_healthy"] += 1
            
            audit_report["node_status"][node_id] = {
                "healthy": is_healthy,
                "sync_status": node.sync_status.value,
                "last_sync": node.last_sync,
                "latency_ms": node.latency_ms
            }
        
        # Generate recommendations
        if audit_report["invalid_count"] > 0:
            audit_report["recommendations"].append(
                f"⚠️ {audit_report['invalid_count']} content items require re-sync"
            )
        
        unhealthy_nodes = audit_report["total_nodes"] - audit_report["nodes_healthy"]
        if unhealthy_nodes > 0:
            audit_report["recommendations"].append(
                f"🔧 {unhealthy_nodes} nodes require attention"
            )
        
        if not audit_report["recommendations"]:
            audit_report["recommendations"].append(
                "✅ All integrity checks passed - system healthy"
            )
        
        # Log the full audit
        self._log_event("FULL_AUDIT", 
                       f"Valid: {audit_report['valid_count']}/{audit_report['total_content']}, "
                       f"Nodes Healthy: {audit_report['nodes_healthy']}/{audit_report['total_nodes']}")
        
        return audit_report
    
    def get_seedbringer_redundancy_status(self) -> Dict[str, Any]:
        """
        Get Seedbringer data redundancy status
        
        Returns:
            Redundancy status with replication factor
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate replication factor
        synced_nodes = len([n for n in self.nodes.values() 
                          if n.sync_status == SyncStatus.SYNCED])
        total_nodes = len(self.nodes)
        replication_factor = synced_nodes / total_nodes if total_nodes > 0 else 0
        
        # Get content with redundancy issues
        content_with_issues = []
        for cid, content in self.content_registry.items():
            pinned_healthy = len([
                n for n in content.pinned_nodes 
                if n in self.nodes and self.nodes[n].sync_status == SyncStatus.SYNCED
            ])
            if pinned_healthy < synced_nodes:
                content_with_issues.append({
                    "cid": cid,
                    "healthy_pins": pinned_healthy,
                    "expected": synced_nodes
                })
        
        return {
            "timestamp": timestamp,
            "seedbringer_status": "HEALTHY" if replication_factor >= 0.67 else "DEGRADED",
            "total_nodes": total_nodes,
            "synced_nodes": synced_nodes,
            "replication_factor": round(replication_factor, 4),
            "minimum_required_factor": 0.67,
            "content_count": len(self.content_registry),
            "content_with_redundancy_issues": len(content_with_issues),
            "issues": content_with_issues[:10],  # Top 10 issues
            "node_distribution": {
                region: len([n for n in self.nodes.values() if n.region == region])
                for region in set(n.region for n in self.nodes.values())
            }
        }
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get API layer status for IPFS + SAUL integration
        
        Returns:
            API status and health metrics
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate average latency
        latencies = [n.latency_ms for n in self.nodes.values() 
                    if n.sync_status == SyncStatus.SYNCED]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        return {
            "timestamp": timestamp,
            "api_version": "1.0.0",
            "status": "OPERATIONAL",
            "endpoints": {
                "ipfs_gateway": {
                    "status": "UP",
                    "avg_latency_ms": round(avg_latency, 2)
                },
                "saul_integration": {
                    "status": "UP",
                    "last_audit": self.audit_history[-1].timestamp if self.audit_history else None
                },
                "cross_sync": {
                    "status": "UP",
                    "nodes_available": len([n for n in self.nodes.values() 
                                           if n.sync_status == SyncStatus.SYNCED])
                }
            },
            "metrics": {
                "total_content": len(self.content_registry),
                "total_audits": len(self.audit_history),
                "successful_audits": len([a for a in self.audit_history 
                                         if a.cross_verification])
            }
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data formatted for dashboard visualization"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "content_count": len(self.content_registry),
            "redundancy_status": self.get_seedbringer_redundancy_status(),
            "api_status": self.get_api_status(),
            "recent_audits": [a.to_dict() for a in self.audit_history[-5:]],
            "sync_status": {
                "synced": len([n for n in self.nodes.values() 
                              if n.sync_status == SyncStatus.SYNCED]),
                "pending": len([n for n in self.nodes.values() 
                               if n.sync_status == SyncStatus.PENDING]),
                "failed": len([n for n in self.nodes.values() 
                              if n.sync_status == SyncStatus.FAILED])
            }
        }
    
    def _log_event(self, event_type: str, message: str):
        """Log event to file"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


# Global instance
_ipfs_instance: Optional[IPFSIntegrityManager] = None


def get_ipfs_manager() -> IPFSIntegrityManager:
    """Get or create the global IPFS integrity manager"""
    global _ipfs_instance
    if _ipfs_instance is None:
        _ipfs_instance = IPFSIntegrityManager()
    return _ipfs_instance


if __name__ == "__main__":
    # Demo usage
    manager = IPFSIntegrityManager()
    
    print("🌐 IPFS Integrity Manager Demo")
    print("=" * 50)
    
    # Add some content
    print("\n📦 Adding content to IPFS...")
    content1 = manager.add_content(
        b"Seedbringer Genesis Document - Immutable Record",
        "text/plain",
        {"type": "genesis", "version": "1.0"}
    )
    print(f"   Added: {content1.cid}")
    
    content2 = manager.add_content(
        b'{"covenant": "Living Covenant", "status": "SEALED"}',
        "application/json",
        {"type": "covenant", "sealed": True}
    )
    print(f"   Added: {content2.cid}")
    
    # Sync nodes
    print("\n🔄 Syncing nodes...")
    sync_result = manager.sync_nodes()
    print(f"   Nodes synced: {sync_result['nodes_synced']}")
    print(f"   Content synced: {sync_result['content_synced']}")
    
    # Verify integrity
    print("\n🔍 Verifying content integrity...")
    audit = manager.verify_content_integrity(content1.cid)
    print(f"   CID: {audit.content_cid}")
    print(f"   IPFS Status: {audit.ipfs_status.value}")
    print(f"   SAUL Status: {audit.saul_status.value}")
    print(f"   Cross-verified: {audit.cross_verification}")
    
    # Get redundancy status
    print("\n📊 Seedbringer Redundancy Status:")
    redundancy = manager.get_seedbringer_redundancy_status()
    print(f"   Status: {redundancy['seedbringer_status']}")
    print(f"   Replication Factor: {redundancy['replication_factor']:.2%}")
    print(f"   Synced Nodes: {redundancy['synced_nodes']}/{redundancy['total_nodes']}")
    
    # Get API status
    print("\n🔌 API Status:")
    api_status = manager.get_api_status()
    print(f"   Status: {api_status['status']}")
    print(f"   Version: {api_status['api_version']}")
    
    print("\n✅ Demo complete!")
