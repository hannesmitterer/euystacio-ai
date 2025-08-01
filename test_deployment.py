#!/usr/bin/env python3
"""
Deployment Testing Script for Euystacio Dashboard
Tests public accessibility of both GitHub Pages and Netlify deployments
"""

import requests
import time
import sys
from urllib.parse import urljoin

def test_url_accessibility(url, expected_status=200, timeout=10):
    """Test if a URL is accessible and returns expected status"""
    try:
        print(f"Testing {url}...")
        response = requests.get(url, timeout=timeout)
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"  Content-Length: {len(response.content)} bytes")
        
        if response.status_code == expected_status:
            print(f"  ✅ SUCCESS: {url} is accessible")
            return True
        else:
            print(f"  ❌ FAILED: Expected {expected_status}, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def test_dashboard_endpoints(base_url):
    """Test that essential dashboard endpoints/files are accessible"""
    endpoints = [
        "",  # Main page
        "static/css/style.css",
        "static/js/app.js", 
        "data/red_code.json",
        "data/pulses.json"
    ]
    
    results = []
    for endpoint in endpoints:
        url = urljoin(base_url, endpoint)
        success = test_url_accessibility(url)
        results.append((endpoint, success))
    
    return results

def main():
    """Main testing function"""
    print("🧪 Euystacio Dashboard Deployment Test")
    print("=" * 50)
    
    # Test URLs
    github_pages_url = "https://hannesmitterer.github.io/euystacio-ai/"
    netlify_url = "https://euystacio-ai.netlify.app/"
    
    all_tests_passed = True
    
    # Test GitHub Pages
    print("\n📄 Testing GitHub Pages Deployment")
    print("-" * 30)
    github_results = test_dashboard_endpoints(github_pages_url)
    github_success = all(result[1] for result in github_results)
    
    if github_success:
        print("✅ GitHub Pages deployment is fully functional")
    else:
        print("❌ GitHub Pages deployment has issues")
        all_tests_passed = False
    
    # Test Netlify
    print("\n🌐 Testing Netlify Deployment")
    print("-" * 30)
    netlify_results = test_dashboard_endpoints(netlify_url)
    netlify_success = all(result[1] for result in netlify_results)
    
    if netlify_success:
        print("✅ Netlify deployment is fully functional")
    else:
        print("❌ Netlify deployment has issues")
        all_tests_passed = False
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"GitHub Pages: {'✅ PASS' if github_success else '❌ FAIL'}")
    print(f"Netlify:      {'✅ PASS' if netlify_success else '❌ FAIL'}")
    
    if all_tests_passed:
        print("\n🎉 All deployments are working correctly!")
        return 0
    else:
        print("\n⚠️  Some deployments need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())