from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os
from datetime import datetime

app = Flask(__name__)

spi = SentimentoPulseInterface()
tutors = TutorNomination()

def get_pulses():
    # Collect all pulses from logs and recent_pulses in red_code.json
    pulses = []
    # From red_code.json
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except:
        pass
    # From logs
    for fname in sorted(os.listdir("logs")):
        if fname.startswith("log_") and fname.endswith(".json"):
            with open(os.path.join("logs", fname)) as f:
                log = json.load(f)
                for k, v in log.items():
                    if isinstance(v, dict) and "emotion" in v:
                        pulses.append(v)
    return pulses

def get_reflections():
    reflections = []
    for fname in sorted(os.listdir("logs")):
        if "reflection" in fname:
            with open(os.path.join("logs", fname)) as f:
                reflections.append(json.load(f))
    return reflections

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/red_code")
def api_red_code():
    return jsonify(RED_CODE)

@app.route("/api/pulses")
def api_pulses():
    return jsonify(get_pulses())

@app.route("/api/reflect")
def api_reflect():
    # Run reflection, return latest
    reflection = reflect_and_suggest()
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    return jsonify(tutors.list_tutors())

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    return jsonify(event)

@app.route("/api/contact", methods=["POST"])
def api_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        
        # Basic validation
        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400
            
        # Simple email validation
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            return jsonify({"error": "Invalid email address"}), 400
            
        # Log the contact attempt (in production, this would send an actual email)
        contact_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": name,
            "email": email,
            "message": message,
            "status": "received"
        }
        
        # In a real implementation, you would send an email here
        # For now, we'll just log it and return success
        print(f"Contact form submission: {contact_log}")
        
        # Save to a contact log file for demonstration
        try:
            import json
            contact_file = "contact_submissions.json"
            contacts = []
            if os.path.exists(contact_file):
                with open(contact_file, 'r') as f:
                    contacts = json.load(f)
            contacts.append(contact_log)
            with open(contact_file, 'w') as f:
                json.dump(contacts, f, indent=2)
        except Exception as e:
            print(f"Error saving contact log: {e}")
        
        return jsonify({
            "message": "Contact form submitted successfully", 
            "status": "success",
            "note": "This is a demo - in production, an email would be sent to hannes.mitterer@gmail.com"
        })
        
    except Exception as e:
        print(f"Error processing contact form: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True)
