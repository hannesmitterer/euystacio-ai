# Security Runbook

Comprehensive security guide for the Nexus API and EUYSTACIO Framework covering best practices, incident response, blacklist management, and operational procedures.

## Table of Contents

1. [Security Checklist](#security-checklist)
2. [Permanent Blacklist System](#permanent-blacklist-system)
3. [Authentication & Authorization](#authentication--authorization)
4. [Secret Management](#secret-management)
5. [Session Cleanup](#session-cleanup)
6. [Rate Limiting](#rate-limiting)
7. [Input Validation](#input-validation)
8. [Encryption](#encryption)
9. [Incident Response](#incident-response)
10. [Compliance](#compliance)
11. [Security Monitoring](#security-monitoring)

---

## Security Checklist

### Pre-Deployment Security Checklist

- [ ] All secrets stored in environment variables (no hardcoded credentials)
- [ ] API keys rotated and properly secured
- [ ] HTTPS/TLS enforced for all endpoints
- [ ] Input validation implemented for all endpoints
- [ ] Rate limiting configured and tested
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] CSRF protection enabled
- [ ] Session management properly configured
- [ ] Audit logging enabled
- [ ] Security headers configured
- [ ] Dependency vulnerabilities scanned
- [ ] Secrets scanning enabled in CI/CD
- [ ] Database access restricted
- [ ] Backup encryption enabled
- [ ] Incident response plan documented
- [ ] Security monitoring configured

### Post-Deployment Security Checklist

- [ ] API endpoints tested for vulnerabilities
- [ ] Rate limits verified
- [ ] Error messages don't leak sensitive info
- [ ] Authentication working correctly
- [ ] Authorization rules enforced
- [ ] Audit logs collecting properly
- [ ] Monitoring alerts configured
- [ ] Blacklist system initialized and operational
- [ ] Known threats added to blacklist

---

## Permanent Blacklist System

The EUYSTACIO framework includes a permanent blacklist management system to protect against malicious entities, suspicious nodes, and security threats.

### Overview

The Blacklist Manager provides:
- **Persistent blocking** of suspicious entities, IP addresses, and API keys
- **Integration** with the Red Code system for permanent storage
- **Automated logging** of security events
- **Backup integration** through the resilience system
- **Threat level classification** (LOW, MEDIUM, HIGH, CRITICAL)

### Using the Blacklist Manager

#### Import and Initialize

```python
from core import get_blacklist_manager, ThreatLevel, BlockReason

# Get the global blacklist manager instance
blacklist_manager = get_blacklist_manager()
```

#### Block an Entity

```python
# Block a suspicious node
result = blacklist_manager.add_entity(
    entity_id="suspicious_node_001",
    entity_type="node",
    reason=BlockReason.SUSPICIOUS_ACTIVITY,
    threat_level=ThreatLevel.HIGH,
    metadata={
        "detected_at": "2025-01-15T00:00:00Z",
        "indicators": ["high_frequency_requests", "invalid_auth"]
    }
)

# Block an IP address
result = blacklist_manager.add_ip_address(
    ip_address="192.168.1.100",
    reason=BlockReason.ATTACK_ATTEMPT,
    threat_level=ThreatLevel.CRITICAL
)

# Block an API key (provide the SHA-256 hash)
import hashlib
api_key_hash = hashlib.sha256("compromised_key".encode()).hexdigest()
result = blacklist_manager.add_api_key(
    api_key_hash=api_key_hash,
    reason=BlockReason.DATA_THEFT,
    threat_level=ThreatLevel.CRITICAL
)
```

#### Check if Blocked

```python
# Check if entity is blocked
if blacklist_manager.is_entity_blocked("suspicious_node_001"):
    print("Entity is blacklisted - blocking request")

# Check if IP is blocked
if blacklist_manager.is_ip_blocked("192.168.1.100"):
    print("IP address is blacklisted - blocking request")

# Check if API key is blocked (provide the actual key, it will be hashed)
if blacklist_manager.is_api_key_blocked("api_key_value"):
    print("API key is blacklisted - blocking request")
```

#### Remove from Blacklist

```python
# Remove an entity (e.g., false positive)
result = blacklist_manager.remove_entity("entity_id")

# Remove an IP address
result = blacklist_manager.remove_ip_address("192.168.1.100")
```

#### Get Statistics

```python
# Get blacklist statistics
stats = blacklist_manager.get_blacklist_stats()
print(f"Total entities blocked: {stats['total_entities_blocked']}")
print(f"Total IPs blocked: {stats['total_ips_blocked']}")
print(f"Threat distribution: {stats['threat_distribution']}")

# Get list of blacklisted entities
entities = blacklist_manager.get_blacklisted_entities()
for entity in entities:
    print(f"{entity['entity_id']}: {entity['threat_level']} - {entity['reason']}")
```

### Integration with API Endpoints

Example middleware for request validation:

```python
def validate_request_middleware(req, res, next):
    """Validate incoming request against blacklist"""
    blacklist_manager = get_blacklist_manager()
    
    entity_id = req.get('entity_id')
    ip_address = req.get('ip_address')
    api_key = req.headers.get('Authorization', '').replace('Bearer ', '')
    
    # Check entity
    if entity_id and blacklist_manager.is_entity_blocked(entity_id):
        return res.status(403).json({
            'error': 'Access denied - entity blacklisted'
        })
    
    # Check IP
    if ip_address and blacklist_manager.is_ip_blocked(ip_address):
        return res.status(403).json({
            'error': 'Access denied - IP address blacklisted'
        })
    
    # Check API key
    if api_key and blacklist_manager.is_api_key_blocked(api_key):
        return res.status(403).json({
            'error': 'Access denied - API key blacklisted'
        })
    
    next()
```

### Threat Levels

| Level | Usage | Response |
|-------|-------|----------|
| **LOW** | Minor policy violations, first-time suspicious behavior | Monitor, log |
| **MEDIUM** | Repeated suspicious activity, potential threats | Block, alert team |
| **HIGH** | Active attack attempts, data exfiltration | Block, immediate investigation |
| **CRITICAL** | Confirmed malicious activity, system compromise | Block, emergency escalation |

### Block Reasons

- `SUSPICIOUS_ACTIVITY`: Unusual or potentially malicious behavior
- `ATTACK_ATTEMPT`: Active attack on the system
- `DATA_THEFT`: Attempted or successful data exfiltration
- `POLICY_VIOLATION`: Violation of usage policies
- `SECURITY_THREAT`: Identified security threat
- `ECOSYSTEM_TESTING`: Unauthorized access during ecosystem testing phase

### Blacklist Persistence

The blacklist data is permanently stored in the Red Code system (`red_code.json`) and backed up through the resilience system:

```python
# Blacklist data is automatically saved in red_code.json
{
  "security_blacklist": {
    "entities": { ... },
    "ip_addresses": { ... },
    "api_keys": { ... },
    "metadata": {
      "created": "2025-01-15T00:00:00Z",
      "last_updated": "2025-01-15T12:00:00Z",
      "total_blocked": 42
    }
  }
}
```

### Security Audit

Perform regular security audits:

```python
# Get integrity verification
integrity = blacklist_manager.verify_blacklist_integrity()
print(f"Integrity verified: {integrity['verified']}")
print(f"Integrity hash: {integrity['integrity_hash']}")

# Review statistics
stats = blacklist_manager.get_blacklist_stats()
print(f"Total block attempts: {stats['total_block_attempts']}")

# Review high-threat entities
entities = blacklist_manager.get_blacklisted_entities()
high_threat = [e for e in entities if e['threat_level'] in ['high', 'critical']]
print(f"High-threat entities: {len(high_threat)}")
```

### Best Practices

1. ✅ **Regular audits**: Review blacklist entries weekly
2. ✅ **Document reasons**: Always provide detailed metadata for blocks
3. ✅ **Monitor block attempts**: Track entities attempting to access after blocking
4. ✅ **Verify integrity**: Regularly verify blacklist integrity
5. ✅ **Update threat levels**: Escalate threat levels based on behavior
6. ✅ **Remove false positives**: Promptly remove incorrectly blocked entities
7. ✅ **Backup integration**: Ensure blacklist is included in system backups


- [ ] SSL/TLS certificate valid
- [ ] Security headers present in responses
- [ ] Backup procedures tested

---

## Authentication & Authorization

### API Key Management

#### Generating Secure API Keys

```javascript
const crypto = require('crypto');

function generateApiKey() {
  const prefix = 'nexus_api';
  const key = crypto.randomBytes(32).toString('hex');
  return `${prefix}_${key}`;
}

// Store hash, not plaintext
function hashApiKey(apiKey) {
  return crypto
    .createHash('sha256')
    .update(apiKey)
    .digest('hex');
}
```

#### API Key Validation

```javascript
async function validateApiKey(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: 'Missing or invalid authorization header'
    });
  }
  
  const apiKey = authHeader.replace('Bearer ', '');
  const keyHash = hashApiKey(apiKey);
  
  // Lookup in database
  const keyRecord = await db.apiKeys.findOne({
    key_hash: keyHash,
    active: true,
    expires_at: { $gt: new Date() }
  });
  
  if (!keyRecord) {
    // Log failed attempt
    await logSecurityEvent({
      type: 'invalid_api_key',
      ip: req.ip,
      timestamp: new Date()
    });
    
    return res.status(401).json({
      error: 'Invalid or expired API key'
    });
  }
  
  // Attach user context
  req.user = {
    userId: keyRecord.user_id,
    scopes: keyRecord.scopes
  };
  
  // Update last used
  await db.apiKeys.updateOne(
    { _id: keyRecord._id },
    { $set: { last_used_at: new Date() } }
  );
  
  next();
}
```

### JWT Token Security

#### Token Generation

```javascript
const jwt = require('jsonwebtoken');

function generateJWT(userId, scopes) {
  const payload = {
    sub: userId,
    scopes: scopes,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (3600 * 24) // 24 hours
  };
  
  return jwt.sign(payload, process.env.JWT_SECRET, {
    algorithm: 'HS256'
  });
}
```

#### Token Validation

```javascript
function validateJWT(token) {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Check expiration
    if (decoded.exp < Math.floor(Date.now() / 1000)) {
      throw new Error('Token expired');
    }
    
    return decoded;
  } catch (error) {
    throw new Error('Invalid token');
  }
}
```

### Role-Based Access Control

```javascript
const PERMISSIONS = {
  'telemetry:read': ['viewer', 'operator', 'developer', 'admin'],
  'telemetry:write': ['operator', 'developer', 'admin'],
  'command:read': ['operator', 'developer', 'admin'],
  'command:write': ['operator', 'admin'],
  'task:read': ['viewer', 'developer', 'admin'],
  'task:write': ['developer', 'admin'],
  'security:admin': ['admin']
};

function hasPermission(userRole, requiredPermission) {
  const allowedRoles = PERMISSIONS[requiredPermission];
  return allowedRoles && allowedRoles.includes(userRole);
}

// Middleware
function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user || !hasPermission(req.user.role, permission)) {
      return res.status(403).json({
        error: 'Insufficient permissions'
      });
    }
    next();
  };
}

// Usage
app.post('/api/v1/commands',
  authenticate,
  requirePermission('command:write'),
  handleCommandExecution
);
```

---

## Secret Management

### Environment Variables

**Never commit secrets to version control**

#### .env.example (template only)
```bash
# API Configuration
NEXUS_API_KEY=<generate-with-openssl-rand>
JWT_SECRET=<generate-with-openssl-rand>
DATABASE_URL=<connection-string>
REDIS_URL=<connection-string>

# OAuth
GMAIL_CLIENT_ID=<from-google-cloud-console>
GMAIL_CLIENT_SECRET=<from-google-cloud-console>

# Encryption
ENCRYPTION_KEY=<generate-with-openssl-rand>
IV_LENGTH=16

# Webhooks
WEBHOOK_SECRET=<generate-with-openssl-rand>
```

#### Generate Secrets

```bash
# Generate API key
openssl rand -hex 32

# Generate JWT secret
openssl rand -base64 64

# Generate encryption key
openssl rand -hex 32

# Generate webhook secret
openssl rand -hex 24
```

### Secret Encryption at Rest

```javascript
const crypto = require('crypto');

class SecretManager {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
  }

  encrypt(text) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);
    
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      encrypted,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex')
    };
  }

  decrypt(encrypted, iv, authTag) {
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      this.key,
      Buffer.from(iv, 'hex')
    );
    
    decipher.setAuthTag(Buffer.from(authTag, 'hex'));
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
}

// Usage
const secretManager = new SecretManager();

// Encrypt before storing
const { encrypted, iv, authTag } = secretManager.encrypt('sensitive-data');
await db.secrets.insert({ encrypted, iv, authTag });

// Decrypt when needed
const decrypted = secretManager.decrypt(encrypted, iv, authTag);
```

### Secret Rotation

```javascript
async function rotateApiKey(userId) {
  // Generate new key
  const newApiKey = generateApiKey();
  const newKeyHash = hashApiKey(newApiKey);
  
  // Store new key
  await db.apiKeys.insert({
    user_id: userId,
    key_hash: newKeyHash,
    created_at: new Date(),
    active: true,
    scopes: ['telemetry:write', 'task:read']
  });
  
  // Mark old keys as deprecated (grace period)
  await db.apiKeys.updateMany(
    {
      user_id: userId,
      created_at: { $lt: new Date() }
    },
    {
      $set: {
        deprecated: true,
        expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
      }
    }
  );
  
  return newApiKey; // Return only once, never log
}
```

---

## Session Cleanup

### Expired Token Cleanup

```javascript
// Run daily
async function cleanupExpiredTokens() {
  const now = new Date();
  
  // Delete expired API keys
  const deletedKeys = await db.apiKeys.deleteMany({
    expires_at: { $lt: now }
  });
  
  // Delete expired JWT refresh tokens
  const deletedTokens = await db.refreshTokens.deleteMany({
    expires_at: { $lt: now }
  });
  
  console.log(`Cleaned up ${deletedKeys.deletedCount} API keys`);
  console.log(`Cleaned up ${deletedTokens.deletedCount} refresh tokens`);
  
  // Log cleanup
  await logSecurityEvent({
    type: 'token_cleanup',
    keys_deleted: deletedKeys.deletedCount,
    tokens_deleted: deletedTokens.deletedCount,
    timestamp: now
  });
}

// Schedule cleanup
const cron = require('node-cron');
cron.schedule('0 2 * * *', cleanupExpiredTokens); // 2 AM daily
```

### WebSocket Connection Cleanup

```javascript
// Clean up stale WebSocket connections
function cleanupStaleConnections() {
  const now = Date.now();
  const staleTimeout = 5 * 60 * 1000; // 5 minutes
  
  clients.forEach((client, clientId) => {
    const age = now - client.createdAt;
    const lastActivity = client.lastActivity || client.createdAt;
    const idleTime = now - lastActivity;
    
    if (idleTime > staleTimeout) {
      console.log(`Closing stale connection: ${clientId}`);
      client.ws.close(1000, 'Connection idle timeout');
      clients.delete(clientId);
    }
  });
}

// Run every minute
setInterval(cleanupStaleConnections, 60000);
```

### Database Session Cleanup

```javascript
async function cleanupDatabaseSessions() {
  // Clean up expired sessions
  await db.sessions.deleteMany({
    expires_at: { $lt: new Date() }
  });
  
  // Clean up orphaned data
  await db.tempData.deleteMany({
    created_at: { $lt: new Date(Date.now() - 24 * 60 * 60 * 1000) } // 1 day
  });
}
```

---

## Rate Limiting

### Implementation

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const redisClient = redis.createClient({
  url: process.env.REDIS_URL
});

// General API rate limiter
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:'
  }),
  windowMs: 60 * 1000, // 1 minute
  max: 1000, // 1000 requests per minute
  message: {
    error: 'Too many requests, please try again later',
    retryAfter: 60
  },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => {
    // Use API key or IP for rate limiting
    return req.user?.userId || req.ip;
  }
});

// Strict rate limiter for sensitive endpoints
const strictLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:strict:'
  }),
  windowMs: 60 * 1000,
  max: 10, // Only 10 requests per minute
  message: {
    error: 'Rate limit exceeded for this endpoint'
  }
});

// Apply rate limiting
app.use('/api/v1', apiLimiter);
app.use('/api/v1/security', strictLimiter);
```

### Custom Rate Limiting

```javascript
class CustomRateLimiter {
  constructor(redis) {
    this.redis = redis;
  }

  async checkLimit(key, limit, window) {
    const now = Date.now();
    const windowStart = now - window;
    
    // Remove old entries
    await this.redis.zremrangebyscore(key, 0, windowStart);
    
    // Count current requests
    const count = await this.redis.zcard(key);
    
    if (count >= limit) {
      const oldest = await this.redis.zrange(key, 0, 0, 'WITHSCORES');
      const resetTime = parseInt(oldest[1]) + window;
      
      return {
        allowed: false,
        remaining: 0,
        resetTime: resetTime
      };
    }
    
    // Add new request
    await this.redis.zadd(key, now, `${now}-${Math.random()}`);
    await this.redis.expire(key, Math.ceil(window / 1000));
    
    return {
      allowed: true,
      remaining: limit - count - 1,
      resetTime: now + window
    };
  }
}

// Usage
const limiter = new CustomRateLimiter(redisClient);

async function rateLimitMiddleware(req, res, next) {
  const key = `ratelimit:${req.user.userId}:${req.path}`;
  const result = await limiter.checkLimit(key, 100, 60000);
  
  res.set({
    'X-RateLimit-Limit': 100,
    'X-RateLimit-Remaining': result.remaining,
    'X-RateLimit-Reset': result.resetTime
  });
  
  if (!result.allowed) {
    return res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: Math.ceil((result.resetTime - Date.now()) / 1000)
    });
  }
  
  next();
}
```

---

## Input Validation

### Schema Validation

```javascript
const Joi = require('joi');

// Define schemas
const telemetrySchema = Joi.object({
  event_type: Joi.string().required().max(100),
  source: Joi.string().required().max(100),
  timestamp: Joi.date().iso().required(),
  data: Joi.object().required(),
  metadata: Joi.object()
});

const commandSchema = Joi.object({
  command_type: Joi.string().required().max(100),
  target: Joi.string().required().max(100),
  parameters: Joi.object(),
  priority: Joi.string().valid('low', 'normal', 'high', 'critical'),
  timeout_seconds: Joi.number().min(1).max(3600)
});

// Validation middleware
function validate(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });
    
    if (error) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.details.map(d => ({
          field: d.path.join('.'),
          message: d.message
        }))
      });
    }
    
    req.validatedBody = value;
    next();
  };
}

// Usage
app.post('/api/v1/telemetry/events',
  authenticate,
  validate(telemetrySchema),
  handleTelemetrySubmission
);
```

### SQL Injection Prevention

```javascript
// NEVER do this:
// const query = `SELECT * FROM users WHERE id = ${userId}`;

// ALWAYS use parameterized queries:
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);

// With PostgreSQL
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

async function getUser(userId) {
  const result = await pool.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
  );
  return result.rows[0];
}
```

### XSS Prevention

```javascript
const xss = require('xss');

function sanitizeInput(input) {
  if (typeof input === 'string') {
    return xss(input);
  }
  
  if (Array.isArray(input)) {
    return input.map(sanitizeInput);
  }
  
  if (typeof input === 'object' && input !== null) {
    const sanitized = {};
    for (const [key, value] of Object.entries(input)) {
      sanitized[key] = sanitizeInput(value);
    }
    return sanitized;
  }
  
  return input;
}

// Middleware
function sanitizeMiddleware(req, res, next) {
  if (req.body) {
    req.body = sanitizeInput(req.body);
  }
  if (req.query) {
    req.query = sanitizeInput(req.query);
  }
  next();
}
```

---

## Encryption

### HTTPS/TLS Configuration

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync(process.env.SSL_KEY_PATH),
  cert: fs.readFileSync(process.env.SSL_CERT_PATH),
  // Enforce strong ciphers
  ciphers: [
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES128-SHA256',
    'ECDHE-RSA-AES256-SHA384'
  ].join(':'),
  honorCipherOrder: true,
  minVersion: 'TLSv1.2'
};

https.createServer(options, app).listen(443);
```

### Data Encryption

```javascript
// Encrypt sensitive fields before storage
async function storeUserData(userData) {
  const encrypted = {
    ...userData,
    email: secretManager.encrypt(userData.email),
    phone: secretManager.encrypt(userData.phone),
    api_key: hashApiKey(userData.api_key) // Hash, don't encrypt
  };
  
  await db.users.insert(encrypted);
}
```

---

## Incident Response

### Security Incident Procedure

1. **Detection**: Monitor for security events
2. **Containment**: Isolate affected systems
3. **Investigation**: Determine scope and impact
4. **Remediation**: Fix vulnerabilities
5. **Recovery**: Restore normal operations
6. **Post-mortem**: Document and learn

### Incident Response Script

```javascript
async function handleSecurityIncident(incidentType, details) {
  // 1. Log incident
  await logSecurityEvent({
    type: 'security_incident',
    incident_type: incidentType,
    details: details,
    timestamp: new Date(),
    severity: 'critical'
  });
  
  // 2. Alert team
  await sendAlert({
    to: process.env.SECURITY_TEAM_EMAIL,
    subject: `SECURITY INCIDENT: ${incidentType}`,
    body: JSON.stringify(details, null, 2)
  });
  
  // 3. Take immediate action based on type
  switch (incidentType) {
    case 'api_key_compromise':
      await revokeCompromisedKey(details.keyId);
      break;
    
    case 'brute_force_attack':
      await blockIP(details.ip);
      break;
    
    case 'data_breach':
      await lockdownSystem();
      break;
  }
  
  // 4. Create incident ticket
  await createIncidentTicket(incidentType, details);
}
```

### Monitoring & Alerts

```javascript
// Monitor for suspicious activity
async function monitorSecurityEvents() {
  // Check for repeated failed auth attempts
  const failedAttempts = await db.securityEvents.count({
    type: 'invalid_api_key',
    timestamp: { $gt: new Date(Date.now() - 5 * 60 * 1000) }
  });
  
  if (failedAttempts > 100) {
    await handleSecurityIncident('brute_force_attack', {
      attempts: failedAttempts,
      timeWindow: '5 minutes'
    });
  }
  
  // Check for unusual data access patterns
  // Check for privilege escalation attempts
  // Check for data exfiltration patterns
}

// Run every minute
setInterval(monitorSecurityEvents, 60000);
```

---

## Compliance

### Audit Logging

```javascript
async function logAuditEvent(event) {
  await db.auditLog.insert({
    timestamp: new Date(),
    user_id: event.userId,
    action: event.action,
    resource_type: event.resourceType,
    resource_id: event.resourceId,
    ip_address: event.ip,
    user_agent: event.userAgent,
    status: event.status,
    details: event.details
  });
}

// Middleware for automatic audit logging
function auditMiddleware(req, res, next) {
  const originalSend = res.send;
  
  res.send = function(data) {
    logAuditEvent({
      userId: req.user?.userId,
      action: `${req.method} ${req.path}`,
      resourceType: req.path.split('/')[3], // e.g., 'tasks'
      resourceId: req.params.id,
      ip: req.ip,
      userAgent: req.headers['user-agent'],
      status: res.statusCode,
      details: { body: req.body, query: req.query }
    });
    
    originalSend.call(this, data);
  };
  
  next();
}
```

### GDPR Compliance

```javascript
// User data export
async function exportUserData(userId) {
  const userData = await db.users.findOne({ id: userId });
  const telemetry = await db.telemetry.find({ user_id: userId });
  const tasks = await db.tasks.find({ user_id: userId });
  
  return {
    user: userData,
    telemetry: telemetry,
    tasks: tasks,
    exported_at: new Date()
  };
}

// User data deletion
async function deleteUserData(userId) {
  // Anonymize or delete user data
  await db.users.deleteOne({ id: userId });
  await db.telemetry.deleteMany({ user_id: userId });
  await db.tasks.updateMany(
    { user_id: userId },
    { $set: { user_id: 'DELETED_USER' } }
  );
  
  await logAuditEvent({
    action: 'user_data_deletion',
    userId: userId,
    timestamp: new Date()
  });
}
```

---

## Security Monitoring

### Security Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  frameguard: { action: 'deny' },
  noSniff: true,
  xssFilter: true
}));
```

### Continuous Security Scanning

```bash
# Package vulnerability scanning
npm audit
npm audit fix

# Dependency scanning
npm install -g snyk
snyk test
snyk monitor

# Code scanning
npm install -g eslint-plugin-security
eslint --plugin security .
```

---

## Best Practices Summary

1. ✅ **Never store secrets in code**
2. ✅ **Always use HTTPS/TLS**
3. ✅ **Validate all inputs**
4. ✅ **Use parameterized queries**
5. ✅ **Implement rate limiting**
6. ✅ **Enable audit logging**
7. ✅ **Encrypt sensitive data**
8. ✅ **Rotate credentials regularly**
9. ✅ **Monitor for security events**
10. ✅ **Keep dependencies updated**

---

**Need Help?** Contact security@nexus.example.com for security-related questions.
