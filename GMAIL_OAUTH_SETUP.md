# Gmail OAuth 2.0 Setup Guide

This guide walks you through setting up Gmail integration using OAuth 2.0 for the Nexus API.

## Table of Contents

1. [Overview](#overview)
2. [Google Cloud Console Setup](#google-cloud-console-setup)
3. [OAuth Scopes](#oauth-scopes)
4. [Environment Configuration](#environment-configuration)
5. [Implementation Example](#implementation-example)
6. [Testing OAuth Flow](#testing-oauth-flow)
7. [Token Management](#token-management)
8. [Troubleshooting](#troubleshooting)

---

## Overview

Gmail OAuth 2.0 integration allows Nexus to access Gmail on behalf of users with their explicit consent. This enables features like:

- Sending emails through user's Gmail account
- Reading emails for automation and AI processing
- Managing labels and filters
- Accessing calendar events
- Managing contacts

### OAuth 2.0 Flow

```mermaid
sequenceDiagram
    participant User
    participant App as Nexus App
    participant Google as Google OAuth
    participant Gmail as Gmail API

    User->>App: Initiate Gmail integration
    App->>Google: Redirect to consent screen
    User->>Google: Grant permissions
    Google->>App: Authorization code
    App->>Google: Exchange code for tokens
    Google->>App: Access token + Refresh token
    App->>Gmail: API request with access token
    Gmail->>App: Response
```

---

## Google Cloud Console Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **"Select a project"** → **"New Project"**
3. Enter project details:
   - **Project name**: `nexus-gmail-integration`
   - **Organization**: (optional)
4. Click **"Create"**

### Step 2: Enable Gmail API

1. In your project, navigate to **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click **"Gmail API"** → **"Enable"**

### Step 3: Configure OAuth Consent Screen

1. Navigate to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose user type:
   - **Internal**: Only for Google Workspace users within your organization
   - **External**: For all users (recommended)
3. Click **"Create"**

#### App Information

Fill in required fields:
- **App name**: `Nexus API`
- **User support email**: `support@yourdomain.com`
- **App logo**: (optional, 120x120 px)
- **Application home page**: `https://nexus.yourdomain.com`
- **Application privacy policy**: `https://nexus.yourdomain.com/privacy`
- **Application terms of service**: `https://nexus.yourdomain.com/terms`
- **Authorized domains**: `yourdomain.com`
- **Developer contact email**: `dev@yourdomain.com`

4. Click **"Save and Continue"**

#### Scopes

Add the following scopes (see [OAuth Scopes](#oauth-scopes) section):
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/userinfo.profile`

5. Click **"Save and Continue"**

#### Test Users (for External apps in testing)

If your app is in testing mode, add test user emails:
- `test@yourdomain.com`
- Add more as needed

6. Click **"Save and Continue"**

### Step 4: Create OAuth 2.0 Credentials

1. Navigate to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select application type: **"Web application"**
4. Configure:
   - **Name**: `Nexus Web Client`
   - **Authorized JavaScript origins**:
     ```
     https://nexus.yourdomain.com
     https://localhost:3000  (for development)
     ```
   - **Authorized redirect URIs**:
     ```
     https://nexus.yourdomain.com/oauth/gmail/callback
     https://localhost:3000/oauth/gmail/callback  (for development)
     ```
5. Click **"Create"**

### Step 5: Save Credentials

After creation, you'll see:
- **Client ID**: `xxxxx.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-xxxxx`

⚠️ **Important**: Copy these immediately and store securely. You'll need them for environment configuration.

---

## OAuth Scopes

### Recommended Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| `gmail.send` | Send emails | Automated email sending |
| `gmail.readonly` | Read emails | Email monitoring, AI processing |
| `gmail.modify` | Modify emails | Label management, archiving |
| `gmail.labels` | Manage labels | Organization, automation |
| `gmail.settings.basic` | View settings | Configuration checks |
| `userinfo.email` | Get user email | User identification |
| `userinfo.profile` | Get user profile | Display name, avatar |

### Full Scope URLs

```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.labels
https://www.googleapis.com/auth/gmail.settings.basic
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

### Minimal Setup (Send Only)

For basic email sending functionality:
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/userinfo.email
```

---

## Environment Configuration

### Required Environment Variables

Add these to your `.env` file or deployment platform:

```bash
# Gmail OAuth Configuration
GMAIL_CLIENT_ID=xxxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-xxxxx
GMAIL_REDIRECT_URI=https://nexus.yourdomain.com/oauth/gmail/callback

# OAuth Scopes (space-separated)
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/userinfo.email

# Token Storage (choose one)
# Option 1: Database
GMAIL_TOKEN_STORAGE=database
DATABASE_URL=postgresql://user:pass@host:5432/nexus

# Option 2: Redis
GMAIL_TOKEN_STORAGE=redis
REDIS_URL=redis://localhost:6379

# Option 3: File (development only)
GMAIL_TOKEN_STORAGE=file
GMAIL_TOKEN_FILE_PATH=/var/nexus/tokens/gmail_tokens.json
```

### Sample .env.example

```bash
# Gmail OAuth 2.0 Configuration
GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-your_client_secret
GMAIL_REDIRECT_URI=https://your-domain.com/oauth/gmail/callback
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/userinfo.email
GMAIL_TOKEN_STORAGE=database
```

---

## Implementation Example

### Node.js Implementation

```javascript
const { google } = require('googleapis');

class GmailOAuthClient {
  constructor() {
    this.oauth2Client = new google.auth.OAuth2(
      process.env.GMAIL_CLIENT_ID,
      process.env.GMAIL_CLIENT_SECRET,
      process.env.GMAIL_REDIRECT_URI
    );
  }

  // Generate authorization URL
  getAuthUrl() {
    const scopes = process.env.GMAIL_SCOPES.split(' ');
    
    return this.oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: scopes,
      prompt: 'consent' // Force consent screen to get refresh token
    });
  }

  // Exchange authorization code for tokens
  async getTokens(authCode) {
    const { tokens } = await this.oauth2Client.getToken(authCode);
    this.oauth2Client.setCredentials(tokens);
    
    // Store tokens securely
    await this.storeTokens(tokens);
    
    return tokens;
  }

  // Refresh access token
  async refreshAccessToken(refreshToken) {
    this.oauth2Client.setCredentials({
      refresh_token: refreshToken
    });
    
    const { credentials } = await this.oauth2Client.refreshAccessToken();
    await this.storeTokens(credentials);
    
    return credentials;
  }

  // Send email
  async sendEmail(to, subject, body) {
    const gmail = google.gmail({ version: 'v1', auth: this.oauth2Client });
    
    const message = [
      `To: ${to}`,
      'Content-Type: text/html; charset=utf-8',
      'MIME-Version: 1.0',
      `Subject: ${subject}`,
      '',
      body
    ].join('\n');

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    const res = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedMessage
      }
    });

    return res.data;
  }

  // Store tokens (implement based on your storage choice)
  async storeTokens(tokens) {
    // Database example
    if (process.env.GMAIL_TOKEN_STORAGE === 'database') {
      await db.query(
        'INSERT INTO oauth_tokens (provider, access_token, refresh_token, expires_at) VALUES ($1, $2, $3, $4)',
        ['gmail', tokens.access_token, tokens.refresh_token, new Date(tokens.expiry_date)]
      );
    }
    // Redis example
    else if (process.env.GMAIL_TOKEN_STORAGE === 'redis') {
      await redis.set('gmail:tokens', JSON.stringify(tokens));
    }
    // File example (dev only)
    else {
      fs.writeFileSync(
        process.env.GMAIL_TOKEN_FILE_PATH,
        JSON.stringify(tokens, null, 2)
      );
    }
  }
}

module.exports = GmailOAuthClient;
```

### Python Implementation

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import base64
from email.mime.text import MIMEText

class GmailOAuthClient:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": os.getenv("GMAIL_CLIENT_ID"),
                "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
                "redirect_uris": [os.getenv("GMAIL_REDIRECT_URI")],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        self.scopes = os.getenv("GMAIL_SCOPES").split()

    def get_auth_url(self):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=os.getenv("GMAIL_REDIRECT_URI")
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            prompt='consent'
        )
        
        return auth_url

    def get_tokens(self, auth_code):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=os.getenv("GMAIL_REDIRECT_URI")
        )
        
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        
        # Store tokens
        self.store_tokens(credentials)
        
        return credentials

    def send_email(self, credentials, to, subject, body):
        service = build('gmail', 'v1', credentials=credentials)
        
        message = MIMEText(body, 'html')
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode('utf-8')
        
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return result

    def store_tokens(self, credentials):
        # Implement based on your storage choice
        pass
```

---

## Testing OAuth Flow

### Step 1: Start Your Application

```bash
npm start
# or
python app.py
```

### Step 2: Initiate OAuth Flow

Navigate to:
```
https://localhost:3000/oauth/gmail/start
```

### Step 3: Grant Permissions

1. You'll be redirected to Google's consent screen
2. Sign in with Google account
3. Review requested permissions
4. Click **"Allow"**

### Step 4: Handle Callback

Your application will receive the authorization code at the callback URL:
```
https://localhost:3000/oauth/gmail/callback?code=xxxxx
```

### Step 5: Verify Token Storage

Check that tokens are stored correctly:

```javascript
// In your callback handler
app.get('/oauth/gmail/callback', async (req, res) => {
  const { code } = req.query;
  
  try {
    const gmailClient = new GmailOAuthClient();
    const tokens = await gmailClient.getTokens(code);
    
    console.log('Tokens received:', {
      access_token: tokens.access_token ? 'present' : 'missing',
      refresh_token: tokens.refresh_token ? 'present' : 'missing',
      expiry_date: new Date(tokens.expiry_date)
    });
    
    res.send('Gmail integration successful!');
  } catch (error) {
    console.error('OAuth error:', error);
    res.status(500).send('OAuth failed');
  }
});
```

---

## Token Management

### Token Refresh Strategy

Access tokens expire after 1 hour. Implement automatic refresh:

```javascript
async function ensureValidToken(userId) {
  const tokens = await getStoredTokens(userId);
  
  // Check if token is expired or will expire in next 5 minutes
  const expiryDate = new Date(tokens.expiry_date);
  const now = new Date();
  const fiveMinutesFromNow = new Date(now.getTime() + 5 * 60000);
  
  if (expiryDate < fiveMinutesFromNow) {
    // Refresh token
    const gmailClient = new GmailOAuthClient();
    const newTokens = await gmailClient.refreshAccessToken(tokens.refresh_token);
    return newTokens;
  }
  
  return tokens;
}
```

### Token Revocation

Allow users to revoke access:

```javascript
async function revokeGmailAccess(userId) {
  const tokens = await getStoredTokens(userId);
  
  // Revoke token with Google
  await fetch('https://oauth2.googleapis.com/revoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `token=${tokens.access_token}`
  });
  
  // Delete from storage
  await deleteStoredTokens(userId);
}
```

---

## Troubleshooting

### Common Issues

#### 1. "Redirect URI mismatch" Error

**Problem**: OAuth flow fails with redirect URI mismatch

**Solution**:
- Ensure redirect URI in code exactly matches Google Cloud Console
- Check for trailing slashes
- Verify protocol (http vs https)
- Ensure redirect URI is added to authorized list

#### 2. "Access blocked: This app's request is invalid"

**Problem**: OAuth consent screen shows error

**Solution**:
- Verify OAuth consent screen is configured
- Check that all required fields are filled
- Ensure scopes are properly configured
- For external apps, verify domain ownership

#### 3. No Refresh Token Received

**Problem**: Only access token received, no refresh token

**Solution**:
- Add `access_type: 'offline'` to auth URL generation
- Add `prompt: 'consent'` to force consent screen
- If user already granted access, revoke and re-authorize

#### 4. Token Expired Errors

**Problem**: API calls fail with "Token has been expired or revoked"

**Solution**:
- Implement automatic token refresh
- Check token expiry before API calls
- Store and use refresh token properly

#### 5. Insufficient Permissions

**Problem**: API calls fail with permission errors

**Solution**:
- Verify requested scopes in OAuth flow
- Check if required scopes are enabled in Google Cloud Console
- Re-authorize with correct scopes

### Debug Mode

Enable debug logging:

```javascript
// Node.js
const { google } = require('googleapis');
google.options({ debug: true });

// Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Security Best Practices

1. **Never commit credentials**: Use environment variables
2. **Encrypt tokens**: Encrypt tokens at rest in database
3. **Use HTTPS**: Always use HTTPS in production
4. **Validate state parameter**: Prevent CSRF attacks
5. **Limit scopes**: Request only necessary scopes
6. **Regular audits**: Review authorized applications regularly
7. **Token rotation**: Implement token refresh and rotation
8. **Secure storage**: Use secure storage solutions (not files in production)

---

## Next Steps

After successful Gmail OAuth setup:

1. ✅ Test email sending functionality
2. ✅ Implement token refresh mechanism
3. ✅ Add user interface for OAuth consent
4. ✅ Set up token encryption
5. ✅ Implement error handling and retries
6. ✅ Add logging and monitoring
7. ✅ Review [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md)

---

**Need Help?** Contact support@nexus.example.com or check Google's [OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2).
