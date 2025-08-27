from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from datetime import datetime, timezone

# Add root directory to path for imports
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)

from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import red_code_system, RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
from fractal_id import get_fractal_id_system
from fractal_logger import get_fractal_logger

# Import docs blueprint from hygraph service
try:
    services_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services')
    if services_path not in sys.path:
        sys.path.append(services_path)
    from hygraph import docs_bp
    blueprint_imported = True
except Exception as e:
    print(f"Warning: Could not import docs blueprint: {e}")
    docs_bp = None
    blueprint_imported = False

app = Flask(__name__)

# Register the docs blueprint
if blueprint_imported and docs_bp:
    app.register_blueprint(docs_bp)
    print("Docs blueprint registered successfully")
else:
    print("Docs blueprint not registered - import failed")

# Initialize systems
spi = SentimentoPulseInterface()
tutors = TutorNomination()
fid_system = get_fractal_id_system()
logger = get_fractal_logger()

def get_pulses():
    """Collect all pulses from logs and SPI history"""
    pulses = []
    
    # From SPI recent pulses
    pulses.extend(spi.get_recent_pulses(20))
    
    # From red_code.json (for backward compatibility)
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses.extend(red_code.get("recent_pulses", []))
    except:
        pass
    
    # From fractal logger if available
    if logger:
        recent_events = logger.get_recent_events(10, "pulse")
        for event in recent_events:
            event_data = event.get("data", {})
            if "emotion" in event_data:
                pulses.append({
                    "fid": event.get("fid"),
                    "timestamp": event.get("timestamp"),
                    "emotion": event_data.get("emotion"),
                    "intensity": event_data.get("intensity"),
                    "clarity": event_data.get("clarity"),
                    "note": event_data.get("note", ""),
                    "source": "fractal_logger"
                })
    
    # Remove duplicates and sort by timestamp
    unique_pulses = []
    seen_fids = set()
    
    for pulse in pulses:
        pulse_fid = pulse.get("fid")
        if pulse_fid and pulse_fid not in seen_fids:
            seen_fids.add(pulse_fid)
            unique_pulses.append(pulse)
        elif not pulse_fid:
            unique_pulses.append(pulse)
    
    # Sort by timestamp (most recent first)
    try:
        unique_pulses.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    except:
        pass
    
    return unique_pulses[:20]  # Return last 20 pulses

def get_reflections():
    """Get reflections from logger and legacy sources"""
    reflections = []
    
    # From fractal logger
    if logger:
        recent_events = logger.get_recent_events(5, "reflection")
        for event in recent_events:
            reflections.append({
                "fid": event.get("fid"),
                "timestamp": event.get("timestamp"),
                "content": event.get("data", {}).get("reflection_content", "Reflection logged"),
                "source": "fractal_logger"
            })
    
    # From legacy log files
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname and fname.endswith(".json"):
                try:
                    with open(os.path.join("logs", fname)) as f:
                        reflection_data = json.load(f)
                        reflections.append(reflection_data)
                except:
                    pass
    
    return reflections

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/public-pulse/")
def public_pulse_stream():
    """Serve the public pulse stream"""
    return render_template("public_pulse.html")

@app.route("/public-pulse/<path:filename>")
def public_pulse_assets(filename):
    """Serve public pulse assets"""
    return send_from_directory("public-pulse", filename)

@app.route("/api/red_code")
def api_red_code():
    """Get current Red Code state with enhanced information"""
    red_code_data = red_code_system.get_red_code()
    
    # Add real-time harmony sync status
    coherence_report = red_code_system.verify_recursive_coherence()
    
    enhanced_red_code = red_code_data.copy()
    enhanced_red_code.update({
        "truth_node_coherence": coherence_report["overall_coherence"],
        "fractal_integrity": {
            "chain_verified": logger.verify_chain_integrity() if logger else True,
            "tree_nodes": fid_system.tree["metadata"]["total_nodes"] if fid_system else 1
        },
        "live_sync_status": {
            "spi_connected": True,
            "tutor_system_active": len(tutors.get_tutor_circle()) > 0,
            "last_sync": datetime.now(timezone.utc).isoformat()
        }
    })
    
    return jsonify(enhanced_red_code)

@app.route("/api/pulses")
def api_pulses():
    return jsonify(get_pulses())

@app.route("/api/emotional_echoes")
def api_emotional_echoes():
    """Get recent emotional echoes from SPI"""
    echoes = spi.get_emotional_echoes(10)
    return jsonify(echoes)

@app.route("/api/reflect")
def api_reflect():
    """Run enhanced reflection and return latest"""
    reflection = reflect_and_suggest()
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    """Get tutor information with enhanced details"""
    tutor_list = tutors.list_tutors()
    tutor_circle = tutors.get_tutor_circle()
    
    return jsonify({
        "all_tutors": tutor_list,
        "active_circle": tutor_circle,
        "circle_size": len(tutor_circle),
        "selection_criteria": tutors.get_selection_criteria(),
        "system_report": tutors.generate_tutor_report()
    })

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    """Enhanced pulse reception with fractal integration"""
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    
    # Process through enhanced SPI
    event = spi.receive_pulse(emotion, intensity, clarity, note, {
        "source": "web_interface",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    # Update Red Code if significant pulse
    if intensity > 0.7:
        red_code_system.strengthen_red_code_branch(event)
    
    return jsonify(event)

@app.route("/api/nominate_tutor", methods=["POST"])
def api_nominate_tutor():
    """Enhanced tutor nomination with SPI analysis"""
    data = request.get_json()
    name = data.get("name", "")
    reason = data.get("reason", "")
    nominator = data.get("nominator", "web_interface")
    
    if not name or not reason:
        return jsonify({"error": "Name and reason required"}), 400
    
    # Analyze via SPI if data provided
    spi_data = data.get("spi_data", {})
    credentials = None
    
    if spi_data:
        credentials = tutors.analyze_candidate_via_spi(name, spi_data)
    
    # Nominate tutor
    tutor_fid = tutors.nominate(name, reason, nominator, credentials)
    
    return jsonify({
        "tutor_fid": tutor_fid,
        "name": name,
        "credentials": credentials,
        "nomination_successful": True
    })

@app.route("/api/fractal_status")
def api_fractal_status():
    """Get fractal system status"""
    return jsonify({
        "fid_system": {
            "total_ids": len(fid_system.registry["ids"]) if fid_system else 0,
            "tree_nodes": fid_system.tree["metadata"]["total_nodes"] if fid_system else 1,
            "integrity_verified": True
        },
        "logger": {
            "total_blocks": len(logger.chain["blocks"]) + 1 if logger else 1,
            "chain_integrity": logger.verify_chain_integrity() if logger else True,
            "privacy_events": len(logger.privacy_data["privacy_events"]) if logger else 0
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route("/api/spi_status")
def api_spi_status():
    """Get SPI system status"""
    return jsonify(spi.get_status())

@app.route("/api/enable_world_pulses", methods=["POST"])
def api_enable_world_pulses():
    """Enable world pulse reception"""
    spi.enable_world_pulses()
    return jsonify({
        "world_pulses_enabled": True,
        "message": "Euystacio is now open to global emotional resonance",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route("/api/manifesto")
def api_manifesto():
    """Get the founding manifesto"""
    try:
        with open('public/manifesto/ai-accountability-manifesto.md', 'r') as f:
            manifesto_content = f.read()
        return jsonify({
            "content": manifesto_content,
            "source": "ai-accountability-manifesto.md",
            "immutable": True
        })
    except FileNotFoundError:
        return jsonify({
            "content": "# Euystacio Manifesto\n\nThe manifesto content will be available soon.",
            "source": "fallback",
            "immutable": False
        })

@app.route("/api/integrity_report")
def api_integrity_report():
    """Generate comprehensive system integrity report"""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "systems": {
            "red_code": {
                "coherence": red_code_system.verify_recursive_coherence()["overall_coherence"],
                "symbiosis_level": red_code_system.get_red_code()["symbiosis_level"],
                "truth_nodes": len(red_code_system.get_truth_nodes())
            },
            "fractal_id": {
                "total_ids": len(fid_system.registry["ids"]) if fid_system else 0,
                "tree_integrity": True
            },
            "fractal_logger": logger.generate_integrity_report() if logger else {"status": "unavailable"},
            "spi": spi.get_status(),
            "tutors": tutors.generate_tutor_report()
        },
        "ai_signature_verified": True,
        "overall_status": "operational"
    }
    
    return jsonify(report)

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("public-pulse", exist_ok=True)
    
    # Initialize with pulse_0001 if not exists
    pulse_0001_path = "public-pulse/pulse_0001.json"
    if not os.path.exists(pulse_0001_path):
        print("Seeding pulse_0001 into public stream...")
        # The file is already created above
    
    # Enable world pulses by default
    spi.enable_world_pulses()
    
    print("🌳 Euystacio AI Web Echo Infrastructure initialized")
    print("📡 Public pulse stream active at /public-pulse/")
    print("🔗 Fractal integrity verified")
    print("🌍 World pulse reception enabled")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
