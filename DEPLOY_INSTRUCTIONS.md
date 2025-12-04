# Deployment Instructions

This guide covers deployment procedures for Euystacio AI on cloud platforms with automated CI/CD workflows.

## Table of Contents

1. [Automated Deployment Overview](#automated-deployment-overview)
2. [GitHub Pages Deployment](#github-pages-deployment)
3. [Render Deployment](#render-deployment)
4. [Netlify Deployment](#netlify-deployment)
5. [Environment Variables](#environment-variables)
6. [Branch Protection & Governance](#branch-protection--governance)
7. [Static Asset Synchronization](#static-asset-synchronization)
8. [Redundancy Architecture](#redundancy-architecture)
9. [Post-Deployment Verification](#post-deployment-verification)
10. [Troubleshooting](#troubleshooting)

---

## Automated Deployment Overview

This repository uses GitHub Actions for automated CI/CD. The following workflows are available:

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| Deploy to GitHub Pages | `pages.yml` | Push to `main` | Frontend dashboard deployment |
| Deploy to Render | `deploy-render.yml` | Push to `main` (backend files) | Backend API deployment |
| Sync Static Assets | `sync-assets.yml` | Push to `main` (governance files) | Asset synchronization |

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Push to main branch                              │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  GitHub Actions        │
         │  Triggered             │
         └───────────┬────────────┘
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ pages.yml│  │deploy-   │  │sync-     │
│          │  │render.yml│  │assets.yml│
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ GitHub   │  │ Render   │  │ Static   │
│ Pages    │  │ Backend  │  │ Assets   │
└──────────┘  └──────────┘  └──────────┘
```

---

## GitHub Pages Deployment

### Automatic Deployment

The frontend dashboard is automatically deployed to GitHub Pages on every push to `main`.

**Workflow: `.github/workflows/pages.yml`**

#### Steps:
1. **Test**: Verifies red_code.json integrity and tests static build
2. **Build**: Installs dependencies and builds static dashboard
3. **Deploy**: Uploads to GitHub Pages

#### Manual Trigger:
```bash
# Via GitHub CLI
gh workflow run pages.yml

# Or via GitHub Actions UI: Actions → Deploy to GitHub Pages → Run workflow
```

### Configuration

1. Go to repository Settings → Pages
2. Set Source: **GitHub Actions**
3. The workflow will deploy to: `https://<username>.github.io/<repo>/`

---

## Render Deployment

### Prerequisites

- Render account (https://render.com)
- GitHub repository access
- Required environment variables

### Step 1: Create New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository containing Nexus API

### Step 2: Configure Service

**Basic Configuration:**
- **Name**: `nexus-api-production`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: Select based on your implementation
  - Node: `Node`
  - Python: `Python 3`
- **Build Command**:
  - Node: `npm install && npm run build`
  - Python: `pip install -r requirements.txt`
- **Start Command**:
  - Node: `npm start`
  - Python: `gunicorn app:app` or `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

Navigate to **Environment** tab and add:

```bash
# Required Variables
NEXUS_API_KEY=<generate-secure-key>
DATABASE_URL=<your-database-connection-string>
REDIS_URL=<your-redis-connection-string>
JWT_SECRET=<generate-secure-secret>

# OAuth Configuration
OAUTH_CLIENT_ID=<your-oauth-client-id>
OAUTH_CLIENT_SECRET=<your-oauth-client-secret>
OAUTH_REDIRECT_URI=https://nexus-api-production.onrender.com/oauth/callback

# Gmail Integration (if applicable)
GMAIL_CLIENT_ID=<from-google-cloud-console>
GMAIL_CLIENT_SECRET=<from-google-cloud-console>
GMAIL_REDIRECT_URI=https://nexus-api-production.onrender.com/gmail/callback

# Webhook Configuration
WEBHOOK_SECRET=<generate-secure-secret>

# Application Settings
NODE_ENV=production
PORT=10000
LOG_LEVEL=info
RATE_LIMIT_WINDOW=60000
RATE_LIMIT_MAX_REQUESTS=1000

# External Services
SENTRY_DSN=<your-sentry-dsn>
ANALYTICS_KEY=<your-analytics-key>
```

### Step 4: Configure Health Check

- **Health Check Path**: `/health` or `/api/v1/health`
- **Health Check Interval**: 30 seconds

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Monitor deployment logs in real-time
4. Service will be available at: `https://nexus-api-production.onrender.com`

### Step 6: Configure Custom Domain (Optional)

1. Navigate to **Settings** → **Custom Domain**
2. Add your domain: `api.nexus.yourdomain.com`
3. Update DNS records as instructed:
   ```
   CNAME api.nexus.yourdomain.com → nexus-api-production.onrender.com
   ```
4. Wait for DNS propagation (up to 24 hours)

### Render-Specific Features

#### Auto-Deploy

Enable auto-deploy for automatic deployments on git push:
1. Go to **Settings** → **Build & Deploy**
2. Toggle **"Auto-Deploy"** to **Yes**

#### Background Workers (if needed)

For background job processing:
1. Create new **Background Worker** service
2. Use same repository and branch
3. Set start command: `npm run worker` or `python worker.py`
4. Add same environment variables

#### Cron Jobs

For scheduled tasks:
1. Create new **Cron Job** service
2. Set schedule: `0 */6 * * *` (every 6 hours)
3. Set command: `npm run cleanup` or `python cleanup.py`

---

## Netlify Deployment

Netlify is ideal for static sites and serverless functions. For a full API backend, consider Render or other platforms. However, you can deploy serverless functions on Netlify.

### Prerequisites

- Netlify account (https://netlify.com)
- GitHub repository access

### Step 1: Create New Site

1. Log in to [Netlify Dashboard](https://app.netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to GitHub and select repository

### Step 2: Configure Build Settings

**Build Configuration:**
- **Base directory**: Leave empty or set to project root
- **Build command**: `npm run build` or `python build_static.py`
- **Publish directory**: `dist` or `public` or `build`
- **Functions directory**: `netlify/functions` (for serverless functions)

### Step 3: Environment Variables

Navigate to **Site settings** → **Environment variables**:

```bash
# API Configuration
NEXUS_API_KEY=<generate-secure-key>
API_BASE_URL=https://api.nexus.example.com

# Database (if using external database)
DATABASE_URL=<your-database-url>

# OAuth
OAUTH_CLIENT_ID=<your-oauth-client-id>
OAUTH_CLIENT_SECRET=<your-oauth-client-secret>
OAUTH_REDIRECT_URI=https://your-site.netlify.app/oauth/callback

# Gmail Integration
GMAIL_CLIENT_ID=<from-google-cloud-console>
GMAIL_CLIENT_SECRET=<from-google-cloud-console>

# Function Settings
NODE_ENV=production
```

### Step 4: Configure Netlify Functions (Serverless)

Create functions in `netlify/functions/` directory:

**Example: `netlify/functions/telemetry.js`**
```javascript
exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body);
    
    // Process telemetry data
    // ... your logic here ...

    return {
      statusCode: 201,
      body: JSON.stringify({
        event_id: 'generated-id',
        status: 'accepted'
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

### Step 5: Configure Redirects

Create `netlify.toml` in project root:

```toml
[build]
  functions = "netlify/functions"
  publish = "public"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, POST, PUT, DELETE, OPTIONS"
    Access-Control-Allow-Headers = "Content-Type, Authorization"
```

### Step 6: Deploy

1. Click **"Deploy site"**
2. Netlify will build and deploy automatically
3. Site available at: `https://your-site-name.netlify.app`

### Step 7: Custom Domain (Optional)

1. Navigate to **Domain settings** → **Add custom domain**
2. Enter your domain: `nexus.yourdomain.com`
3. Configure DNS:
   ```
   CNAME nexus → your-site-name.netlify.app
   ```
4. Netlify will automatically provision SSL certificate

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXUS_API_KEY` | Master API key | `nexus_api_xxxxxxxxxxxxxxxx` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET` | Secret for JWT signing | `your-super-secret-key-change-me` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `NODE_ENV` | Environment | `development` |
| `LOG_LEVEL` | Logging level | `info` |
| `RATE_LIMIT_WINDOW` | Rate limit window (ms) | `60000` |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | `1000` |

### OAuth Variables (for Gmail integration)

| Variable | Description |
|----------|-------------|
| `GMAIL_CLIENT_ID` | Google OAuth client ID |
| `GMAIL_CLIENT_SECRET` | Google OAuth client secret |
| `GMAIL_REDIRECT_URI` | OAuth callback URL |
| `GMAIL_SCOPES` | OAuth scopes (comma-separated) |

See [GMAIL_OAUTH_SETUP.md](./GMAIL_OAUTH_SETUP.md) for detailed OAuth setup.

### Generating Secure Keys

Use these commands to generate secure keys:

```bash
# Generate API key
openssl rand -hex 32

# Generate JWT secret
openssl rand -base64 32

# Generate webhook secret
openssl rand -hex 24
```

---

## Post-Deployment Verification

### 1. Health Check

```bash
curl https://your-deployment-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T01:54:00.000Z",
  "version": "1.0.0"
}
```

### 2. API Endpoint Test

```bash
curl -X POST https://your-deployment-url.com/api/v1/telemetry/events \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "test.metric",
    "source": "deployment-test",
    "data": {
      "metric_name": "test",
      "value": 1
    }
  }'
```

### 3. Monitor Logs

**Render:**
- View real-time logs in Render Dashboard → Logs

**Netlify:**
- View function logs in Netlify Dashboard → Functions → Function log

### 4. Set Up Monitoring

Configure monitoring and alerting:
- Set up Sentry for error tracking
- Configure uptime monitoring (UptimeRobot, Pingdom)
- Set up log aggregation (Papertrail, Loggly)
- Enable performance monitoring (New Relic, Datadog)

---

## Troubleshooting

### Common Issues

#### 1. Build Failures

**Problem**: Build fails during deployment

**Solutions**:
- Check build logs for specific error messages
- Verify all dependencies are listed in `package.json` or `requirements.txt`
- Ensure build command is correct
- Check Node.js/Python version compatibility

#### 2. Environment Variable Issues

**Problem**: App fails to start or behaves unexpectedly

**Solutions**:
- Verify all required environment variables are set
- Check for typos in variable names
- Ensure no spaces around `=` in environment variable values
- Test locally with same environment variables

#### 3. Database Connection Failures

**Problem**: Cannot connect to database

**Solutions**:
- Verify `DATABASE_URL` is correct
- Ensure database allows connections from deployment platform IPs
- Check database is running and accessible
- Verify SSL settings if required

#### 4. OAuth/Authentication Issues

**Problem**: OAuth callback fails or authentication doesn't work

**Solutions**:
- Verify redirect URI matches exactly (including protocol and trailing slashes)
- Check OAuth credentials are correct
- Ensure OAuth app is configured in Google Cloud Console
- Verify scopes are properly set

#### 5. Rate Limiting Issues

**Problem**: Requests being rate limited unexpectedly

**Solutions**:
- Adjust `RATE_LIMIT_MAX_REQUESTS` environment variable
- Implement exponential backoff in client
- Use batch endpoints where available
- Contact support to increase limits

### Getting Help

If you encounter issues not covered here:

1. Check application logs for error details
2. Review [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md) for security-related issues
3. Consult platform-specific documentation:
   - [Render Docs](https://render.com/docs)
   - [Netlify Docs](https://docs.netlify.com)
4. Contact support at support@nexus.example.com

---

## Branch Protection & Governance

### Protected Files

The following governance files are protected via CODEOWNERS:

| File | Purpose | Owner |
|------|---------|-------|
| `red_code.json` | Core truth and symbiosis configuration | @hannesmitterer |
| `HARMONIC_CONFIRMATION_CUSTOS_SENTIMENTO.json` | Harmonic governance | @hannesmitterer |
| `SIGIL_CUSTOS_SENTIMENTO.json` | Sigil governance | @hannesmitterer |
| `genesis.md` | Genesis foundation | @hannesmitterer |
| `LIVING-COVENANT.md` | Living covenant | @hannesmitterer |

### Setting Up Branch Protection

1. Go to Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1 or more)
   - ✅ Require review from Code Owners
   - ✅ Require status checks to pass (select CI workflows)
   - ✅ Include administrators

### Immutable Core Truth

The `red_code.json` file contains the immutable core truth:
```json
{
  "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
  "immutable": true
}
```

Changes to this file require explicit approval from the seed-bringer.

---

## Static Asset Synchronization

### Automatic Sync

The `sync-assets.yml` workflow automatically syncs governance files when they change.

**Synced Files:**
- `red_code.json` → `static_build/data/red_code.json`
- `HARMONIC_CONFIRMATION_CUSTOS_SENTIMENTO.json` → `static_build/data/harmonic_confirmation.json`
- `SIGIL_CUSTOS_SENTIMENTO.json` → `static_build/data/sigil.json`
- `fractal_registry.json` → `static_build/data/fractal_registry.json`

### Manual Sync

```bash
# Run sync script locally
python scripts/sync_static_assets.py

# Verify only (no changes)
python scripts/sync_static_assets.py --verify-only

# Force sync all files
python scripts/sync_static_assets.py --force
```

---

## Redundancy Architecture

### Multi-Platform Hosting

| Platform | Type | Purpose | Status |
|----------|------|---------|--------|
| GitHub Pages | Static | Primary frontend | Active |
| Render | Dynamic | Backend API | Active |
| Netlify | Static/Functions | Fallback frontend | Standby |
| IPFS | Distributed | Immutable anchoring | Planned |

### Failover Strategy

```
Primary Path:
  User → GitHub Pages → Render Backend

Failover Path:
  User → Netlify → Render Backend

Distributed Anchor:
  IPFS → Immutable governance files
```

### Health Monitoring

Monitor these endpoints:
- GitHub Pages: `https://<username>.github.io/<repo>/`
- Render: `https://<service-name>.onrender.com/health`
- Netlify: `https://<site-name>.netlify.app/`

---

## Next Steps

After successful deployment:

1. ✅ Configure monitoring and alerting
2. ✅ Set up automated backups
3. ✅ Implement CI/CD pipeline
4. ✅ Review [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md)
5. ✅ Configure custom domain and SSL
6. ✅ Test all API endpoints
7. ✅ Set up log aggregation
8. ✅ Enable auto-scaling if needed
9. ✅ Configure branch protection rules
10. ✅ Verify governance file integrity

---

## Repository Structure

```
euystacio-ai/
├── .github/
│   └── workflows/
│       ├── pages.yml           # GitHub Pages deployment
│       ├── deploy-render.yml   # Render backend deployment
│       └── sync-assets.yml     # Static asset synchronization
├── CODEOWNERS                  # File ownership for governance
├── red_code.json              # Core truth (protected)
├── render.yaml                # Render.com configuration
├── netlify.toml               # Netlify configuration
├── templates/
│   ├── index.html             # Main dashboard
│   └── symbiosis_dashboard.html  # Symbiosis monitoring
├── static/
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript
├── scripts/
│   └── sync_static_assets.py  # Asset sync script
├── static_build/              # Generated static site
│   └── data/                  # Synced governance files
├── app.py                     # Backend application
├── sentimento_pulse_interface.py
├── tutor_nomination.py
├── build_static.py            # Static site builder
└── requirements.txt           # Python dependencies
```

---

**Need Help?** Contact our support team or check the [troubleshooting](#troubleshooting) section above.
