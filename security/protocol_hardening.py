#!/usr/bin/env python3
"""
Communication Protocol Hardening
QUIC + TLS 1.3 integration for secure, low-latency communication
"""

import os
import sys
import json
import ssl
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger = logging.getLogger(__name__)


class ProtocolHardeningConfig:
    """Configuration for protocol hardening with QUIC and TLS 1.3"""
    
    def __init__(self, config_path: str = "security/protocol_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load protocol configuration"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default secure configuration"""
        return {
            "tls": {
                "minimum_version": "TLS1_3",
                "allowed_versions": ["TLS1_3"],
                "cipher_suites": [
                    "TLS_AES_256_GCM_SHA384",
                    "TLS_CHACHA20_POLY1305_SHA256",
                    "TLS_AES_128_GCM_SHA256"
                ],
                "verify_mode": "CERT_REQUIRED",
                "check_hostname": True,
                "disable_insecure": True
            },
            "quic": {
                "enabled": True,
                "max_datagram_size": 1350,
                "initial_max_data": 10485760,
                "initial_max_stream_data_bidi_local": 1048576,
                "initial_max_stream_data_bidi_remote": 1048576,
                "initial_max_stream_data_uni": 1048576,
                "initial_max_streams_bidi": 100,
                "initial_max_streams_uni": 100,
                "max_idle_timeout": 30000,
                "max_ack_delay": 25
            },
            "security": {
                "disable_http": True,
                "disable_unencrypted": True,
                "enforce_hsts": True,
                "hsts_max_age": 31536000,
                "require_certificate_pinning": True,
                "allowed_protocols": ["h3", "http/1.1"],
                "min_dh_size": 2048
            },
            "logging": {
                "log_failed_connections": True,
                "log_protocol_downgrades": True,
                "alert_on_insecure_attempt": True
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        logger.info(f"Configuration saved to {self.config_path}")
    
    def create_tls_context(self) -> ssl.SSLContext:
        """Create hardened TLS context"""
        # Create context with TLS 1.3 only
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        
        # Set minimum TLS version to 1.3
        try:
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            logger.info("TLS 1.3 enforced")
        except AttributeError:
            # Fallback for older Python versions
            logger.warning("TLS 1.3 enforcement not available in this Python version")
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Set cipher suites
        try:
            # TLS 1.3 cipher suites
            context.set_ciphers(':'.join(self.config["tls"]["cipher_suites"]))
        except Exception as e:
            logger.warning(f"Could not set specific cipher suites: {e}")
        
        # Security options
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.options |= ssl.OP_NO_COMPRESSION
        context.options |= ssl.OP_SINGLE_DH_USE
        context.options |= ssl.OP_SINGLE_ECDH_USE
        
        # Verify mode
        if self.config["tls"]["verify_mode"] == "CERT_REQUIRED":
            context.verify_mode = ssl.CERT_REQUIRED
        
        # Check hostname
        context.check_hostname = self.config["tls"]["check_hostname"]
        
        logger.info("TLS context created with hardened configuration")
        return context
    
    def get_quic_config(self) -> Dict[str, Any]:
        """Get QUIC configuration"""
        return {
            "max_datagram_size": self.config["quic"]["max_datagram_size"],
            "initial_max_data": self.config["quic"]["initial_max_data"],
            "initial_max_stream_data_bidi_local": self.config["quic"]["initial_max_stream_data_bidi_local"],
            "initial_max_stream_data_bidi_remote": self.config["quic"]["initial_max_stream_data_bidi_remote"],
            "initial_max_stream_data_uni": self.config["quic"]["initial_max_stream_data_uni"],
            "initial_max_streams_bidi": self.config["quic"]["initial_max_streams_bidi"],
            "initial_max_streams_uni": self.config["quic"]["initial_max_streams_uni"],
            "max_idle_timeout": self.config["quic"]["max_idle_timeout"],
            "max_ack_delay": self.config["quic"]["max_ack_delay"]
        }
    
    def validate_connection(self, protocol: str, encrypted: bool) -> bool:
        """Validate if connection meets security requirements"""
        # Check if unencrypted connections are disabled
        if self.config["security"]["disable_unencrypted"] and not encrypted:
            logger.error("Unencrypted connection rejected")
            if self.config["logging"]["alert_on_insecure_attempt"]:
                self._log_security_alert("unencrypted_connection_attempt", {
                    "protocol": protocol,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            return False
        
        # Check if protocol is allowed
        if protocol not in self.config["security"]["allowed_protocols"]:
            logger.error(f"Protocol not allowed: {protocol}")
            return False
        
        # Check for HTTP (should be disabled)
        if self.config["security"]["disable_http"] and protocol.lower() in ["http", "http/1.0"]:
            logger.error("HTTP connections disabled, use HTTPS")
            return False
        
        logger.info(f"Connection validated: {protocol}, encrypted={encrypted}")
        return True
    
    def _log_security_alert(self, event_type: str, details: Dict[str, Any]):
        """Log security alert"""
        alert = {
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": "HIGH"
        }
        
        logger.warning(f"SECURITY ALERT: {json.dumps(alert)}")
        
        # Write to security log
        security_log_dir = os.path.join(os.getcwd(), "security")
        os.makedirs(security_log_dir, exist_ok=True)
        security_log = os.path.join(security_log_dir, "protocol_security.log")
        
        with open(security_log, 'a') as f:
            f.write(json.dumps(alert) + '\n')
    
    def get_nginx_config(self) -> str:
        """Generate nginx configuration for QUIC + TLS 1.3"""
        return """
# Nginx configuration for QUIC and TLS 1.3
server {
    listen 443 ssl http2;
    listen 443 quic reuseport;
    
    server_name euystacio.ai;
    
    # TLS 1.3 only
    ssl_protocols TLSv1.3;
    
    # Strong cipher suites for TLS 1.3
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256';
    ssl_prefer_server_ciphers on;
    
    # SSL certificate
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # QUIC parameters
    quic_retry on;
    ssl_early_data off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Disable insecure methods
    if ($request_method !~ ^(GET|HEAD|POST|PUT|DELETE|OPTIONS)$ ) {
        return 405;
    }
    
    # QUIC advertisement
    add_header Alt-Svc 'h3=":443"; ma=86400';
    
    location / {
        # Your application
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name euystacio.ai;
    return 301 https://$server_name$request_uri;
}
"""
    
    def get_apache_config(self) -> str:
        """Generate Apache configuration for QUIC + TLS 1.3"""
        return """
# Apache configuration for QUIC and TLS 1.3
<VirtualHost *:443>
    ServerName euystacio.ai
    
    # Enable HTTP/3 (QUIC)
    Protocols h2 http/1.1 h3
    
    # TLS Configuration
    SSLEngine on
    SSLProtocol -all +TLSv1.3
    SSLCipherSuite TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
    SSLHonorCipherOrder on
    
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
    
    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    
    # Security headers
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # QUIC Alt-Svc header
    Header always set Alt-Svc 'h3=":443"; ma=86400'
    
    # Document root
    DocumentRoot /var/www/euystacio
    
    <Directory /var/www/euystacio>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName euystacio.ai
    Redirect permanent / https://euystacio.ai/
</VirtualHost>
"""
    
    def generate_certificate_config(self) -> str:
        """Generate OpenSSL configuration for certificate generation"""
        return """
[req]
default_bits = 4096
default_md = sha256
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = IT
ST = State
L = City
O = Euystacio AI
OU = Security
CN = euystacio.ai
emailAddress = security@euystacio.ai

[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = euystacio.ai
DNS.2 = *.euystacio.ai
DNS.3 = localhost
"""
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get protocol security status"""
        return {
            "tls_version": self.config["tls"]["minimum_version"],
            "quic_enabled": self.config["quic"]["enabled"],
            "unencrypted_disabled": self.config["security"]["disable_unencrypted"],
            "http_disabled": self.config["security"]["disable_http"],
            "hsts_enabled": self.config["security"]["enforce_hsts"],
            "allowed_protocols": self.config["security"]["allowed_protocols"],
            "cipher_suites_count": len(self.config["tls"]["cipher_suites"]),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def main():
    """Main entry point"""
    # Initialize protocol hardening
    protocol_config = ProtocolHardeningConfig()
    
    # Save default config
    protocol_config.save_config()
    
    # Show security status
    status = protocol_config.get_security_status()
    logger.info("Protocol Hardening Status:")
    for key, value in status.items():
        logger.info(f"  {key}: {value}")
    
    # Generate configuration files
    nginx_config_path = "/home/runner/work/euystacio-ai/euystacio-ai/security/nginx-quic-tls13.conf"
    with open(nginx_config_path, 'w') as f:
        f.write(protocol_config.get_nginx_config())
    logger.info(f"Nginx config generated: {nginx_config_path}")
    
    apache_config_path = "/home/runner/work/euystacio-ai/euystacio-ai/security/apache-quic-tls13.conf"
    with open(apache_config_path, 'w') as f:
        f.write(protocol_config.get_apache_config())
    logger.info(f"Apache config generated: {apache_config_path}")
    
    cert_config_path = "/home/runner/work/euystacio-ai/euystacio-ai/security/openssl-cert.conf"
    with open(cert_config_path, 'w') as f:
        f.write(protocol_config.generate_certificate_config())
    logger.info(f"Certificate config generated: {cert_config_path}")
    
    # Test TLS context creation
    try:
        tls_context = protocol_config.create_tls_context()
        logger.info("TLS context created successfully")
    except Exception as e:
        logger.error(f"Failed to create TLS context: {e}")
    
    # Test connection validation
    logger.info("\nTesting connection validation:")
    logger.info(f"  HTTPS (h3): {protocol_config.validate_connection('h3', True)}")
    logger.info(f"  HTTP (unencrypted): {protocol_config.validate_connection('http', False)}")
    logger.info(f"  Unknown protocol: {protocol_config.validate_connection('unknown', True)}")


if __name__ == "__main__":
    main()
