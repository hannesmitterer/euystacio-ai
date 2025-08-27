"""
Test blueprint import specifically
"""

import os
import sys

# Add the app directory to the path
app_dir = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'app')
sys.path.insert(0, app_dir)

# Add the root directory for other imports
root_dir = os.path.dirname(__file__)
sys.path.insert(0, root_dir)

# Test import step by step
print("Testing imports...")

try:
    print("1. Importing Flask...")
    from flask import Flask
    print("   Flask imported successfully")
    
    print("2. Creating test app...")
    test_app = Flask(__name__)
    print("   Test app created successfully")
    
    print("3. Testing blueprint import...")
    services_path = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'services')
    sys.path.insert(0, services_path)
    
    from hygraph import docs_bp
    print("   Blueprint imported successfully")
    print(f"   Blueprint: {docs_bp}")
    print(f"   Blueprint name: {docs_bp.name}")
    
    print("4. Registering blueprint...")
    test_app.register_blueprint(docs_bp)
    print("   Blueprint registered successfully")
    print(f"   Blueprints: {list(test_app.blueprints.keys())}")
    
    print("5. Testing routes...")
    for rule in test_app.url_map.iter_rules():
        if 'docs' in rule.rule:
            print(f"   {rule.rule} -> {rule.endpoint}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n6. Now testing full app import...")
try:
    from app import app as full_app
    print(f"   Full app blueprints: {list(full_app.blueprints.keys())}")
    docs_routes = [rule for rule in full_app.url_map.iter_rules() if 'docs' in rule.rule]
    print(f"   Docs routes: {len(docs_routes)}")
    for rule in docs_routes:
        print(f"     {rule.rule} -> {rule.endpoint}")
        
except Exception as e:
    print(f"Error importing full app: {e}")
    import traceback
    traceback.print_exc()