import requests
import os
import re

# --- CONFIGURATION ---
PINATA_API_KEY = "YOUR_PINATA_API_KEY"
PINATA_SECRET_KEY = "YOUR_PINATA_SECRET_KEY"
FILE_NAME = "README.md"

# This variable will be automatically updated by the script after upload
IPFS_CID = "Qm_PLACEHOLDER_INIT" 

def generate_readme_content(cid):
    """Generates the Markdown string with the current CID."""
    return f"""# 🌌 EUS-2026: The Living Covenant
    
## 🛡️ Master Metadata Guard
- **IPFS_ANCHOR**: ipfs://{cid}
- **NSR_STATUS**: ACTIVE
- **CONSECRATED**: 2026-04-11

---
[View on IPFS Gateway](https://gateway.pinata.cloud/ipfs/{cid})
"""

def upload_to_pinata(filepath):
    """Uploads file to Pinata and returns the new CID."""
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }
    
    with open(filepath, 'rb') as f:
        response = requests.post(url, files={'file': f}, headers=headers)
        
    if response.status_code == 200:
        return response.json()['IpfsHash']
    else:
        raise Exception(f"Pinata Error: {response.text}")

def update_script_cid(new_cid):
    """Updates the IPFS_CID variable inside this Python file."""
    with open(__file__, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find IPFS_CID = "..." and replace it
    new_content = re.sub(r'IPFS_CID = ".*?"', f'IPFS_CID = "{new_cid}"', content)
    
    with open(__file__, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    # 1. Create initial file with current (or placeholder) CID
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(generate_readme_content(IPFS_CID))
    
    print(f"🚀 Uploading {FILE_NAME} to Pinata...")
    new_hash = upload_to_pinata(FILE_NAME)
    print(f"✅ Success! New CID: {new_hash}")
    
    # 2. Update the script so the NEXT run uses the correct CID
    update_script_cid(new_hash)
    
    # 3. Regenerate the file one last time with the FINAL hash
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(generate_readme_content(new_hash))
    print("✨ Script and README synchronized.")
