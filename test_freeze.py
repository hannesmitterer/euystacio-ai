"""
Simple test of freeze functionality
"""

import os
import sys
from flask_frozen import Freezer

# Add the app directory to the path
app_dir = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'app')
sys.path.insert(0, app_dir)

# Add the root directory for other imports
root_dir = os.path.dirname(__file__)
sys.path.insert(0, root_dir)

# Import the Flask app
from app import app

# Create the Freezer
freezer = Freezer(app)

# Configuration
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'test_static_build')
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True

def test_freeze():
    """
    Test freeze functionality
    """
    print("Testing freeze functionality...")
    
    # Ensure the destination directory exists
    os.makedirs(app.config['FREEZER_DESTINATION'], exist_ok=True)
    
    # Just freeze basic routes first
    try:
        urls = list(freezer.all_urls())
        print(f"Found {len(urls)} URLs to freeze:")
        for url in urls[:10]:  # Show first 10
            print(f"  {url}")
        if len(urls) > 10:
            print(f"  ... and {len(urls) - 10} more")
        
        # Freeze only the index page for testing
        with app.test_client() as client:
            print("Testing index page...")
            rv = client.get('/')
            print(f"Index status: {rv.status_code}")
            
            print("Testing docs index...")
            rv = client.get('/docs/')
            print(f"Docs index status: {rv.status_code}")
    
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_freeze()