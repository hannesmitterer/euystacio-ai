# WebSocket Real-Time Updates

This document describes the WebSocket real-time update functionality added to the Euystacio Dashboard.

## Overview

The dashboard now supports bidirectional real-time communication using WebSockets in addition to the existing polling mechanism. This provides immediate updates when data changes, creating a more responsive user experience.

## Features

### Real-Time Events

The WebSocket implementation broadcasts the following events to all connected clients:

1. **`pulse_update`** - Triggered when a new emotional pulse is submitted
   - Contains the new pulse data and complete pulse list
   - Updates the pulse feed in real-time

2. **`reflection_update`** - Triggered when a reflection is generated
   - Contains the new reflection data and complete reflection list
   - Updates the evolution log immediately

3. **`red_code_update`** - Triggered when the core red code data changes
   - Updates symbiosis levels, guardian mode status, etc.
   - Triggered by both pulse submissions and reflections

4. **`tutors_update`** - Triggered when tutor nominations are updated
   - Updates the tutors list in real-time

### Fallback Mechanism

The system gracefully falls back to polling-based updates if:
- WebSocket connection fails
- Socket.IO library is not available
- Network restrictions prevent WebSocket connections

When using polling fallback:
- Data refreshes every 30 seconds for pulses and red code
- Reflections and tutors refresh every 2 minutes
- A connection status indicator shows the current mode

## Implementation Details

### Backend (Flask-SocketIO)

**Dependencies:**
- `flask-socketio>=5.3.0` - WebSocket support for Flask

**Key Components:**
- WebSocket event handlers for connect/disconnect
- Real-time broadcasting on data changes
- Backward compatibility with existing REST API

**Events Emitted:**
```python
# On new pulse submission
socketio.emit('pulse_update', {
    'pulse': event,
    'allPulses': get_pulses()
})

# On reflection trigger
socketio.emit('reflection_update', {
    'reflection': reflection,
    'allReflections': get_reflections()
})

# On red code changes
socketio.emit('red_code_update', RED_CODE)
```

### Frontend (JavaScript)

**Features:**
- Automatic WebSocket connection detection
- Real-time event listeners
- Graceful fallback to polling
- Connection status indicators

**Key Functions:**
- `setupWebSocket()` - Initializes WebSocket connection
- `showConnectionStatus()` - Displays connection state
- Real-time event handlers for each data type

## Configuration

### Production Deployment

For production environments with WebSocket support:

1. **Install dependencies:**
   ```bash
   pip install flask-socketio>=5.3.0
   ```

2. **Run with production WSGI server:**
   ```bash
   # Using Gunicorn with eventlet workers
   pip install gunicorn eventlet
   gunicorn --worker-class eventlet -w 1 app:app
   ```

3. **Configure reverse proxy (nginx):**
   ```nginx
   location /socket.io/ {
       proxy_pass http://127.0.0.1:5000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
       proxy_set_header Host $host;
   }
   ```

### Static Deployment (GitHub Pages)

For static deployments where WebSocket backend is not available:
- The system automatically detects static mode
- Falls back to polling-based updates
- Uses localStorage for demo functionality
- All features remain functional

## Testing

### Manual Testing

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open multiple browser tabs** to `http://localhost:5000`

3. **Submit a pulse** in one tab and observe real-time updates in other tabs

4. **Trigger reflections** and verify immediate updates across all clients

### WebSocket Connection Testing

- Console logs show connection status
- Connection indicator displays current mode
- Fallback functionality can be tested by blocking WebSocket connections

## Benefits

### Real-Time Experience
- Immediate updates without page refreshes
- Synchronized data across multiple clients
- Enhanced collaboration for multiple users

### Backward Compatibility
- Existing REST API endpoints preserved
- Polling fallback ensures universal compatibility
- No breaking changes to existing functionality

### Performance
- Reduced server load with push-based updates
- Fewer unnecessary API calls
- More efficient data synchronization

## Browser Support

WebSocket functionality works in all modern browsers:
- Chrome/Chromium (all versions)
- Firefox (all versions)
- Safari (all versions)
- Edge (all versions)

Older browsers automatically fall back to polling mode.

## Troubleshooting

### Common Issues

1. **WebSocket connection fails:**
   - Check that Flask-SocketIO is installed
   - Verify no firewall blocking WebSocket ports
   - System falls back to polling automatically

2. **Real-time updates not working:**
   - Check browser console for connection errors
   - Verify Socket.IO client library is loading
   - Confirm backend is emitting events correctly

3. **High CPU usage:**
   - May indicate too frequent polling fallback
   - Check WebSocket connection stability
   - Adjust polling intervals if needed

### Debug Mode

Enable debug logging:
```python
socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
```

Monitor console logs for:
- Connection/disconnection events
- Event broadcasting
- Fallback mode activation