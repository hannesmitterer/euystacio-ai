"""
Debug app import with prints
"""

import os
import sys

# Add the app directory to the path
app_dir = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'app')
sys.path.insert(0, app_dir)

# Add the root directory for other imports  
root_dir = os.path.dirname(__file__)
sys.path.insert(0, root_dir)

print("Starting app import...")

try:
    from app import app
    print(f"App imported: {app}")
    print(f"Blueprints: {list(app.blueprints.keys())}")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
    
    # Try importing manually
    print("\nTrying manual import...")
    
    # First import all the dependencies
    try:
        from flask import Flask
        print("Flask imported")
        
        # Test importing hygraph directly
        services_path = os.path.join(app_dir, '..', 'services')
        services_path = os.path.abspath(services_path)
        print(f"Services path: {services_path}")
        print(f"Services path exists: {os.path.exists(services_path)}")
        
        if os.path.exists(services_path):
            sys.path.insert(0, services_path)
            from hygraph import docs_bp
            print(f"Blueprint imported: {docs_bp}")
        
    except Exception as e2:
        print(f"Error in manual import: {e2}")
        import traceback
        traceback.print_exc()