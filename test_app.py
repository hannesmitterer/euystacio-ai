"""
Test app import and blueprints
"""

import os
import sys

# Add the app directory to the path
app_dir = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'app')
sys.path.insert(0, app_dir)

# Add the root directory for other imports
root_dir = os.path.dirname(__file__)
sys.path.insert(0, root_dir)

# Import the Flask app
from app import app

def test_app():
    """
    Test the app and its blueprints
    """
    print("Testing app configuration...")
    print(f"App: {app}")
    print(f"Blueprints: {list(app.blueprints.keys())}")
    print("Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    print("\nTesting with app context:")
    with app.app_context():
        from flask import url_for
        try:
            print(f"docs_index: {url_for('docs.docs_index')}")
            print(f"get_doc: {url_for('docs.get_doc', slug='test')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    test_app()