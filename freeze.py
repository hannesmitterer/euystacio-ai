"""
Freeze Flask application using Frozen-Flask to generate static files
for GitHub Pages deployment
"""

import os
import sys
from flask_frozen import Freezer

# Add the services path
services_path = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'services')
sys.path.insert(0, services_path)

# Import the docs blueprint
from hygraph import docs_bp

# Import the main app
from app import app

# Register the docs blueprint with the main app
app.register_blueprint(docs_bp)

# Create the Freezer
freezer = Freezer(app)

# Configuration
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'static_build')
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True

@freezer.register_generator
def docs_generator():
    """
    Generate URLs for all documentation pages
    """
    from hygraph import list_local_markdown_docs, fetch_from_hygraph, DOCS_LIST_QUERY
    
    # Try to get docs from Hygraph first
    hygraph_data = fetch_from_hygraph(DOCS_LIST_QUERY)
    
    if hygraph_data and 'docs' in hygraph_data:
        docs = hygraph_data['docs']
    else:
        # Fallback to local docs
        docs = list_local_markdown_docs()
    
    # Generate URLs for each document
    for doc in docs:
        yield 'docs.get_doc', {'slug': doc['slug']}
        yield 'docs.get_doc_json', {'slug': doc['slug']}

def freeze_site():
    """
    Freeze the Flask application to static files
    """
    print("Freezing Flask application to static files...")
    
    # Ensure the destination directory exists
    os.makedirs(app.config['FREEZER_DESTINATION'], exist_ok=True)
    
    # Check that docs blueprint is registered
    print(f"Registered blueprints: {list(app.blueprints.keys())}")
    
    try:
        # Freeze the application
        frozen_urls = freezer.freeze()
        
        docs_urls = [url for url in frozen_urls if '/docs' in url]
        print(f"Generated {len(frozen_urls)} static files")
        print(f"Documentation pages: {len(docs_urls)}")
        
        print(f"Static site generated in: {app.config['FREEZER_DESTINATION']}")
        
    except Exception as e:
        print(f"Warning: Some pages failed to freeze: {e}")
        print("Attempting to freeze core pages only...")
        
        # Fallback: try to freeze manually with error handling
        with app.test_client() as client:
            # Create core directories
            docs_dir = os.path.join(app.config['FREEZER_DESTINATION'], 'docs')
            os.makedirs(docs_dir, exist_ok=True)
            
            # Generate docs index manually
            try:
                rv = client.get('/docs/')
                if rv.status_code == 200:
                    with open(os.path.join(docs_dir, 'index.html'), 'w') as f:
                        f.write(rv.data.decode())
                    print("✓ Docs index generated")
            except Exception as e2:
                print(f"✗ Failed to generate docs index: {e2}")

if __name__ == '__main__':
    freeze_site()