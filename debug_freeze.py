"""
Debug freeze URLs
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
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'debug_static_build')
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True

@freezer.register_generator
def docs_generator():
    """
    Generate URLs for all documentation pages
    """
    # Import here to avoid circular imports
    services_path = os.path.join(os.path.dirname(__file__), 'woodstone_festival_2025_fullpack_cms_ai', 'services')
    sys.path.insert(0, services_path)
    
    from hygraph import list_local_markdown_docs
    
    docs = list_local_markdown_docs()
    print(f"Found {len(docs)} docs: {[doc['slug'] for doc in docs]}")
    
    # Generate URLs for the docs index and each document
    yield 'docs.docs_index'
    
    for doc in docs:
        yield 'docs.get_doc', {'slug': doc['slug']}
        yield 'docs.get_doc_json', {'slug': doc['slug']}

def debug_urls():
    """
    Debug URL generation
    """
    print("Debugging URL generation...")
    
    try:
        urls = list(freezer.all_urls())
        print(f"Generated {len(urls)} URLs:")
        for url in urls:
            print(f"  {url}")
        
        # Test URL generation for docs specifically
        print("\nTesting docs URL generation:")
        with app.test_request_context():
            from flask import url_for
            print(f"docs_index: {url_for('docs.docs_index')}")
            print(f"get_doc: {url_for('docs.get_doc', slug='getting-started')}")
            print(f"get_doc_json: {url_for('docs.get_doc_json', slug='getting-started')}")
            
    except Exception as e:
        print(f"Error during URL generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_urls()