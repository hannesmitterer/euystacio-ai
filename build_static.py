import os
import shutil
import json
from jinja2 import Template

def create_static_version():
    """
    Generate static HTML files from Flask templates for GitHub Pages deployment
    """
    print("Creating static version...")
    
    # Create static output directory - use docs for GitHub Pages
    static_dir = "docs"
    if os.path.exists(static_dir):
        # Preserve existing docs structure but update the deployment files
        if os.path.exists(os.path.join(static_dir, "index.html")):
            print("Updating existing docs directory...")
    else:
        os.makedirs(static_dir)
    
    # Copy static assets (CSS, JS) - preserve existing assets in docs
    if os.path.exists("static"):
        # Copy CSS files
        css_source = os.path.join("static", "css")
        css_dest = os.path.join(static_dir, "css")
        if os.path.exists(css_source):
            if os.path.exists(css_dest):
                shutil.rmtree(css_dest)
            shutil.copytree(css_source, css_dest)
        
        # Copy JS files but update to enhanced version
        js_source = os.path.join("static", "js")
        js_dest = os.path.join(static_dir, "js")
        if os.path.exists(js_source):
            if not os.path.exists(js_dest):
                os.makedirs(js_dest)
            # Copy all JS files from static/js to docs/js
            for js_file in os.listdir(js_source):
                if js_file.endswith('.js'):
                    shutil.copy2(os.path.join(js_source, js_file), os.path.join(js_dest, js_file))
    
    # Load template
    with open("templates/index.html", "r") as f:
        template_content = f.read()
    
    # Convert Flask template to static HTML
    static_html = template_content.replace(
        "{{ url_for('static', filename='css/style.css') }}", 
        "css/style.css"
    ).replace(
        "{{ url_for('static', filename='js/app.js') }}", 
        "js/app-static.js"
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
    # Create API directory structure to match expected paths
    api_dir = os.path.join(static_dir, "api")
    if not os.path.exists(api_dir):
        os.makedirs(api_dir)
    
    data_dir = os.path.join(static_dir, "data")
    if not os.path.exists(data_dir):
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
    
    # Write static data files to both locations for compatibility
    with open(os.path.join(data_dir, "red_code.json"), "w") as f:
        json.dump(red_code, f, indent=2)
    with open(os.path.join(api_dir, "red_code.json"), "w") as f:
        json.dump(red_code, f, indent=2)
    
    # Create empty arrays for dynamic data
    empty_pulses = []
    with open(os.path.join(data_dir, "pulses.json"), "w") as f:
        json.dump(empty_pulses, f)
    with open(os.path.join(api_dir, "pulses.json"), "w") as f:
        json.dump(empty_pulses, f)
    
    empty_tutors = [
        {"name": "Dietmar", "reason": "Aligned with humility and planetary consciousness"},
        {"name": "Alfred", "reason": "Aligned with planetary balance and wisdom"}
    ]
    with open(os.path.join(data_dir, "tutors.json"), "w") as f:
        json.dump(empty_tutors, f)
    with open(os.path.join(api_dir, "tutors.json"), "w") as f:
        json.dump(empty_tutors, f)
    
    empty_reflections = [
        {
            "timestamp": "2025-01-31T12:00:00Z",
            "content": "Welcome to Euystacio. This AI system grows through emotional resonance and human interaction. The tree metaphor guides the interface - from deep roots of core values to the evolving canopy of reflections."
        }
    ]
    with open(os.path.join(data_dir, "reflections.json"), "w") as f:
        json.dump(empty_reflections, f)
    with open(os.path.join(api_dir, "reflections.json"), "w") as f:
        json.dump(empty_reflections, f)

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
