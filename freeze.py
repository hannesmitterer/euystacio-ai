"""
Freeze Flask application using Frozen-Flask to generate static files
for GitHub Pages deployment
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
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'static_build')
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
    
    from hygraph import list_local_markdown_docs, fetch_from_hygraph, DOCS_LIST_QUERY
    
    # Try to get docs from Hygraph first
    hygraph_data = fetch_from_hygraph(DOCS_LIST_QUERY)
    
    if hygraph_data and 'docs' in hygraph_data:
        docs = hygraph_data['docs']
    else:
        # Fallback to local docs
        docs = list_local_markdown_docs()
    
    # Generate URLs for the docs index and each document
    yield 'docs.docs_index'
    
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
    
    # Freeze the application
    freezer.freeze()
    
    print(f"Static site generated in: {app.config['FREEZER_DESTINATION']}")

if __name__ == '__main__':
    freeze_site()