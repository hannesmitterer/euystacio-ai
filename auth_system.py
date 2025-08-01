"""
auth_system.py
Simple authentication system for Euystacio admin roles.
Supports cofounders and seed bringer roles with session-based authentication.
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from functools import wraps
import hashlib
import secrets

# Import fractal systems for logging
try:
    from fractal_logger import get_fractal_logger
except ImportError:
    get_fractal_logger = lambda: None


class AuthSystem:
    def __init__(self):
        self.logger = get_fractal_logger()
        self.sessions = {}  # In-memory session storage
        self.admin_users = {
            "seed_bringer": {
                "username": "seed_bringer",
                "display_name": "Seed Bringer (bioarchitettura)",
                "role": "seed_bringer",
                "permissions": ["all"],
                "password_hash": self._hash_password("euystacio_genesis_2025"),  # Default password
                "created_at": "2025-01-31T00:00:00Z",
                "active": True
            },
            "cofounder_hannes": {
                "username": "cofounder_hannes", 
                "display_name": "Hannes Mitterer",
                "role": "cofounder",
                "permissions": ["tutor_nomination", "system_management", "pulse_management"],
                "password_hash": self._hash_password("hannes_cofounder_2025"),  # Default password
                "created_at": "2025-01-31T00:00:00Z",
                "active": True
            },
            "cofounder_admin": {
                "username": "cofounder_admin",
                "display_name": "Co-founder Admin",
                "role": "cofounder", 
                "permissions": ["tutor_nomination", "system_management"],
                "password_hash": self._hash_password("cofounder_admin_2025"),  # Default password
                "created_at": "2025-01-31T00:00:00Z",
                "active": True
            }
        }
        
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = "euystacio_seed_salt_2025"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user info if successful"""
        if username not in self.admin_users:
            return None
            
        user = self.admin_users[username]
        if not user["active"]:
            return None
            
        password_hash = self._hash_password(password)
        if password_hash != user["password_hash"]:
            return None
            
        # Log authentication
        if self.logger:
            self.logger.log_event("admin_authentication", {
                "username": username,
                "role": user["role"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        return user.copy()
    
    def create_session(self, user: Dict[str, Any]) -> str:
        """Create a new session for authenticated user"""
        session_token = self._generate_session_token()
        session_data = {
            "user": user,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=24),
            "last_activity": datetime.now(timezone.utc)
        }
        
        self.sessions[session_token] = session_data
        
        # Log session creation
        if self.logger:
            self.logger.log_event("admin_session_created", {
                "username": user["username"],
                "role": user["role"],
                "session_token": session_token[:8] + "...",  # Partial token for security
                "expires_at": session_data["expires_at"].isoformat()
            })
            
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate session token and return user if valid"""
        if not session_token or session_token not in self.sessions:
            return None
            
        session = self.sessions[session_token]
        
        # Check if session expired
        if datetime.now(timezone.utc) > session["expires_at"]:
            del self.sessions[session_token]
            return None
            
        # Update last activity
        session["last_activity"] = datetime.now(timezone.utc)
        
        return session["user"]
    
    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        if session_token in self.sessions:
            user = self.sessions[session_token]["user"]
            
            # Log logout
            if self.logger:
                self.logger.log_event("admin_logout", {
                    "username": user["username"],
                    "role": user["role"],
                    "session_token": session_token[:8] + "..."
                })
                
            del self.sessions[session_token]
            return True
        return False
    
    def has_permission(self, user: Dict[str, Any], permission: str) -> bool:
        """Check if user has specific permission"""
        if not user:
            return False
            
        user_permissions = user.get("permissions", [])
        return "all" in user_permissions or permission in user_permissions
    
    def is_admin(self, user: Dict[str, Any]) -> bool:
        """Check if user is an admin (cofounder or seed bringer)"""
        if not user:
            return False
        return user.get("role") in ["cofounder", "seed_bringer"]
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of active sessions (for admin monitoring)"""
        active_sessions = []
        current_time = datetime.now(timezone.utc)
        
        for token, session in list(self.sessions.items()):
            if current_time <= session["expires_at"]:
                active_sessions.append({
                    "username": session["user"]["username"],
                    "role": session["user"]["role"],
                    "created_at": session["created_at"].isoformat(),
                    "last_activity": session["last_activity"].isoformat(),
                    "expires_at": session["expires_at"].isoformat()
                })
            else:
                # Clean up expired sessions
                del self.sessions[token]
                
        return active_sessions
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if username not in self.admin_users:
            return False
            
        user = self.admin_users[username]
        old_hash = self._hash_password(old_password)
        
        if old_hash != user["password_hash"]:
            return False
            
        # Update password
        user["password_hash"] = self._hash_password(new_password)
        user["password_updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # Log password change
        if self.logger:
            self.logger.log_event("admin_password_changed", {
                "username": username,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        return True
    
    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information (without sensitive data)"""
        if username not in self.admin_users:
            return None
            
        user = self.admin_users[username].copy()
        # Remove sensitive information
        user.pop("password_hash", None)
        return user


# Global auth system instance
auth_system = AuthSystem()


def require_auth(permission: str = None):
    """Decorator to require authentication for Flask routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify, session
            
            # Check for session token in cookie or header
            session_token = request.cookies.get("euystacio_session") or request.headers.get("Authorization")
            if session_token and session_token.startswith("Bearer "):
                session_token = session_token[7:]
                
            user = auth_system.validate_session(session_token)
            if not user:
                return jsonify({"error": "Authentication required", "authenticated": False}), 401
                
            # Check permission if specified
            if permission and not auth_system.has_permission(user, permission):
                return jsonify({"error": "Insufficient permissions", "required_permission": permission}), 403
                
            # Add user to request context
            request.current_user = user
            return f(*args, **kwargs)
            
        return decorated_function
    return decorator


def require_admin(f):
    """Decorator to require admin role (cofounder or seed bringer)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        session_token = request.cookies.get("euystacio_session") or request.headers.get("Authorization")
        if session_token and session_token.startswith("Bearer "):
            session_token = session_token[7:]
            
        user = auth_system.validate_session(session_token)
        if not user or not auth_system.is_admin(user):
            return jsonify({"error": "Admin access required"}), 403
            
        request.current_user = user
        return f(*args, **kwargs)
        
    return decorated_function