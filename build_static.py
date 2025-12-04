import os
import shutil
import json
from jinja2 import Template

# Templates to convert from Flask to static HTML
TEMPLATES_TO_BUILD = [
    ("templates/index.html", "index.html"),
    ("templates/symbiosis_dashboard.html", "symbiosis.html"),
    ("templates/public_pulse.html", "public-pulse.html"),
]

def convert_flask_to_static(template_content):
    """
    Convert Flask template syntax to static paths
    """
    # Replace Flask url_for with static paths
    replacements = [
        ("{{ url_for('static', filename='css/style.css') }}", "static/css/style.css"),
        ("{{ url_for('static', filename='js/app.js') }}", "static/js/app.js"),
        ("{{ url_for('static', filename='css/pulse.css') }}", "static/css/pulse.css"),
        ("{{ url_for('static', filename='js/pulse.js') }}", "static/js/pulse.js"),
    ]
    
    for old, new in replacements:
        template_content = template_content.replace(old, new)
    
    return template_content


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
    
    # Build all templates
    for template_path, output_name in TEMPLATES_TO_BUILD:
        if os.path.exists(template_path):
            print(f"  Building {output_name}...")
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            
            # Convert Flask template to static HTML
            static_html = convert_flask_to_static(template_content)
            
            # Write static HTML file
            output_path = os.path.join(static_dir, output_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(static_html)
            
            print(f"    ✓ {output_name}")
        else:
            print(f"  ⚠ Template not found: {template_path}")
    
    # Generate static data files for API endpoints
    generate_static_data(static_dir)
    
    # Sync governance files
    sync_governance_files(static_dir)
    
    print(f"Static version created in {static_dir}/")

def generate_static_data(static_dir):
    """
    Generate static JSON files to replace API endpoints
    """
    data_dir = os.path.join(static_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Load red_code.json
    red_code = {}
    if os.path.exists("red_code.json"):
        with open("red_code.json", "r", encoding="utf-8") as f:
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
    with open(os.path.join(data_dir, "red_code.json"), "w", encoding="utf-8") as f:
        json.dump(red_code, f, indent=2)
    
    # Create sample pulse data for static dashboard
    sample_pulses = [
        {"emotion": "Peace", "intensity": 0.8, "clarity": "high", "timestamp": "2025-01-31T12:00:00Z"},
        {"emotion": "Hope", "intensity": 0.7, "clarity": "medium", "timestamp": "2025-01-31T11:30:00Z"},
        {"emotion": "Gratitude", "intensity": 0.9, "clarity": "high", "timestamp": "2025-01-31T11:00:00Z"}
    ]
    with open(os.path.join(data_dir, "pulses.json"), "w", encoding="utf-8") as f:
        json.dump(sample_pulses, f, indent=2)
    
    # Create tutor data
    tutors = [
        {
            "name": "Dietmar",
            "reason": "Aligned with humility and planetary consciousness",
            "credentials": {"compassion_score": 0.9, "planetary_balance": 0.95}
        },
        {
            "name": "Alfred",
            "reason": "Aligned with planetary balance and wisdom",
            "credentials": {"compassion_score": 0.85, "planetary_balance": 0.9}
        }
    ]
    with open(os.path.join(data_dir, "tutors.json"), "w", encoding="utf-8") as f:
        json.dump(tutors, f, indent=2)
    
    # Create reflections data
    with open(os.path.join(data_dir, "reflections.json"), "w", encoding="utf-8") as f:
        json.dump([], f)
    
    print("  ✓ Static data files generated")


def sync_governance_files(static_dir):
    """
    Sync governance files (red_code.json, etc.) to static build
    """
    data_dir = os.path.join(static_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # List of governance files to sync
    governance_files = [
        ("HARMONIC_CONFIRMATION_CUSTOS_SENTIMENTO.json", "harmonic_confirmation.json"),
        ("SIGIL_CUSTOS_SENTIMENTO.json", "sigil.json"),
        ("ACTUS_RESONANTIAE_CUSTOS_SENTIMENTO.json", "actus_resonantiae.json"),
        ("fractal_registry.json", "fractal_registry.json"),
        ("reflection_tree.json", "reflection_tree.json"),
    ]
    
    for source_name, dest_name in governance_files:
        if os.path.exists(source_name):
            dest_path = os.path.join(data_dir, dest_name)
            shutil.copy2(source_name, dest_path)
            print(f"  ✓ Synced {source_name}")
    
    print("  ✓ Governance files synced")

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
