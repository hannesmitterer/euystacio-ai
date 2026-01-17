"""
ipfs_pr_backup.py
IPFS PR Configuration Backup System for Euystacio AI

Implements:
- Complete mirroring of PR configurations to IPFS
- Protection against external escalations
- Automated backup on PR events
- Integration with existing ipfs_integrity.py

Based on Lex Amoris: Preserve knowledge and protect against loss.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Constants for backup verification
MAX_BACKUPS_TO_CHECK = 50
POOR_REPLICATION_THRESHOLD = 0.2  # 20%

# Import existing IPFS integrity system
try:
    from core.ipfs_integrity import IPFSIntegrityManager, get_ipfs_manager
except ImportError:
    # Fallback if not available
    IPFSIntegrityManager = None
    get_ipfs_manager = lambda: None


class BackupTrigger(Enum):
    """Trigger events for backup"""
    PR_CREATED = "PR_CREATED"
    PR_UPDATED = "PR_UPDATED"
    PR_MERGED = "PR_MERGED"
    PR_CLOSED = "PR_CLOSED"
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    ESCALATION_DETECTED = "ESCALATION_DETECTED"


class BackupStatus(Enum):
    """Status of backup operation"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"


@dataclass
class PRConfiguration:
    """Pull Request configuration data"""
    pr_number: int
    title: str
    description: str
    branch: str
    base_branch: str
    files_changed: List[str]
    commits: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pr_number": self.pr_number,
            "title": self.title,
            "description": self.description,
            "branch": self.branch,
            "base_branch": self.base_branch,
            "files_changed": self.files_changed,
            "commits": self.commits,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def to_json_bytes(self) -> bytes:
        """Convert to JSON bytes for IPFS storage"""
        return json.dumps(self.to_dict(), indent=2).encode('utf-8')


@dataclass
class BackupRecord:
    """Record of a PR backup operation"""
    backup_id: str
    pr_number: int
    trigger: BackupTrigger
    status: BackupStatus
    ipfs_cid: Optional[str]
    backup_timestamp: str
    verification_hash: str
    size_bytes: int
    nodes_replicated: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "pr_number": self.pr_number,
            "trigger": self.trigger.value,
            "status": self.status.value,
            "ipfs_cid": self.ipfs_cid,
            "backup_timestamp": self.backup_timestamp,
            "verification_hash": self.verification_hash,
            "size_bytes": self.size_bytes,
            "nodes_replicated": self.nodes_replicated,
            "metadata": self.metadata
        }


class IPFSPRBackupManager:
    """
    Manages complete mirroring of PR configurations to IPFS
    
    Protects repository from external escalations by maintaining
    immutable copies of all PR states.
    """
    
    def __init__(self, log_path: str = "logs/ipfs_pr_backup.log"):
        self.ipfs_manager = get_ipfs_manager() if get_ipfs_manager else None
        self.backup_records: Dict[str, BackupRecord] = {}
        self.pr_history: Dict[int, List[str]] = {}  # PR number -> list of backup IDs
        self.log_path = log_path
        self._ensure_log_directory()
        self._load_backup_index()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def _load_backup_index(self):
        """Load backup index from disk"""
        index_path = "backups/ipfs_pr_backup_index.json"
        if os.path.exists(index_path):
            try:
                with open(index_path, 'r') as f:
                    data = json.load(f)
                    # Reconstruct backup records
                    for backup_data in data.get("backups", []):
                        record = BackupRecord(
                            backup_id=backup_data["backup_id"],
                            pr_number=backup_data["pr_number"],
                            trigger=BackupTrigger(backup_data["trigger"]),
                            status=BackupStatus(backup_data["status"]),
                            ipfs_cid=backup_data.get("ipfs_cid"),
                            backup_timestamp=backup_data["backup_timestamp"],
                            verification_hash=backup_data["verification_hash"],
                            size_bytes=backup_data["size_bytes"],
                            nodes_replicated=backup_data.get("nodes_replicated", []),
                            metadata=backup_data.get("metadata", {})
                        )
                        self.backup_records[record.backup_id] = record
                    
                    self.pr_history = data.get("pr_history", {})
                    # Convert string keys back to int
                    self.pr_history = {int(k): v for k, v in self.pr_history.items()}
            except (json.JSONDecodeError, KeyError, ValueError):
                pass
    
    def _save_backup_index(self):
        """Save backup index to disk"""
        index_path = "backups/ipfs_pr_backup_index.json"
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_backups": len(self.backup_records),
            "backups": [record.to_dict() for record in self.backup_records.values()],
            "pr_history": self.pr_history
        }
        
        with open(index_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_backup_id(self, pr_number: int, trigger: BackupTrigger) -> str:
        """Generate unique backup ID"""
        timestamp = datetime.now(timezone.utc).isoformat()
        data = f"PR-{pr_number}-{trigger.value}-{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:20].upper()
    
    def backup_pr_configuration(self,
                                pr_config: PRConfiguration,
                                trigger: BackupTrigger = BackupTrigger.MANUAL,
                                metadata: Optional[Dict[str, Any]] = None) -> BackupRecord:
        """
        Backup a PR configuration to IPFS
        
        Args:
            pr_config: PR configuration to backup
            trigger: What triggered this backup
            metadata: Additional metadata
            
        Returns:
            BackupRecord with IPFS CID and status
        """
        backup_id = self._generate_backup_id(pr_config.pr_number, trigger)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Convert PR config to bytes
        pr_data = pr_config.to_json_bytes()
        
        # Calculate verification hash
        verification_hash = hashlib.sha256(pr_data).hexdigest()
        
        # Create backup record
        record = BackupRecord(
            backup_id=backup_id,
            pr_number=pr_config.pr_number,
            trigger=trigger,
            status=BackupStatus.IN_PROGRESS,
            ipfs_cid=None,
            backup_timestamp=timestamp,
            verification_hash=verification_hash,
            size_bytes=len(pr_data),
            nodes_replicated=[],
            metadata=metadata or {}
        )
        
        try:
            # Add to IPFS if manager available
            if self.ipfs_manager:
                ipfs_content = self.ipfs_manager.add_content(
                    pr_data,
                    "application/json",
                    {
                        "pr_number": pr_config.pr_number,
                        "trigger": trigger.value,
                        "backup_id": backup_id,
                        "type": "pr_configuration"
                    }
                )
                
                record.ipfs_cid = ipfs_content.cid
                record.nodes_replicated = ipfs_content.pinned_nodes
                record.status = BackupStatus.COMPLETED
                
                # Verify integrity
                audit = self.ipfs_manager.verify_content_integrity(ipfs_content.cid)
                if audit.cross_verification:
                    record.status = BackupStatus.VERIFIED
            else:
                # Fallback: store locally
                local_path = f"backups/pr_configs/PR-{pr_config.pr_number}-{backup_id}.json"
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(pr_data)
                
                record.ipfs_cid = f"local:{local_path}"
                record.status = BackupStatus.COMPLETED
            
            # Record in history
            self.backup_records[backup_id] = record
            
            if pr_config.pr_number not in self.pr_history:
                self.pr_history[pr_config.pr_number] = []
            self.pr_history[pr_config.pr_number].append(backup_id)
            
            # Save index
            self._save_backup_index()
            
            self._log_event("PR_BACKUP_COMPLETED",
                          f"PR #{pr_config.pr_number}, Backup ID: {backup_id}, "
                          f"CID: {record.ipfs_cid}, Size: {record.size_bytes} bytes")
            
        except Exception as e:
            record.status = BackupStatus.FAILED
            record.metadata["error"] = str(e)
            self._log_event("PR_BACKUP_FAILED",
                          f"PR #{pr_config.pr_number}, Error: {str(e)}")
        
        return record
    
    def get_pr_backups(self, pr_number: int) -> List[BackupRecord]:
        """Get all backups for a specific PR"""
        backup_ids = self.pr_history.get(pr_number, [])
        return [self.backup_records[bid] for bid in backup_ids if bid in self.backup_records]
    
    def get_latest_backup(self, pr_number: int) -> Optional[BackupRecord]:
        """Get the latest backup for a PR"""
        backups = self.get_pr_backups(pr_number)
        if not backups:
            return None
        
        # Sort by timestamp
        backups.sort(key=lambda b: b.backup_timestamp, reverse=True)
        return backups[0]
    
    def verify_backup_integrity(self, backup_id: str) -> Tuple[bool, str]:
        """
        Verify integrity of a backup
        
        Returns:
            Tuple of (is_valid, message)
        """
        if backup_id not in self.backup_records:
            return False, "Backup not found"
        
        record = self.backup_records[backup_id]
        
        if not record.ipfs_cid:
            return False, "No IPFS CID"
        
        if self.ipfs_manager and not record.ipfs_cid.startswith("local:"):
            # Verify through IPFS
            audit = self.ipfs_manager.verify_content_integrity(record.ipfs_cid)
            
            if audit.cross_verification:
                return True, "Integrity verified through IPFS"
            else:
                return False, f"Integrity check failed: {', '.join(audit.discrepancies)}"
        else:
            # Verify local file
            if record.ipfs_cid.startswith("local:"):
                local_path = record.ipfs_cid[6:]  # Remove "local:" prefix
                if os.path.exists(local_path):
                    with open(local_path, 'rb') as f:
                        data = f.read()
                        file_hash = hashlib.sha256(data).hexdigest()
                        
                        if file_hash == record.verification_hash:
                            return True, "Local backup integrity verified"
                        else:
                            return False, "Hash mismatch"
                else:
                    return False, "Local backup file not found"
        
        return False, "Unable to verify"
    
    def detect_escalation_threat(self) -> Dict[str, Any]:
        """
        Detect potential external escalation threats
        
        Monitors for suspicious patterns that might indicate
        external attempts to modify or delete PR history.
        
        Returns:
            Threat assessment report
        """
        threat_indicators = []
        threat_level = "NONE"
        
        # Check for missing backups
        missing_backups = [
            backup_id for backup_id, record in self.backup_records.items()
            if record.status == BackupStatus.FAILED
        ]
        
        if missing_backups:
            threat_indicators.append({
                "type": "FAILED_BACKUPS",
                "count": len(missing_backups),
                "severity": "MEDIUM"
            })
            threat_level = "MEDIUM"
        
        # Check for integrity failures
        integrity_failures = 0
        for backup_id in list(self.backup_records.keys())[:MAX_BACKUPS_TO_CHECK]:
            is_valid, _ = self.verify_backup_integrity(backup_id)
            if not is_valid:
                integrity_failures += 1
        
        if integrity_failures > 0:
            threat_indicators.append({
                "type": "INTEGRITY_FAILURES",
                "count": integrity_failures,
                "severity": "HIGH" if integrity_failures > 5 else "MEDIUM"
            })
            if integrity_failures > 5:
                threat_level = "HIGH"
            elif threat_level == "NONE":
                threat_level = "MEDIUM"
        
        # Check replication status
        if self.ipfs_manager:
            poorly_replicated = [
                record for record in self.backup_records.values()
                if len(record.nodes_replicated) < 2
            ]
            
            if len(poorly_replicated) > len(self.backup_records) * POOR_REPLICATION_THRESHOLD:
                threat_indicators.append({
                    "type": "POOR_REPLICATION",
                    "count": len(poorly_replicated),
                    "severity": "MEDIUM"
                })
                if threat_level == "NONE":
                    threat_level = "MEDIUM"
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "threat_level": threat_level,
            "indicators": threat_indicators,
            "total_backups": len(self.backup_records),
            "recommendations": self._generate_threat_recommendations(threat_indicators)
        }
    
    def _generate_threat_recommendations(self, indicators: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on threat indicators"""
        recommendations = []
        
        for indicator in indicators:
            if indicator["type"] == "FAILED_BACKUPS":
                recommendations.append(
                    "⚠️ Retry failed backups immediately"
                )
            elif indicator["type"] == "INTEGRITY_FAILURES":
                recommendations.append(
                    "🔍 Investigate integrity failures and restore from healthy nodes"
                )
            elif indicator["type"] == "POOR_REPLICATION":
                recommendations.append(
                    "📡 Increase replication factor and sync to more nodes"
                )
        
        if not recommendations:
            recommendations.append("✅ No immediate action required")
        
        return recommendations
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get backup system statistics"""
        total_backups = len(self.backup_records)
        
        status_counts = {}
        for status in BackupStatus:
            status_counts[status.value] = len([
                r for r in self.backup_records.values()
                if r.status == status
            ])
        
        trigger_counts = {}
        for trigger in BackupTrigger:
            trigger_counts[trigger.value] = len([
                r for r in self.backup_records.values()
                if r.trigger == trigger
            ])
        
        total_size = sum(r.size_bytes for r in self.backup_records.values())
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_backups": total_backups,
            "total_prs": len(self.pr_history),
            "by_status": status_counts,
            "by_trigger": trigger_counts,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "ipfs_enabled": self.ipfs_manager is not None
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get PR backup dashboard data"""
        stats = self.get_backup_statistics()
        threat_assessment = self.detect_escalation_threat()
        
        # Recent backups
        recent_backups = sorted(
            self.backup_records.values(),
            key=lambda r: r.backup_timestamp,
            reverse=True
        )[:10]
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "statistics": stats,
            "threat_assessment": threat_assessment,
            "recent_backups": [r.to_dict() for r in recent_backups],
            "system_health": "HEALTHY" if threat_assessment["threat_level"] == "NONE" else "DEGRADED"
        }
    
    def _log_event(self, event_type: str, message: str):
        """Log backup event"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            with open(self.log_path, 'a') as f:
                f.write(f"[{event_type}] {timestamp} | {message}\n")
        except (OSError, IOError):
            pass


# Global instance
_pr_backup_manager: Optional[IPFSPRBackupManager] = None


def get_pr_backup_manager() -> IPFSPRBackupManager:
    """Get or create global PR backup manager"""
    global _pr_backup_manager
    if _pr_backup_manager is None:
        _pr_backup_manager = IPFSPRBackupManager()
    return _pr_backup_manager


if __name__ == "__main__":
    # Demo
    print("📦 IPFS PR Backup System Demo")
    print("=" * 60)
    
    manager = IPFSPRBackupManager()
    
    # Create a sample PR configuration
    print("\n📝 Creating sample PR configuration...")
    pr_config = PRConfiguration(
        pr_number=42,
        title="Implement Lex Amoris Security Features",
        description="Adding rhythm validation, lazy security, and rescue channel",
        branch="feature/lex-amoris-security",
        base_branch="main",
        files_changed=[
            "core/lex_amoris_security.py",
            "core/lex_amoris_rescue.py",
            "core/ipfs_pr_backup.py"
        ],
        commits=[
            {
                "sha": "abc123",
                "message": "Add rhythm validation",
                "author": "euystacio-ai"
            }
        ],
        metadata={"labels": ["enhancement", "security"]},
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat()
    )
    
    # Backup the PR
    print("\n💾 Backing up PR to IPFS...")
    record = manager.backup_pr_configuration(
        pr_config,
        trigger=BackupTrigger.PR_CREATED,
        metadata={"priority": "high"}
    )
    print(f"   Backup ID: {record.backup_id}")
    print(f"   Status: {record.status.value}")
    print(f"   IPFS CID: {record.ipfs_cid}")
    print(f"   Size: {record.size_bytes} bytes")
    
    # Verify integrity
    print("\n🔍 Verifying backup integrity...")
    is_valid, message = manager.verify_backup_integrity(record.backup_id)
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")
    
    # Check for threats
    print("\n⚠️ Checking for escalation threats...")
    threat = manager.detect_escalation_threat()
    print(f"   Threat Level: {threat['threat_level']}")
    print(f"   Indicators: {len(threat['indicators'])}")
    
    # Get statistics
    print("\n📊 Backup Statistics:")
    stats = manager.get_backup_statistics()
    print(f"   Total Backups: {stats['total_backups']}")
    print(f"   Total PRs: {stats['total_prs']}")
    print(f"   Total Size: {stats['total_size_mb']} MB")
    print(f"   IPFS Enabled: {stats['ipfs_enabled']}")
    
    print("\n✅ IPFS PR Backup Demo Complete!")
