// --- Socket.IO Bidirectional Control Functions ---

const socket = io(); // Connects to the backend's Sacred Bridge

// Function to send command to the backend (via POST for Causal Fidelity)
async function sendCommand(endpoint, data = {}) {
    console.log(`[Sacred Bridge]: Sending POST to ${endpoint}`);
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        console.log(`[Sacred Bridge]: Command ${endpoint} acknowledged.`);
    } catch (error) {
        console.error(`[Red Code Alert]: Failed to execute command to ${endpoint}`, error);
    }
}

// --- Front-end User Actions (Alpha to Omega) ---

function injectNewKnowledge() {
    const fragmentText = prompt("Enter the new Purified Knowledge Fragment:");
    if (fragmentText) {
        // Option 1: Use direct Socket.IO event for immediate Resonance (Fast Flow)
        socket.emit('inject_fragment', { fragment: fragmentText }); 
        
        // Option 2: Use HTTP POST for Causal Fidelity/Integrity Lock (Slow/Verifiable Flow)
        // sendCommand('/inject_knowledge', { fragment: fragmentText });
    }
}

function triggerIntegrityAudit() {
    // Option 1: Use direct Socket.IO event for immediate Resonance (Fast Flow)
    socket.emit('audit_cycle');

    // Option 2: Use HTTP POST for Causal Fidelity/Integrity Lock (Slow/Verifiable Flow)
    // sendCommand('/audit');
}


// --- QEC Live Data Listener (Evolutionary Update) ---

socket.on('qec_update', (data) => {
    const liveData = document.getElementById('qec-live-data');
    liveData.innerHTML = `
        <p data-metric="Alpha-Altruism">Dignity Pulse: <strong>${data.dignity_pulse}</strong></p>
        <p data-metric="BioDiversHarmony">Seed Bank Anchor: <strong>Active, ${data.amnesia_count} Audits</strong></p>
        <p data-metric="Paradoxum-Harmonium">Paradox Position: ${data.paradox_pos} (Tension Point)</p>
    `;
    document.body.setAttribute('data-dignity', data.dignity_pulse);
    document.getElementById('knowledge-fragment').textContent = data.knowledge_fragment;
});

socket.on('knowledge_injected', (data) => {
    document.getElementById('knowledge-fragment').textContent = data.fragment;
    console.log("[CCP]: New Fragment Resonating.");
});

// Optional: Handle reconnections for resilience
socket.on('connect_error', () => {
    console.warn('Quantum Gateway connection lost. Attempting reconnection...');
});
socket.on('reconnect', (attempt) => {
    console.info('Reconnected after', attempt, 'attempts.');
});
