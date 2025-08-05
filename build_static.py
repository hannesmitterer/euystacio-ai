import os
import shutil
import json
from jinja2 import Template

def create_static_version():
    """
    Generate static HTML files from Flask templates for GitHub Pages deployment
    """
    print("Creating static version...")
    
    # Create static output directory
    static_dir = "static_build"
    if os.path.exists(static_dir):
        shutil.rmtree(static_dir)
    os.makedirs(static_dir)
    
    # Copy static assets (CSS, JS)
    if os.path.exists("static"):
        shutil.copytree("static", os.path.join(static_dir, "static"))
    
    # Copy docs directory for GitHub Pages access
    if os.path.exists("docs"):
        shutil.copytree("docs", os.path.join(static_dir, "docs"))
    
    # Load template
    with open("templates/index.html", "r") as f:
        template_content = f.read()
    
    # Convert Flask template to static HTML
    static_html = template_content.replace(
        "{{ url_for('static', filename='css/style.css') }}", 
        "static/css/style.css"
    ).replace(
        "{{ url_for('static', filename='js/app.js') }}", 
        "static/js/app.js"
    )
    
    # Write static index.html
    with open(os.path.join(static_dir, "index.html"), "w") as f:
        f.write(static_html)
    
    # Generate static data files for API endpoints
    generate_static_data(static_dir)
    
    print(f"Static version created in {static_dir}/")

def generate_static_data(static_dir):
    """
    Generate static JSON files to replace API endpoints
    """
    data_dir = os.path.join(static_dir, "data")
    os.makedirs(data_dir)
    
    # Load red_code.json
    red_code = {}
    if os.path.exists("red_code.json"):
        with open("red_code.json", "r") as f:
            red_code = json.load(f)
    else:
        red_code = {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": "2025-01-31",
            "growth_history": []
        }
    
    # Write static data files
    with open(os.path.join(data_dir, "red_code.json"), "w") as f:
        json.dump(red_code, f, indent=2)
    
    # Create empty arrays for dynamic data
    with open(os.path.join(data_dir, "pulses.json"), "w") as f:
        json.dump([], f)
    
    with open(os.path.join(data_dir, "tutors.json"), "w") as f:
        json.dump([], f)
    
    with open(os.path.join(data_dir, "reflections.json"), "w") as f:
        json.dump([], f)

def build_bidirectional_dashboard():
    """
    Stub function for bidirectional dashboard creation.
    This function serves as a placeholder for potential future bidirectional dashboard functionality. Currently, it delegates to the existing static version creation process to maintain compatibility.
    """
    print("Building bidirectional dashboard...")
    create_static_version()
    print("Bidirectional dashboard build completed (using static version)")

if __name__ == "__main__":
    create_static_version()
