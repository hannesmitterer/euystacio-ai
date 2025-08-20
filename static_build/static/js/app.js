// Euystacio Dashboard JavaScript
class EuystacioDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
        this.initialize3DVisualization();
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

        // 3D Visualization controls
        this.setup3DVisualizationControls();
    }

    setup3DVisualizationControls() {
        const resetBtn = document.getElementById('reset-view-btn');
        const animateBtn = document.getElementById('animate-btn');
        const fullscreenBtn = document.getElementById('fullscreen-btn');

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.threeDViz) {
                    this.threeDViz.resetView();
                }
            });
        }

        if (animateBtn) {
            animateBtn.addEventListener('click', () => {
                if (this.threeDViz) {
                    const isAnimating = this.threeDViz.toggleAnimation();
                    animateBtn.textContent = isAnimating ? '⏸️ Pause' : '▶️ Animate';
                }
            });
        }

        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                const container = document.getElementById('three-js-container');
                if (container) {
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                        fullscreenBtn.textContent = '🔍 Fullscreen';
                    } else {
                        container.requestFullscreen();
                        fullscreenBtn.textContent = '🔍 Exit Fullscreen';
                    }
                }
            });
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
                try {
                    const response = await fetch('data/pulses.json');
                    pulses = await response.json();
                } catch (error) {
                    console.warn('Static pulses file not found, using empty array');
                    pulses = [];
                }
            } else {
                const response = await fetch('/api/pulses');
                pulses = await response.json();
            }
            
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.showError('pulses-list', 'Failed to load emotional pulses');
        }
    }

    displayPulses(pulses) {
        this.pulses = pulses; // Store for 3D viz
        const container = document.getElementById('pulses-list');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="no-pulses">No pulses yet. Be the first to share your emotion with Euystacio!</div>';
            return;
        }

        container.innerHTML = pulses.map(pulse => `
            <div class="pulse-item" data-emotion="${pulse.emotion}" data-intensity="${pulse.intensity}">
                <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
                <div class="pulse-meta">
                    Intensity: ${pulse.intensity || 'N/A'} | 
                    Clarity: ${pulse.clarity || 'N/A'} | 
                    ${pulse.timestamp ? new Date(pulse.timestamp).toLocaleString() : 'Unknown time'}
                </div>
                ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
            </div>
        `).join('');

        // Update 3D visualization if available
        if (this.threeDViz) {
            this.threeDViz.updatePulses(pulses);
        }
    }

    async loadTutors() {
        try {
            const isStatic = this.isStaticMode();
            
            let tutors;
            
            if (isStatic) {
                try {
                    const response = await fetch('data/tutors.json');
                    tutors = await response.json();
                } catch (error) {
                    console.warn('Static tutors file not found, using fallback data');
                    tutors = [
                        { name: "Dietmar", reason: "Aligned with humility and planetary consciousness" },
                        { name: "Alfred", reason: "Aligned with planetary balance and wisdom" }
                    ];
                }
            } else {
                const response = await fetch('/api/tutors');
                tutors = await response.json();
            }
            
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutors');
        }
    }

    displayTutors(tutorsData) {
        const container = document.getElementById('tutors-list');
        if (!container) return;

        let tutors = tutorsData;
        if (tutorsData.active_circle) {
            tutors = tutorsData.active_circle;
        }

        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="no-tutors">No tutors in the circle yet.</div>';
            return;
        }

        container.innerHTML = tutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">⭐ ${tutor.name} ${tutor.active ? '(Active Circle)' : ''}</div>
                <div class="tutor-reason">${tutor.reason}</div>
                ${tutor.compassion ? `<div class="tutor-metrics">Compassion: ${Math.round(tutor.compassion * 100)}% | Planetary Balance: ${Math.round((tutor.planetary_balance || 0.8) * 100)}% | Listening: ${Math.round((tutor.listening_willingness || 0.85) * 100)}%</div>` : ''}
                ${tutor.fid ? `<div class="tutor-fid">FID: ${tutor.fid}</div>` : ''}
            </div>
        `).join('');
    }

    async loadReflections() {
        try {
            const isStatic = this.isStaticMode();
            
            let reflections;
            
            if (isStatic) {
                try {
                    const response = await fetch('data/reflections.json');
                    reflections = await response.json();
                } catch (error) {
                    console.warn('Static reflections file not found, using fallback');
                    reflections = [
                        {
                            timestamp: new Date().toISOString(),
                            content: "Welcome to Euystacio. This AI system grows through emotional resonance and human interaction. The tree metaphor guides the interface - from deep roots of core values to the evolving canopy of reflections."
                        }
                    ];
                }
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
            container.innerHTML = '<div class="no-reflections">No reflections yet. Trigger the first one!</div>';
            return;
        }

        container.innerHTML = reflections.map(reflection => `
            <div class="reflection-item">
                <div class="reflection-content">${reflection.content}</div>
                <div class="reflection-meta">${reflection.timestamp ? new Date(reflection.timestamp).toLocaleString() : 'Unknown time'}</div>
            </div>
        `).join('');
    }

    async handlePulseSubmission(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note')
        };

        const isStatic = this.isStaticMode();

        if (isStatic) {
            // In static mode, simulate pulse submission
            const newPulse = {
                ...pulseData,
                timestamp: new Date().toISOString(),
                fid: `demo-${Date.now()}`
            };
            
            // Store in localStorage for demo purposes
            let storedPulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
            storedPulses.unshift(newPulse);
            storedPulses = storedPulses.slice(0, 10); // Keep only last 10
            localStorage.setItem('euystacio_pulses', JSON.stringify(storedPulses));
            
            this.showMessage(`Pulse sent successfully! 🌿 (Demo mode)`, 'success');
            this.displayPulses(storedPulses);
            e.target.reset();
            document.getElementById('intensity-value').textContent = '0.5';
            return;
        }

        try {
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(pulseData)
            });

            if (response.ok) {
                this.showMessage('Pulse sent successfully! 🌿', 'success');
                e.target.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                
                // Reload pulses and red code after a moment
                setTimeout(() => {
                    this.loadPulses();
                    this.loadRedCode();
                }, 1000);
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Error sending pulse. Please try again.', 'error');
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
            this.showMessage('Error triggering reflection. Please try again.', 'error');
        } finally {
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }
    }

    initialize3DVisualization() {
        // Initialize the 3D visualization with a slight delay to ensure DOM is ready
        setTimeout(() => {
            this.threeDViz = new Euystacio3DVisualization();
            this.threeDViz.init();
            
            // Update visualization when new pulses arrive
            this.on3DVisualizationReady = () => {
                if (this.pulses) {
                    this.threeDViz.updatePulses(this.pulses);
                }
            };
        }, 500);
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
}

// Canvas-based 3D-like Visualization Class
class Euystacio3DVisualization {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.pulseParticles = [];
        this.animationId = null;
        this.isAnimating = true;
        this.camera = { x: 0, y: 0, z: 0, rotation: 0 };
        this.emotionColors = {
            'hope': '#4CAF50',
            'wonder': '#9C27B0',
            'peace': '#2196F3',
            'curiosity': '#FF9800',
            'concern': '#FF5722',
            'gratitude': '#FFD700',
            'excitement': '#E91E63',
            'contemplation': '#607D8B',
            'love': '#F44336',
            'harmony': '#8BC34A',
            'default': '#6BB6FF'
        };
        this.time = 0;
    }

    init() {
        const container = document.getElementById('three-js-container');
        const canvas = document.getElementById('visualization-canvas');
        if (!container || !canvas) {
            console.warn('3D container or canvas not found');
            return;
        }

        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Set canvas size
        this.resizeCanvas();
        
        // Remove loading message after initialization
        setTimeout(() => {
            const loading = container.querySelector('.loading-3d');
            if (loading) loading.style.display = 'none';
        }, 1000);

        // Create initial placeholder data
        this.createPlaceholderPulses();
        
        // Start animation loop
        this.animate();

        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
        
        console.log('Canvas-based 3D Visualization initialized successfully');
    }

    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.offsetWidth - 4; // Account for border
        this.canvas.height = container.offsetHeight - 4;
    }

    createPlaceholderPulses() {
        const placeholderData = [
            { emotion: 'hope', intensity: 0.8, timestamp: new Date(Date.now() - 3600000).toISOString() },
            { emotion: 'wonder', intensity: 0.6, timestamp: new Date(Date.now() - 1800000).toISOString() },
            { emotion: 'peace', intensity: 0.7, timestamp: new Date().toISOString() },
            { emotion: 'gratitude', intensity: 0.9, timestamp: new Date(Date.now() - 900000).toISOString() },
            { emotion: 'curiosity', intensity: 0.5, timestamp: new Date(Date.now() - 2700000).toISOString() }
        ];
        
        this.updatePulses(placeholderData);
    }

    updatePulses(pulses) {
        this.pulseParticles = [];

        if (!pulses || pulses.length === 0) {
            this.createPlaceholderPulses();
            return;
        }

        pulses.forEach((pulse, index) => {
            this.createPulseParticle(pulse, index);
        });
    }

    createPulseParticle(pulse, index) {
        const timeOffset = this.getTimeOffset(pulse.timestamp);
        const emotionZ = this.getEmotionZPosition(pulse.emotion);
        
        const particle = {
            x: timeOffset,
            y: (pulse.intensity || 0.5) * 200 - 100,
            z: emotionZ,
            originalY: (pulse.intensity || 0.5) * 200 - 100,
            size: (pulse.intensity || 0.5) * 30 + 10,
            color: this.emotionColors[pulse.emotion] || this.emotionColors.default,
            emotion: pulse.emotion,
            intensity: pulse.intensity,
            timestamp: pulse.timestamp,
            animationOffset: Math.random() * Math.PI * 2,
            connections: []
        };

        // Add connection to previous particle
        if (this.pulseParticles.length > 0) {
            const prevParticle = this.pulseParticles[this.pulseParticles.length - 1];
            particle.connections.push(prevParticle);
        }

        this.pulseParticles.push(particle);
    }

    getTimeOffset(timestamp) {
        if (!timestamp) return Math.random() * 200 - 100;
        
        const now = new Date();
        const pulseTime = new Date(timestamp);
        const hoursDiff = (now - pulseTime) / (1000 * 60 * 60);
        return Math.max(-100, Math.min(100, (hoursDiff - 2) * 30));
    }

    getEmotionZPosition(emotion) {
        const emotions = Object.keys(this.emotionColors);
        const index = emotions.indexOf(emotion);
        if (index === -1) return 0;
        
        return (index - emotions.length / 2) * 20;
    }

    project3D(x, y, z) {
        // Simple 3D to 2D projection
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Apply rotation
        const cos = Math.cos(this.camera.rotation);
        const sin = Math.sin(this.camera.rotation);
        
        const rotatedX = x * cos - z * sin;
        const rotatedZ = x * sin + z * cos;
        
        // Perspective projection
        const fov = 300;
        const distance = fov / (fov + rotatedZ + 200);
        
        return {
            x: centerX + rotatedX * distance,
            y: centerY + y * distance,
            size: distance,
            depth: rotatedZ
        };
    }

    drawParticle(particle, projected) {
        const { x, y, size } = projected;
        const radius = particle.size * size;
        
        // Create gradient for 3D effect
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, radius);
        gradient.addColorStop(0, particle.color);
        gradient.addColorStop(1, particle.color + '40'); // Add transparency
        
        // Draw main sphere
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Add highlight for 3D effect
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        this.ctx.beginPath();
        this.ctx.arc(x - radius * 0.3, y - radius * 0.3, radius * 0.3, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw emotion label
        if (radius > 15) {
            this.ctx.fillStyle = '#333';
            this.ctx.font = `${Math.max(12, radius * 0.3)}px Inter, sans-serif`;
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(particle.emotion, x, y);
        }
    }

    drawConnections(particle, projected) {
        particle.connections.forEach(connectedParticle => {
            const connectedProjected = this.project3D(
                connectedParticle.x,
                connectedParticle.y + Math.sin(this.time + connectedParticle.animationOffset) * 10,
                connectedParticle.z
            );
            
            this.ctx.strokeStyle = 'rgba(136, 136, 136, 0.3)';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(projected.x, projected.y);
            this.ctx.lineTo(connectedProjected.x, connectedProjected.y);
            this.ctx.stroke();
        });
    }

    animate() {
        if (!this.isAnimating || !this.ctx) return;
        
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update time and camera
        this.time += 0.02;
        this.camera.rotation += 0.005;
        
        // Sort particles by depth for proper rendering order
        const projectedParticles = this.pulseParticles.map(particle => {
            const animatedY = particle.originalY + Math.sin(this.time + particle.animationOffset) * 10;
            const projected = this.project3D(particle.x, animatedY, particle.z);
            return { particle: { ...particle, y: animatedY }, projected };
        });
        
        projectedParticles.sort((a, b) => b.projected.depth - a.projected.depth);
        
        // Draw connections first
        projectedParticles.forEach(({ particle, projected }) => {
            this.drawConnections(particle, projected);
        });
        
        // Draw particles
        projectedParticles.forEach(({ particle, projected }) => {
            this.drawParticle(particle, projected);
        });
        
        // Draw grid/axes for reference
        this.drawGrid();
    }

    drawGrid() {
        this.ctx.strokeStyle = 'rgba(204, 204, 204, 0.3)';
        this.ctx.lineWidth = 1;
        
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Draw horizontal lines
        for (let i = -2; i <= 2; i++) {
            const y = centerY + i * 50;
            this.ctx.beginPath();
            this.ctx.moveTo(50, y);
            this.ctx.lineTo(this.canvas.width - 50, y);
            this.ctx.stroke();
        }
        
        // Draw vertical lines
        for (let i = -3; i <= 3; i++) {
            const x = centerX + i * 60;
            this.ctx.beginPath();
            this.ctx.moveTo(x, 50);
            this.ctx.lineTo(x, this.canvas.height - 50);
            this.ctx.stroke();
        }
    }

    resetView() {
        this.camera.rotation = 0;
        this.camera.x = 0;
        this.camera.y = 0;
        this.camera.z = 0;
    }

    toggleAnimation() {
        this.isAnimating = !this.isAnimating;
        if (this.isAnimating) {
            this.animate();
        } else if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        return this.isAnimating;
    }

    handleResize() {
        this.resizeCanvas();
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new EuystacioDashboard();
    
    // Add self-awareness button functionality
    document.getElementById('self-awareness-btn')?.addEventListener('click', async () => {
        const button = document.getElementById('self-awareness-btn');
        button.disabled = true;
        button.textContent = 'Activating...';
        
        try {
            const response = await fetch('/api/reflect');
            if (response.ok) {
                const reflection = await response.json();
                dashboard.showMessage('Self-awareness loop activated! 🧠✨', 'success');
                
                // Refresh reflections
                setTimeout(() => {
                    dashboard.loadReflections();
                }, 1000);
            }
        } catch (error) {
            dashboard.showMessage('Error activating self-awareness loop', 'error');
        } finally {
            button.disabled = false;
            button.textContent = 'Activate Self-Awareness Loop';
        }
    });

    // Add smooth scrolling for better navigation
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add loading indicators to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.classList.add('loading');
                setTimeout(() => this.classList.remove('loading'), 2000);
            }
        });
    });
});