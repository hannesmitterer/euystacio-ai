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

        // Contact modal functionality
        this.setupContactModal();
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

    async loadRedCode() {
        try {
            const response = await fetch('/api/red_code');
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
            const response = await fetch('/api/pulses');
            const pulses = await response.json();
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
            const response = await fetch('/api/tutors');
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutor nominations');
        }
    }

    displayTutors(tutors) {
        const container = document.getElementById('tutors-list');
        if (!container) return;

        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="loading">No tutor nominations yet.</div>';
            return;
        }

        container.innerHTML = tutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">${tutor.name || 'Anonymous Tutor'}</div>
                <div class="tutor-reason">${tutor.reason || 'Nominated for wisdom and guidance'}</div>
            </div>
        `).join('');
    }

    async loadReflections() {
        try {
            const response = await fetch('/api/reflections');
            const reflections = await response.json();
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

    setupContactModal() {
        const contactBtn = document.getElementById('contact-admin-btn');
        const contactModal = document.getElementById('contact-modal');
        const closeModal = document.getElementById('close-contact-modal');
        const cancelBtn = document.getElementById('cancel-contact');
        const contactForm = document.getElementById('contact-form');

        if (contactBtn && contactModal) {
            // Open modal
            contactBtn.addEventListener('click', () => {
                contactModal.classList.add('show');
                document.body.style.overflow = 'hidden';
            });

            // Close modal functions
            const closeModalFunc = () => {
                contactModal.classList.remove('show');
                document.body.style.overflow = 'auto';
                if (contactForm) {
                    contactForm.reset();
                }
                this.clearContactMessages();
            };

            // Close modal events
            if (closeModal) {
                closeModal.addEventListener('click', closeModalFunc);
            }
            if (cancelBtn) {
                cancelBtn.addEventListener('click', closeModalFunc);
            }

            // Close on outside click
            contactModal.addEventListener('click', (e) => {
                if (e.target === contactModal) {
                    closeModalFunc();
                }
            });

            // Close on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && contactModal.classList.contains('show')) {
                    closeModalFunc();
                }
            });

            // Handle form submission
            if (contactForm) {
                contactForm.addEventListener('submit', (e) => this.handleContactSubmission(e));
            }
        }
    }

    async handleContactSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const contactData = {
            name: formData.get('name').trim(),
            email: formData.get('email').trim(),
            message: formData.get('message').trim()
        };

        // Validate fields
        if (!contactData.name || !contactData.email || !contactData.message) {
            this.showContactMessage('Please fill in all fields', 'error');
            return;
        }

        if (!this.isValidEmail(contactData.email)) {
            this.showContactMessage('Please enter a valid email address', 'error');
            return;
        }

        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';

            // Try to send via backend API first
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(contactData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showContactMessage('Message sent successfully! Thank you for reaching out. 🌱', 'success');
                setTimeout(() => {
                    const modal = document.getElementById('contact-modal');
                    if (modal) {
                        modal.classList.remove('show');
                        document.body.style.overflow = 'auto';
                    }
                    event.target.reset();
                    this.clearContactMessages();
                }, 2000);
            } else {
                throw new Error('Backend API failed');
            }
        } catch (error) {
            console.log('Backend API failed, falling back to EmailJS');
            // Fallback to EmailJS for static hosting compatibility
            this.sendViaEmailJS(contactData, submitBtn, originalText, event.target);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    async sendViaEmailJS(contactData, submitBtn, originalText, form) {
        try {
            // EmailJS configuration for static hosting
            const emailData = {
                to_email: 'hannes.mitterer@gmail.com',
                from_name: contactData.name,
                from_email: contactData.email,
                message: `From: ${contactData.name} (${contactData.email})\n\nMessage:\n${contactData.message}\n\nSent from Euystacio Dashboard`,
                reply_to: contactData.email
            };

            // This would normally use EmailJS service
            // For now, we'll show a message with instructions
            this.showContactMessage(
                `Thanks for your message! Please email hannes.mitterer@gmail.com directly with your message:\n\nFrom: ${contactData.name}\nEmail: ${contactData.email}\nMessage: ${contactData.message}`,
                'info'
            );

            setTimeout(() => {
                const modal = document.getElementById('contact-modal');
                if (modal) {
                    modal.classList.remove('show');
                    document.body.style.overflow = 'auto';
                }
                form.reset();
                this.clearContactMessages();
            }, 5000);

        } catch (error) {
            console.error('EmailJS fallback failed:', error);
            this.showContactMessage('Unable to send message. Please email hannes.mitterer@gmail.com directly.', 'error');
        }
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    showContactMessage(message, type = 'info') {
        this.clearContactMessages();
        
        const modalBody = document.querySelector('.modal-body');
        if (!modalBody) return;

        const messageEl = document.createElement('div');
        messageEl.className = `contact-message ${type}`;
        messageEl.textContent = message;
        
        // Insert message at the top of modal body
        modalBody.insertBefore(messageEl, modalBody.firstChild);
    }

    clearContactMessages() {
        const messages = document.querySelectorAll('.contact-message');
        messages.forEach(msg => msg.remove());
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