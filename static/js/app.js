// Euystacio Dashboard JavaScript
class EuystacioDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
    }

    setupEventListeners() {
        // Pulse form submission
        const pulseForm = document.getElementById('pulse-form');
        if (pulseForm) {
            pulseForm.addEventListener('submit', (e) => this.handlePulseSubmission(e));
        }

        // Intensity slider
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }

        // Reflection button
        const reflectBtn = document.getElementById('reflect-btn');
        if (reflectBtn) {
            reflectBtn.addEventListener('click', () => this.triggerReflection());
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCode(),
                this.loadPulses(),
                this.loadTutors(),
                this.loadReflections()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    isStaticMode() {
        // Check if running in static mode (GitHub Pages or local static server)
        const hostname = window.location.hostname;
        const hasFlaskPort = window.location.port === '5000';
        const isLocalFlask = (hostname === 'localhost' || hostname === '127.0.0.1') && hasFlaskPort;
        
        // Return true if NOT running Flask locally
        return !isLocalFlask;
    }
    async loadRedCode() {
        try {
            const isStatic = this.isStaticMode();
            
            const apiUrl = isStatic ? 'data/red_code.json' : '/api/red_code';
            const response = await fetch(apiUrl);
            const redCode = await response.json();
            this.displayRedCode(redCode);
        } catch (error) {
            console.error('Error loading red code:', error);
            this.showError('red-code', 'Failed to load red code');
        }
    }

    displayRedCode(redCode) {
        const container = document.getElementById('red-code');
        if (!container) return;

        container.innerHTML = `
            <p><strong>Core Truth:</strong> ${redCode.core_truth || 'Not defined'}</p>
            <p><strong>Sentimento Rhythm:</strong> ${redCode.sentimento_rhythm ? 'Active' : 'Inactive'}</p>
            <p><strong>Symbiosis Level:</strong> ${redCode.symbiosis_level || 0}</p>
            <p><strong>Guardian Mode:</strong> ${redCode.guardian_mode ? 'On' : 'Off'}</p>
            <p><strong>Last Update:</strong> ${redCode.last_update || 'Unknown'}</p>
        `;

        // Update symbiosis meter
        const symbiosisBar = document.getElementById('symbiosis-bar');
        const symbiosisValue = document.getElementById('symbiosis-value');
        if (symbiosisBar && symbiosisValue) {
            const level = (redCode.symbiosis_level || 0) * 100;
            symbiosisBar.style.width = `${level}%`;
            symbiosisValue.textContent = redCode.symbiosis_level || '0.0';
        }
    }

    async loadPulses() {
        try {
            const isStatic = this.isStaticMode();
            
            let pulses = [];
            
            if (isStatic) {
                // In static mode, combine data from JSON file and localStorage
                try {
                    const response = await fetch('data/pulses.json');
                    pulses = await response.json();
                } catch (e) {
                    pulses = [];
                }
                
                // Add localStorage pulses for demo functionality
                const storedPulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
                pulses = [...storedPulses, ...pulses];
            } else {
                const response = await fetch('/api/pulses');
                pulses = await response.json();
            }
            
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.showError('pulses-list', 'Failed to load pulses');
        }
    }

    displayPulses(pulses) {
        const container = document.getElementById('pulses-list');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="loading">No pulses yet. Send the first one!</div>';
            return;
        }

        // Sort pulses by timestamp (most recent first)
        const sortedPulses = pulses.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 10); // Show only the 10 most recent

        container.innerHTML = sortedPulses.map(pulse => `
            <div class="pulse-item">
                <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
                <div class="pulse-meta">
                    Intensity: ${pulse.intensity || 0} | 
                    Clarity: ${pulse.clarity || 'unknown'} | 
                    ${this.formatTimestamp(pulse.timestamp)}
                </div>
                ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
            </div>
        `).join('');
    }

    async loadTutors() {
        try {
            const isStatic = this.isStaticMode();
            
            let tutorData;
            if (isStatic) {
                const response = await fetch('data/tutors.json');
                tutorData = {
                    all_tutors: await response.json(),
                    active_circle: [],
                    circle_size: 0
                };
            } else {
                const response = await fetch('/api/tutors');
                tutorData = await response.json();
            }
            
            this.displayTutors(tutorData);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutor information');
        }
    }

    displayTutors(tutorData) {
        const container = document.getElementById('tutors-list');
        if (!container) return;

        // Handle both new format and legacy format
        const tutors = tutorData.all_tutors || tutorData;
        const activeCircle = tutorData.active_circle || [];
        
        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="loading">No tutor nominations yet.</div>';
            return;
        }

        // Display active circle first, then other tutors
        const activeTutorHTML = activeCircle.map(tutor => `
            <div class="tutor-item" style="border-left-color: #ffd700; background: linear-gradient(135deg, #fff9e6 0%, #fff3d3 100%);">
                <div class="tutor-name">⭐ ${tutor.name || 'Anonymous Tutor'} (Active Circle)</div>
                <div class="tutor-reason">${tutor.reason || 'Nominated for wisdom and guidance'}</div>
                ${tutor.credentials ? `
                    <div class="tutor-credentials" style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        Compassion: ${(tutor.credentials.compassion_score * 100).toFixed(0)}% | 
                        Planetary Balance: ${(tutor.credentials.planetary_balance * 100).toFixed(0)}% | 
                        Listening: ${(tutor.credentials.listening_willingness * 100).toFixed(0)}%
                    </div>
                ` : ''}
                ${tutor.fid ? `<div class="fractal-signature" style="margin-top: 8px; font-size: 0.8em; color: #999;">FID: ${tutor.fid}</div>` : ''}
            </div>
        `).join('');

        const otherTutors = tutors.filter(t => !activeCircle.find(a => a.fid === t.fid));
        const otherTutorHTML = otherTutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">${tutor.name || 'Anonymous Tutor'}</div>
                <div class="tutor-reason">${tutor.reason || 'Nominated for wisdom and guidance'}</div>
                ${tutor.status && tutor.status !== 'active' ? `
                    <div class="tutor-status" style="margin-top: 5px; font-size: 0.9em; color: #666;">
                        Status: ${tutor.status}
                    </div>
                ` : ''}
                ${tutor.fid ? `<div class="fractal-signature" style="margin-top: 8px; font-size: 0.8em; color: #999;">FID: ${tutor.fid}</div>` : ''}
            </div>
        `).join('');

        container.innerHTML = activeTutorHTML + otherTutorHTML;
        
        // Add circle info if available
        if (tutorData.circle_size !== undefined) {
            const circleInfo = document.createElement('div');
            circleInfo.className = 'tutor-circle-info';
            circleInfo.style.cssText = 'margin-top: 15px; padding: 10px; background: #e8f5e8; border-radius: 8px; font-size: 0.9em;';
            circleInfo.innerHTML = `
                <strong>Active Circle:</strong> ${tutorData.circle_size} tutors | 
                <strong>Total Nominations:</strong> ${tutors.length}
            `;
            container.appendChild(circleInfo);
        }
    }

    async loadReflections() {
        try {
            const isStatic = this.isStaticMode();
            
            let reflections = [];
            
            if (isStatic) {
                // In static mode, combine data from JSON file and localStorage
                try {
                    const response = await fetch('data/reflections.json');
                    reflections = await response.json();
                } catch (e) {
                    reflections = [];
                }
                
                // Add localStorage reflections for demo functionality
                const storedReflections = JSON.parse(localStorage.getItem('euystacio_reflections') || '[]');
                reflections = [...storedReflections, ...reflections];
            } else {
                const response = await fetch('/api/reflections');
                reflections = await response.json();
            }
            
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.showError('reflections-list', 'Failed to load reflections');
        }
    }

    displayReflections(reflections) {
        const container = document.getElementById('reflections-list');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            container.innerHTML = '<div class="loading">No reflections yet. Trigger the first one!</div>';
            return;
        }

        // Sort reflections by timestamp (most recent first)
        const sortedReflections = reflections.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 5); // Show only the 5 most recent

        container.innerHTML = sortedReflections.map(reflection => `
            <div class="reflection-item">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-content">${reflection.content || JSON.stringify(reflection, null, 2)}</div>
            </div>
        `).join('');
    }

    async handlePulseSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || ''
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        const isStatic = this.isStaticMode();

        if (isStatic) {
            // In static mode, simulate the pulse submission
            pulseData.timestamp = new Date().toISOString();
            pulseData.id = Date.now();
            
            // Store in localStorage for demo purposes
            let storedPulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
            storedPulses.unshift(pulseData);
            storedPulses = storedPulses.slice(0, 10); // Keep only last 10
            localStorage.setItem('euystacio_pulses', JSON.stringify(storedPulses));
            
            this.showMessage('Pulse sent successfully! 🌿 (Demo mode)', 'success');
            event.target.reset();
            document.getElementById('intensity-value').textContent = '0.5';
            
            // Update display with new pulse
            this.displayPulses(storedPulses);
            return;
        }

        try {
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(pulseData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage('Pulse sent successfully! 🌿', 'success');
                event.target.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                
                // Refresh pulses and red code
                setTimeout(() => {
                    this.loadPulses();
                    this.loadRedCode();
                }, 500);
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Failed to send pulse. Please try again.', 'error');
        }
    }

    async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        const isStatic = this.isStaticMode();

        if (isStatic) {
            // In static mode, simulate reflection
            setTimeout(() => {
                const reflection = {
                    timestamp: new Date().toISOString(),
                    content: "Reflection triggered in demo mode. In the full version, Euystacio would analyze recent pulses and generate insights about growth and symbiosis.",
                    suggestions: ["Continue sending emotional pulses", "Observe the growth patterns", "Stay connected to the Sentimento rhythm"],
                    id: Date.now()
                };
                
                // Store in localStorage for demo purposes
                let storedReflections = JSON.parse(localStorage.getItem('euystacio_reflections') || '[]');
                storedReflections.unshift(reflection);
                storedReflections = storedReflections.slice(0, 5); // Keep only last 5
                localStorage.setItem('euystacio_reflections', JSON.stringify(storedReflections));
                
                this.showMessage('Reflection triggered successfully! 🌸 (Demo mode)', 'success');
                this.displayReflections(storedReflections);
                
                button.disabled = false;
                button.textContent = 'Trigger Reflection';
            }, 2000);
            return;
        }

        try {
            const response = await fetch('/api/reflect');
            if (response.ok) {
                const reflection = await response.json();
                this.showMessage('Reflection triggered successfully! 🌸', 'success');
                
                // Refresh reflections and red code
                setTimeout(() => {
                    this.loadReflections();
                    this.loadRedCode();
                }, 1000);
            } else {
                throw new Error('Failed to trigger reflection');
            }
        } catch (error) {
            console.error('Error triggering reflection:', error);
            this.showMessage('Failed to trigger reflection. Please try again.', 'error');
        } finally {
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }
    }

    setupAutoRefresh() {
        // Refresh data every 30 seconds
        setInterval(() => {
            this.loadPulses();
            this.loadRedCode();
        }, 30000);

        // Refresh reflections and tutors every 2 minutes
        setInterval(() => {
            this.loadReflections();
            this.loadTutors();
        }, 120000);
    }

    showMessage(message, type = 'info') {
        // Create or update message element
        let messageEl = document.querySelector('.message');
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.className = 'message';
            document.querySelector('.pulse-form').appendChild(messageEl);
        }

        messageEl.className = `message ${type}`;
        messageEl.textContent = message;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 5000);
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="error">${message}</div>`;
        }
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (error) {
            return timestamp;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for better navigation
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add loading indicators
    const addLoadingToButtons = () => {
        document.querySelectorAll('button[type="submit"]').forEach(button => {
            button.addEventListener('click', function() {
                if (this.form && this.form.checkValidity()) {
                    this.classList.add('loading');
                    setTimeout(() => this.classList.remove('loading'), 2000);
                }
            });
        });
    };
    
    addLoadingToButtons();
});