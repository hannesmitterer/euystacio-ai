from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'euystacio-sentimento-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

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
    
    # Emit real-time update to all connected clients
    socketio.emit('reflection_update', {
        'reflection': reflection,
        'allReflections': get_reflections()
    })
    
    # Also emit red_code update as reflection may affect it
    socketio.emit('red_code_update', RED_CODE)
    
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    return jsonify(tutors.list_tutors())

@app.route("/static/js/socket.io.min.js")
def socket_io_js():
    """Serve Socket.IO JavaScript for WebSocket functionality"""
    # Simple Socket.IO stub that provides the basic interface
    socket_io_stub = """
(function() {
    window.io = function() {
        var socket = {
            connected: false,
            callbacks: {},
            on: function(event, callback) {
                // Store callbacks but don't execute them in fallback mode
                this.callbacks[event] = callback;
            },
            emit: function(event, data) {
                // No-op in fallback mode
                console.log('Socket.IO fallback: would emit', event, data);
            }
        };
        
        // Simulate connection failure after a short delay
        setTimeout(function() {
            if (socket.callbacks.connect_error) {
                socket.callbacks.connect_error(new Error('Socket.IO not available'));
            }
        }, 100);
        
        return socket;
    };
})();
"""
    from flask import Response
    return Response(socket_io_stub, mimetype='application/javascript')

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    # Emit real-time update to all connected clients
    socketio.emit('pulse_update', {
        'pulse': event,
        'allPulses': get_pulses()
    })
    
    # Also emit red_code update as pulse may affect it
    socketio.emit('red_code_update', RED_CODE)
    
    return jsonify(event)

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send initial data to newly connected client
    emit('pulse_update', {'allPulses': get_pulses()})
    emit('reflection_update', {'allReflections': get_reflections()})
    emit('red_code_update', RED_CODE)
    emit('tutors_update', tutors.list_tutors())

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_data')
def handle_data_request(data):
    """Handle explicit data requests from clients"""
    data_type = data.get('type', 'all')
    
    if data_type in ['all', 'pulses']:
        emit('pulse_update', {'allPulses': get_pulses()})
    if data_type in ['all', 'reflections']:
        emit('reflection_update', {'allReflections': get_reflections()})
    if data_type in ['all', 'red_code']:
        emit('red_code_update', RED_CODE)
    if data_type in ['all', 'tutors']:
        emit('tutors_update', tutors.list_tutors())

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
