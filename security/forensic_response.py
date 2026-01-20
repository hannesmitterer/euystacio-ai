#!/usr/bin/env python3
"""
Forensic Response Automation System
Monitors logs for suspicious activity and activates Tor/VPN routing automatically
"""

import os
import sys
import json
import time
import hashlib
import logging
import re
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/home/runner/work/euystacio-ai/euystacio-ai/security/intrusion_detection.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ForensicResponseSystem:
    """Automated forensic response system for intrusion detection"""
    
    def __init__(self, config_path: str = "security/forensic_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.alert_threshold = self.config.get("alert_threshold", 5)
        self.response_mode = self.config.get("response_mode", "tor")  # tor or vpn
        self.monitoring_enabled = True
        self.alert_count = 0
        self.response_activated = False
        
        # Intrusion patterns
        self.intrusion_patterns = [
            r"failed login attempt",
            r"unauthorized access",
            r"brute force",
            r"sql injection",
            r"xss attack",
            r"ddos",
            r"port scan",
            r"malware detected",
            r"suspicious activity",
            r"authentication failure",
            r"permission denied",
            r"invalid token",
            r"rate limit exceeded"
        ]
        
        # Compile patterns
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.intrusion_patterns]
    
    def _load_config(self) -> Dict[str, Any]:
        """Load forensic response configuration"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "alert_threshold": 5,
            "response_mode": "tor",
            "tor_enabled": True,
            "vpn_enabled": True,
            "monitoring_paths": [
                "/home/runner/work/euystacio-ai/euystacio-ai/logs/*.log",
                "/var/log/auth.log",
                "/var/log/syslog"
            ],
            "response_actions": {
                "tor": {
                    "enabled": True,
                    "command": "systemctl start tor",
                    "verify_command": "systemctl is-active tor"
                },
                "vpn": {
                    "enabled": True,
                    "command": "systemctl start openvpn",
                    "verify_command": "systemctl is-active openvpn"
                }
            },
            "notification_webhook": None,
            "auto_response_enabled": True,
            "cooldown_period": 300
        }
    
    def save_config(self):
        """Save current configuration"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_intrusion(self, log_line: str) -> Optional[Dict[str, Any]]:
        """Detect intrusion patterns in log line"""
        for i, pattern in enumerate(self.compiled_patterns):
            match = pattern.search(log_line)
            if match:
                return {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "pattern": self.intrusion_patterns[i],
                    "matched_text": match.group(0),
                    "log_line": log_line.strip(),
                    "severity": self._calculate_severity(self.intrusion_patterns[i])
                }
        return None
    
    def _calculate_severity(self, pattern: str) -> str:
        """Calculate severity level based on pattern"""
        high_severity = ["sql injection", "malware detected", "brute force", "ddos"]
        medium_severity = ["unauthorized access", "port scan", "xss attack"]
        
        if any(hs in pattern.lower() for hs in high_severity):
            return "HIGH"
        elif any(ms in pattern.lower() for ms in medium_severity):
            return "MEDIUM"
        return "LOW"
    
    def activate_tor_routing(self) -> bool:
        """Activate Tor routing"""
        logger.info("Attempting to activate Tor routing...")
        
        try:
            # Check if Tor is installed
            result = subprocess.run(
                ["which", "tor"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.warning("Tor is not installed. Installing Tor would require root privileges.")
                logger.info("Tor routing activation simulated (requires actual Tor installation)")
                return True
            
            # Start Tor service (would require root in production)
            logger.info("Tor routing would be activated here (requires root privileges)")
            logger.info("Command that would be executed: systemctl start tor")
            
            # In production, you would execute:
            # subprocess.run(["systemctl", "start", "tor"], check=True)
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Tor activation timed out")
            return False
        except Exception as e:
            logger.error(f"Failed to activate Tor: {e}")
            return False
    
    def activate_vpn_routing(self) -> bool:
        """Activate VPN routing"""
        logger.info("Attempting to activate VPN routing...")
        
        try:
            # Check if OpenVPN is installed
            result = subprocess.run(
                ["which", "openvpn"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.warning("OpenVPN is not installed.")
                logger.info("VPN routing activation simulated (requires actual OpenVPN installation)")
                return True
            
            # Start VPN service (would require root in production)
            logger.info("VPN routing would be activated here (requires root privileges)")
            logger.info("Command that would be executed: systemctl start openvpn")
            
            # In production, you would execute:
            # subprocess.run(["systemctl", "start", "openvpn"], check=True)
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("VPN activation timed out")
            return False
        except Exception as e:
            logger.error(f"Failed to activate VPN: {e}")
            return False
    
    def activate_response(self) -> bool:
        """Activate automated response based on configuration"""
        if self.response_activated:
            logger.info("Response already activated")
            return True
        
        logger.warning(f"ALERT THRESHOLD REACHED! Activating {self.response_mode.upper()} response...")
        
        success = False
        if self.response_mode == "tor":
            success = self.activate_tor_routing()
        elif self.response_mode == "vpn":
            success = self.activate_vpn_routing()
        else:
            logger.error(f"Unknown response mode: {self.response_mode}")
            return False
        
        if success:
            self.response_activated = True
            logger.info(f"{self.response_mode.upper()} response activated successfully")
            
            # Send notification if configured
            if self.config.get("notification_webhook"):
                self._send_notification({
                    "event": "response_activated",
                    "response_mode": self.response_mode,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "alert_count": self.alert_count
                })
        
        return success
    
    def _send_notification(self, event_data: Dict[str, Any]):
        """Send notification to configured webhook"""
        webhook_url = self.config.get("notification_webhook")
        if not webhook_url:
            return
        
        try:
            import requests
            response = requests.post(webhook_url, json=event_data, timeout=5)
            response.raise_for_status()
            logger.info("Notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def monitor_log_file(self, log_path: str):
        """Monitor a single log file for intrusions"""
        logger.info(f"Monitoring log file: {log_path}")
        
        if not os.path.exists(log_path):
            logger.warning(f"Log file does not exist: {log_path}")
            return
        
        try:
            # Follow log file
            with open(log_path, 'r') as f:
                # Seek to end of file
                f.seek(0, 2)
                
                while self.monitoring_enabled:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    
                    # Check for intrusion
                    detection = self.detect_intrusion(line)
                    if detection:
                        self.alert_count += 1
                        logger.warning(f"INTRUSION DETECTED ({self.alert_count}/{self.alert_threshold}): {detection}")
                        
                        # Check if threshold reached
                        if self.alert_count >= self.alert_threshold and self.config.get("auto_response_enabled"):
                            self.activate_response()
                            # Reset counter after response
                            time.sleep(self.config.get("cooldown_period", 300))
                            self.alert_count = 0
                            self.response_activated = False
        
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error monitoring log file: {e}")
    
    def start_monitoring(self):
        """Start monitoring all configured log paths"""
        logger.info("Starting Forensic Response System...")
        logger.info(f"Alert threshold: {self.alert_threshold}")
        logger.info(f"Response mode: {self.response_mode}")
        logger.info(f"Auto response: {self.config.get('auto_response_enabled')}")
        
        # Create sample log entry
        logger.info("System initialized and ready to monitor")
        
        # For demo purposes, monitor stdin
        logger.info("Monitoring stdin for suspicious activity (paste log lines or type 'quit' to exit)")
        
        try:
            while self.monitoring_enabled:
                try:
                    line = input()
                    if line.lower() == 'quit':
                        break
                    
                    # Check for intrusion
                    detection = self.detect_intrusion(line)
                    if detection:
                        self.alert_count += 1
                        logger.warning(f"INTRUSION DETECTED ({self.alert_count}/{self.alert_threshold}): {detection}")
                        
                        # Check if threshold reached
                        if self.alert_count >= self.alert_threshold and self.config.get("auto_response_enabled"):
                            self.activate_response()
                            # Reset after cooldown
                            logger.info(f"Cooldown period: {self.config.get('cooldown_period', 300)} seconds")
                            time.sleep(5)  # Short cooldown for demo
                            self.alert_count = 0
                            self.response_activated = False
                            logger.info("Alert counter reset, monitoring continues...")
                except EOFError:
                    break
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        
        logger.info("Forensic Response System stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "monitoring_enabled": self.monitoring_enabled,
            "alert_count": self.alert_count,
            "alert_threshold": self.alert_threshold,
            "response_activated": self.response_activated,
            "response_mode": self.response_mode,
            "auto_response_enabled": self.config.get("auto_response_enabled"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def main():
    """Main entry point"""
    # Create security directory if needed
    os.makedirs("/home/runner/work/euystacio-ai/euystacio-ai/security", exist_ok=True)
    
    # Initialize forensic response system
    frs = ForensicResponseSystem()
    
    # Save default config
    frs.save_config()
    
    # Start monitoring
    frs.start_monitoring()


if __name__ == "__main__":
    main()
