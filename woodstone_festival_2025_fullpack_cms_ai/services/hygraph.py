"""
Hygraph integration service for docs management
Provides GraphQL API integration with local markdown fallback
"""

from flask import Blueprint, render_template_string, request, jsonify, abort
import requests
import json
import os
from typing import Dict, Any, Optional

# Create the docs blueprint
docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

# Hygraph configuration - these would come from environment variables
HYGRAPH_ENDPOINT = os.environ.get('HYGRAPH_ENDPOINT', '')
HYGRAPH_TOKEN = os.environ.get('HYGRAPH_TOKEN', '')

# GraphQL query for fetching docs
DOCS_QUERY = """
query GetDoc($slug: String!) {
  doc(where: {slug: $slug}) {
    id
    title
    slug
    content
    createdAt
    updatedAt
  }
}
"""

DOCS_LIST_QUERY = """
query GetDocs {
  docs {
    id
    title
    slug
    createdAt
    updatedAt
  }
}
"""

def fetch_from_hygraph(query: str, variables: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from Hygraph GraphQL API
    """
    if not HYGRAPH_ENDPOINT or not HYGRAPH_TOKEN:
        return None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {HYGRAPH_TOKEN}'
    }
    
    payload = {
        'query': query,
        'variables': variables or {}
    }
    
    try:
        response = requests.post(
            HYGRAPH_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        if 'errors' in data:
            print(f"Hygraph GraphQL errors: {data['errors']}")
            return None
            
        return data.get('data')
    except requests.RequestException as e:
        print(f"Hygraph API error: {e}")
        return None

def get_local_markdown_fallback(slug: str) -> Optional[Dict[str, Any]]:
    """
    Get documentation from local markdown files as fallback
    """
    # Look for markdown files in docs directory
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    markdown_path = os.path.join(docs_dir, f"{slug}.md")
    
    if os.path.exists(markdown_path):
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract title from first line if it's a header
            title = slug.replace('-', ' ').title()
            lines = content.split('\n')
            if lines and lines[0].startswith('# '):
                title = lines[0][2:].strip()
            
            return {
                'id': slug,
                'title': title,
                'slug': slug,
                'content': content,
                'source': 'local_markdown'
            }
        except Exception as e:
            print(f"Error reading local markdown {slug}: {e}")
    
    return None

def list_local_markdown_docs() -> list:
    """
    List available local markdown documentation files
    """
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    docs = []
    
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            if filename.endswith('.md'):
                slug = filename[:-3]  # Remove .md extension
                title = slug.replace('-', ' ').title()
                
                # Try to extract title from file
                try:
                    with open(os.path.join(docs_dir, filename), 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('# '):
                            title = first_line[2:].strip()
                except:
                    pass
                
                docs.append({
                    'id': slug,
                    'title': title,
                    'slug': slug,
                    'source': 'local_markdown'
                })
    
    return docs

@docs_bp.route('/')
def docs_index():
    """
    List all available documentation
    """
    # Try to fetch from Hygraph first
    hygraph_data = fetch_from_hygraph(DOCS_LIST_QUERY)
    
    if hygraph_data and 'docs' in hygraph_data:
        docs = hygraph_data['docs']
        source = 'hygraph'
    else:
        # Fallback to local markdown
        docs = list_local_markdown_docs()
        source = 'local_markdown'
    
    # Simple HTML template for docs index
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
            .doc-list { list-style: none; padding: 0; }
            .doc-item { margin: 15px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .doc-link { text-decoration: none; color: #0066cc; font-size: 18px; }
            .doc-link:hover { text-decoration: underline; }
            .source-badge { 
                background: #f0f0f0; 
                padding: 3px 8px; 
                border-radius: 3px; 
                font-size: 12px; 
                margin-left: 10px; 
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Documentation</h1>
            <p>Source: <strong>{{ data_source }}</strong></p>
        </div>
        
        {% if docs %}
        <ul class="doc-list">
            {% for doc in docs %}
            <li class="doc-item">
                <a href="/docs/{{ doc.slug }}" class="doc-link">{{ doc.title }}</a>
                <span class="source-badge">{{ doc.get('source', 'hygraph') }}</span>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No documentation available.</p>
        {% endif %}
    </body>
    </html>
    """
    
    return render_template_string(template, docs=docs, data_source=source)

@docs_bp.route('/<slug>')
def get_doc(slug: str):
    """
    Get a specific document by slug
    """
    # Try to fetch from Hygraph first
    hygraph_data = fetch_from_hygraph(DOCS_QUERY, {'slug': slug})
    
    doc = None
    if hygraph_data and 'doc' in hygraph_data and hygraph_data['doc']:
        doc = hygraph_data['doc']
        doc['source'] = 'hygraph'
    else:
        # Fallback to local markdown
        doc = get_local_markdown_fallback(slug)
    
    if not doc:
        abort(404)
    
    # Simple HTML template for document display
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ doc.title }}</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                line-height: 1.6; 
            }
            .header { 
                border-bottom: 1px solid #eee; 
                padding-bottom: 20px; 
                margin-bottom: 30px; 
            }
            .source-badge { 
                background: #f0f0f0; 
                padding: 3px 8px; 
                border-radius: 3px; 
                font-size: 12px; 
                margin-left: 10px; 
            }
            .content {
                max-width: 800px;
            }
            .back-link {
                display: inline-block;
                margin-top: 30px;
                color: #0066cc;
                text-decoration: none;
            }
            .back-link:hover {
                text-decoration: underline;
            }
            pre {
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ doc.title }}</h1>
            <p>
                Slug: <code>{{ doc.slug }}</code>
                <span class="source-badge">{{ doc.source }}</span>
            </p>
        </div>
        
        <div class="content">
            {% if doc.content %}
                <pre>{{ doc.content }}</pre>
            {% else %}
                <p>No content available.</p>
            {% endif %}
        </div>
        
        <a href="/docs/" class="back-link">← Back to documentation index</a>
    </body>
    </html>
    """
    
    return render_template_string(template, doc=doc)

@docs_bp.route('/api/<slug>')
def get_doc_json(slug: str):
    """
    Get a specific document as JSON
    """
    # Try to fetch from Hygraph first
    hygraph_data = fetch_from_hygraph(DOCS_QUERY, {'slug': slug})
    
    doc = None
    if hygraph_data and 'doc' in hygraph_data and hygraph_data['doc']:
        doc = hygraph_data['doc']
        doc['source'] = 'hygraph'
    else:
        # Fallback to local markdown
        doc = get_local_markdown_fallback(slug)
    
    if not doc:
        abort(404)
    
    return jsonify(doc)