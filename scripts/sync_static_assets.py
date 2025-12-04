#!/usr/bin/env python3
"""
Static Assets Synchronization Script

This script synchronizes key static assets (like red_code.json) to both 
frontend and backend deployment directories, ensuring consistency across
all environments.

Usage:
    python scripts/sync_static_assets.py [--force] [--verify-only]

Options:
    --force         Force sync even if checksums match
    --verify-only   Only verify integrity, don't sync
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent
STATIC_BUILD_DIR = REPO_ROOT / "static_build"
DATA_DIR = STATIC_BUILD_DIR / "data"

# Files to sync (source -> relative destination in static_build)
SYNC_FILES = [
    ("red_code.json", "data/red_code.json"),
    ("HARMONIC_CONFIRMATION_CUSTOS_SENTIMENTO.json", "data/harmonic_confirmation.json"),
    ("SIGIL_CUSTOS_SENTIMENTO.json", "data/sigil.json"),
    ("ACTUS_RESONANTIAE_CUSTOS_SENTIMENTO.json", "data/actus_resonantiae.json"),
    ("fractal_registry.json", "data/fractal_registry.json"),
    ("reflection_tree.json", "data/reflection_tree.json"),
]

# Required fields for governance files
REQUIRED_FIELDS = {
    "red_code.json": ["core_truth", "sentimento_rhythm", "ai_signature"],
}


def calculate_checksum(filepath: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    if not filepath.exists():
        return ""
    
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_json_integrity(filepath: Path, required_fields: list = None) -> tuple:
    """
    Verify JSON file integrity.
    Returns (is_valid, error_message).
    """
    if not filepath.exists():
        return False, f"File not found: {filepath}"
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Try to parse JSON, handling potential literal \n in content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Try replacing literal \n with actual newlines
            content_fixed = content.replace('\\n', '\n')
            data = json.loads(content_fixed)
        
        # Check required fields
        if required_fields:
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return False, f"Missing required fields: {missing_fields}"
        
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def sync_file(source: Path, dest: Path, force: bool = False) -> bool:
    """
    Sync a single file from source to destination.
    Returns True if file was synced.
    """
    if not source.exists():
        print(f"  ⚠ Source not found: {source.name}")
        return False
    
    # Create destination directory if needed
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if sync is needed
    source_checksum = calculate_checksum(source)
    dest_checksum = calculate_checksum(dest)
    
    if source_checksum == dest_checksum and not force:
        print(f"  ✓ {source.name} - Already synced")
        return False
    
    # Copy file
    shutil.copy2(source, dest)
    print(f"  ✓ {source.name} -> {dest.relative_to(REPO_ROOT)}")
    return True


def generate_sync_manifest(synced_files: list) -> dict:
    """Generate a manifest of synced files."""
    manifest = {
        "sync_timestamp": datetime.now(timezone.utc).isoformat(),
        "files": [],
        "integrity_verified": True,
    }
    
    for source_name, dest_rel in SYNC_FILES:
        source = REPO_ROOT / source_name
        dest = STATIC_BUILD_DIR / dest_rel
        
        if source.exists():
            manifest["files"].append({
                "source": source_name,
                "destination": dest_rel,
                "checksum": calculate_checksum(source),
                "synced": source_name in synced_files,
            })
    
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Sync static assets")
    parser.add_argument("--force", action="store_true", help="Force sync all files")
    parser.add_argument("--verify-only", action="store_true", help="Only verify integrity")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Euystacio Static Assets Synchronization")
    print("=" * 60)
    print()
    
    # Step 1: Verify integrity of source files
    print("Step 1: Verifying source file integrity...")
    errors = []
    for source_name, _ in SYNC_FILES:
        source = REPO_ROOT / source_name
        if not source.exists():
            print(f"  ⚠ {source_name} - Not found (optional)")
            continue
        
        required_fields = REQUIRED_FIELDS.get(source_name, [])
        is_valid, error = verify_json_integrity(source, required_fields)
        
        if is_valid:
            print(f"  ✓ {source_name} - Valid")
        else:
            print(f"  ✗ {source_name} - {error}")
            errors.append(error)
    
    if errors:
        print("\n✗ Integrity verification failed!")
        sys.exit(1)
    
    print("\n✓ All source files verified")
    
    if args.verify_only:
        print("\n--verify-only mode: Skipping sync")
        sys.exit(0)
    
    # Step 2: Create output directory
    print("\nStep 2: Preparing sync directories...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created: {DATA_DIR.relative_to(REPO_ROOT)}")
    
    # Step 3: Sync files
    print("\nStep 3: Syncing files...")
    synced_files = []
    for source_name, dest_rel in SYNC_FILES:
        source = REPO_ROOT / source_name
        dest = STATIC_BUILD_DIR / dest_rel
        
        if sync_file(source, dest, force=args.force):
            synced_files.append(source_name)
    
    # Step 4: Generate manifest
    print("\nStep 4: Generating sync manifest...")
    manifest = generate_sync_manifest(synced_files)
    manifest_path = DATA_DIR / "sync_manifest.json"
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"  ✓ Manifest: {manifest_path.relative_to(REPO_ROOT)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Sync Complete!")
    print(f"  Files synced: {len(synced_files)}")
    print(f"  Total files:  {len([f for f in SYNC_FILES if (REPO_ROOT / f[0]).exists()])}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
