#!/bin/bash
# Integration script for all security and resilience systems

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "======================================"
echo "Euystacio AI Security & Resilience"
echo "Integration Script"
echo "======================================"
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command availability
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 is not installed"
        return 1
    fi
}

# Function to check Python module
check_python_module() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python module '$1' is available"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Python module '$1' is not available"
        return 1
    fi
}

echo "Step 1: Checking dependencies..."
echo "================================"
echo

# Check Python
check_command python3 || {
    echo -e "${RED}Error: Python 3 is required${NC}"
    exit 1
}

# Check optional dependencies
check_command docker || echo "  Docker needed for monitoring"
check_command docker-compose || echo "  Docker Compose needed for monitoring"
check_command gpg || echo "  GPG needed for encryption/signatures"
check_command tor || echo "  Tor needed for forensic response"
check_command ipfs || echo "  IPFS needed for distributed backups"
check_command openssl || echo "  OpenSSL needed for certificates"

echo
echo "Step 2: Checking Python dependencies..."
echo "========================================"
echo

check_python_module "flask" || echo "  Install with: pip install flask"
check_python_module "cryptography" || echo "  Install with: pip install cryptography"

echo
echo "Step 3: Initializing directories..."
echo "===================================="
echo

# Create necessary directories
mkdir -p "$BASE_DIR/logs"
mkdir -p "$BASE_DIR/security"
mkdir -p "$BASE_DIR/backups"
mkdir -p "$BASE_DIR/firmware_updates"
mkdir -p "$BASE_DIR/monitoring"

echo -e "${GREEN}✓${NC} Directories initialized"

echo
echo "Step 4: Setting up configuration files..."
echo "=========================================="
echo

# Initialize configurations by running each Python script
cd "$BASE_DIR"

echo "Initializing forensic response system..."
python3 -c "
from security.forensic_response import ForensicResponseSystem
import os
os.makedirs('security', exist_ok=True)
frs = ForensicResponseSystem()
frs.save_config()
print('Forensic response configuration created')
" || echo -e "${YELLOW}⚠${NC} Could not initialize forensic response"

echo "Initializing protocol hardening..."
python3 -c "
from security.protocol_hardening import ProtocolHardeningConfig
import os
os.makedirs('security', exist_ok=True)
config = ProtocolHardeningConfig()
config.save_config()
print('Protocol hardening configuration created')
" || echo -e "${YELLOW}⚠${NC} Could not initialize protocol hardening"

echo "Initializing IPFS backup system..."
python3 -c "
from security.ipfs_backup import IPFSBackupSystem
import os
os.makedirs('backups', exist_ok=True)
ipfs = IPFSBackupSystem()
config = ipfs.setup_automated_backups()
print('IPFS backup configuration created')
" || echo -e "${YELLOW}⚠${NC} Could not initialize IPFS backup"

echo
echo "Step 5: System status check..."
echo "=============================="
echo

echo "Forensic Response System:"
python3 -c "
from security.forensic_response import ForensicResponseSystem
frs = ForensicResponseSystem()
status = frs.get_status()
for key, value in status.items():
    print(f'  {key}: {value}')
" 2>/dev/null || echo -e "${YELLOW}⚠${NC} Status unavailable"

echo
echo "IPFS Backup System:"
python3 -c "
from security.ipfs_backup import IPFSBackupSystem
ipfs = IPFSBackupSystem()
status = ipfs.get_backup_status()
for key, value in status.items():
    print(f'  {key}: {value}')
" 2>/dev/null || echo -e "${YELLOW}⚠${NC} Status unavailable"

echo
echo "Protocol Security:"
python3 -c "
from security.protocol_hardening import ProtocolHardeningConfig
config = ProtocolHardeningConfig()
status = config.get_security_status()
for key, value in status.items():
    print(f'  {key}: {value}')
" 2>/dev/null || echo -e "${YELLOW}⚠${NC} Status unavailable"

echo
echo "======================================"
echo "Integration Complete!"
echo "======================================"
echo
echo "Next steps:"
echo "1. Start monitoring stack:"
echo "   cd monitoring && docker-compose up -d"
echo
echo "2. Access Grafana:"
echo "   http://localhost:3000 (admin/admin)"
echo
echo "3. Start forensic monitoring:"
echo "   python3 security/forensic_response.py"
echo
echo "4. Configure GPG keys for backups:"
echo "   gpg --full-generate-key"
echo
echo "5. Initialize IPFS daemon:"
echo "   ipfs daemon &"
echo
echo "6. Review security README:"
echo "   cat security/README.md"
echo
echo "For more information, see: security/README.md"
