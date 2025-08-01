# Euystacio Dashboard Deployment Guide

This document provides comprehensive instructions for testing public accessibility and managing deployments of the Euystacio Dashboard.

## 🌐 Live Deployments

### GitHub Pages
- **URL**: https://hannesmitterer.github.io/euystacio-ai/
- **Status**: ✅ Active
- **Auto-deploy**: Triggered on pushes to `main` branch

### Netlify
- **URL**: https://euystacio-ai.netlify.app/
- **Status**: ✅ Active (after netlify.toml fix)
- **Auto-deploy**: Triggered on pushes to `main` branch

## 🔧 Deployment Configuration

### GitHub Pages Setup
The dashboard is deployed using a custom GitHub Actions workflow (`.github/workflows/pages.yml`):

1. **Build Process**: Runs `python build_static.py` to generate static files
2. **Output Directory**: `static_build/`
3. **Triggers**: Push to main branch or manual dispatch
4. **Dependencies**: Python 3.12, Flask

### Netlify Setup
Configured via `netlify.toml`:

```toml
[build]
  publish = "static_build"
  command = "python build_static.py"

[build.environment]
  PYTHON_VERSION = "3.8"
```

**Fixed Issues**:
- ✅ Updated publish directory from "static" to "static_build" to match build output
- ✅ Removed conflicting Jekyll workflow that was overriding custom dashboard deployment

## 🧪 Testing Public Accessibility

### Automated Testing
Use the included test script to verify both deployments:

```bash
python test_deployment.py
```

This script tests:
- Main dashboard page accessibility
- Static assets (CSS, JS)
- API data endpoints (JSON files)
- Response codes and content types

### Manual Testing
1. **GitHub Pages**: Visit https://hannesmitterer.github.io/euystacio-ai/
2. **Netlify**: Visit https://euystacio-ai.netlify.app/
3. **Expected functionality**:
   - Dashboard loads with Euystacio branding
   - CSS styles applied correctly
   - Interactive pulse submission form
   - Red Code display
   - Responsive design on mobile

### Deployment Status Monitoring
- **GitHub Actions**: Check [Actions tab](https://github.com/hannesmitterer/euystacio-ai/actions) for workflow status
- **Netlify**: Monitor deployments at Netlify dashboard
- **Logs**: Review deployment logs for troubleshooting

## 🚀 Deployment Process

### Automatic Deployment
1. Push changes to `main` branch
2. Both GitHub Actions and Netlify workflows trigger automatically
3. Build process runs `python build_static.py`
4. Static files deployed to respective platforms
5. Sites updated within 2-3 minutes

### Manual Deployment
For GitHub Pages:
1. Go to [Actions tab](https://github.com/hannesmitterer/euystacio-ai/actions)
2. Select "Deploy Euystacio Dashboard to GitHub Pages"
3. Click "Run workflow"

For Netlify:
1. Use Netlify dashboard to trigger manual deploy
2. Or push to main branch to trigger auto-deploy

## 🔍 Troubleshooting

### Common Issues
1. **404 Errors**: Check if build output directory matches publish directory in config
2. **Missing Assets**: Ensure `static/` directory is properly copied during build
3. **Jekyll Override**: Remove any Jekyll workflows that might conflict with custom deployment

### Build Process
Local testing:
```bash
# Install dependencies
pip install -r requirements.txt

# Build static version
python build_static.py

# Test locally
cd static_build
python -m http.server 8000
```

### Resolved Conflicts
- ✅ **Netlify 404 Issue**: Fixed netlify.toml to use correct publish directory
- ✅ **Jekyll Conflict**: Removed jekyll-gh-pages.yml workflow that was overriding custom deployment
- ✅ **Main Branch Sync**: No merge conflicts found between branches

## 📋 Deployment Checklist

Before deploying:
- [ ] Test build process locally (`python build_static.py`)
- [ ] Verify static files generated in `static_build/`
- [ ] Test locally (`cd static_build && python -m http.server 8000`)
- [ ] Run deployment test script (`python test_deployment.py`)

After deploying:
- [ ] Verify GitHub Pages accessibility
- [ ] Verify Netlify accessibility  
- [ ] Test dashboard functionality on both platforms
- [ ] Check deployment logs for any errors

## 🛠️ Technical Details

### Build Script
The `build_static.py` script:
- Converts Flask templates to static HTML
- Copies static assets (CSS, JS)
- Generates JSON data files for API endpoints
- Creates demo-compatible version with localStorage

### File Structure
```
static_build/
├── index.html          # Main dashboard page
├── static/
│   ├── css/style.css   # Dashboard styles
│   └── js/app.js       # Dashboard JavaScript
└── data/
    ├── red_code.json   # Core Euystacio state
    ├── pulses.json     # Emotional pulses
    ├── tutors.json     # Tutor nominations
    └── reflections.json # System reflections
```

## 📞 Support

For deployment issues:
1. Check deployment logs in GitHub Actions
2. Run local build test to isolate issues
3. Use deployment test script for comprehensive verification
4. Review this documentation for common solutions