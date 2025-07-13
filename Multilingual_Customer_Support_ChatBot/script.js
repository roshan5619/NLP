// static/js/script.js

class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.languageSelect = document.getElementById('languageSelect');
        this.detectedLanguage = document.getElementById('detectedLanguage');
        this.lastIntent = document.getElementById('lastIntent');
        this.confidence = document.getElementById('confidence');
        
        this.isTyping = false;
        this.conversationHistory = [];
        
        this.init();
    }
    
    init() {
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
        
        // Language selector
        this.languageSelect.addEventListener('change', () => {
            this.updateLanguageDisplay();
        });
        
        // Focus on input
        this.messageInput.focus();
        
        // Initialize display
        this.updateLanguageDisplay();
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Send message to backend
        try {
            const response = await this.sendToBackend(message);
            this.hideTypingIndicator();
            
            if (response.error) {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', 'error');
            } else {
                this.addMessage(response.response, 'bot');
                this.updateChatInfo(response);
            }
        } catch (error) {
            this.hideTypingIndicator();
            console.error('Error:', error);
            this.addMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot', 'error');
        }
    }
    
    async sendToBackend(message) {
        const selectedLanguage = this.languageSelect.value;
        const requestBody = {
            message: message,
            language: selectedLanguage === 'auto' ? null : selectedLanguage
        };
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        return await response.json();
    }
    
    addMessage(text, sender, type = 'normal') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? 'U' : 'B';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (type === 'error') {
            messageContent.classList.add('error-message');
        } else if (type === 'success') {
            messageContent.classList.add('success-message');
        }
        
        messageContent.textContent = text;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in conversation history
        this.conversationHistory.push({
            text: text,
            sender: sender,
            timestamp: new Date().toISOString(),
            type: type
        });
        
        // Animate message
        this.animateMessage(messageDiv);
    }
    
    animateMessage(messageDiv) {
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 100);
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        this.sendButton.disabled = true;
        this.sendButton.innerHTML = '<div class="loading"></div>';
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = 'B';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'message-content';
        typingContent.innerHTML = `
            <span>Bot is typing</span>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(typingContent);
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        this.sendButton.disabled = false;
        this.sendButton.textContent = 'Send';
        
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    updateChatInfo(response) {
        // Update detected language
        const languageName = this.getLanguageName(response.language);
        this.detectedLanguage.textContent = `Language: ${languageName}`;
        
        // Update intent
        this.lastIntent.textContent = `Intent: ${response.intent}`;
        
        // Update confidence with color coding
        const confidenceValue = (response.confidence * 100).toFixed(1);
        this.confidence.textContent = `Confidence: ${confidenceValue}%`;
        
        // Color code confidence
        this.confidence.className = '';
        if (response.confidence >= 0.8) {
            this.confidence.classList.add('confidence-high');
        } else if (response.confidence >= 0.5) {
            this.confidence.classList.add('confidence-medium');
        } else {
            this.confidence.classList.add('confidence-low');
        }
        
        // Update sentiment if available
        if (response.sentiment) {
            const sentimentSpan = document.createElement('span');
            sentimentSpan.textContent = ` (${response.sentiment})`;
            sentimentSpan.className = `sentiment-${response.sentiment}`;
            this.lastIntent.appendChild(sentimentSpan);
        }
    }
    
    getLanguageName(langCode) {
        const languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'hi': 'Hindi',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic'
        };
        return languages[langCode] || langCode;
    }
    
    updateLanguageDisplay() {
        const selected = this.languageSelect.value;
        if (selected === 'auto') {
            this.detectedLanguage.textContent = 'Language: Auto-detect';
        } else {
            this.detectedLanguage.textContent = `Language: ${this.getLanguageName(selected)}`;
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    // Utility methods
    clearChat() {
        this.chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">B</div>
                <div class="message-content">
                    Hello! I'm your multilingual customer support assistant. How can I help you today?
                </div>
            </div>
        `;
        this.conversationHistory = [];
        this.resetChatInfo();
    }
    
    resetChatInfo() {
        this.lastIntent.textContent = 'Intent: -';
        this.confidence.textContent = 'Confidence: -';
        this.confidence.className = '';
        this.updateLanguageDisplay();
    }
    
    exportConversation() {
        const conversation = {
            timestamp: new Date().toISOString(),
            messages: this.conversationHistory
        };
        
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(conversation, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "conversation.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }
    
    // Voice input support (if available)
    startVoiceInput() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = this.languageSelect.value === 'auto' ? 'en-US' : this.getVoiceLanguage();
            
            recognition.onstart = () => {
                this.messageInput.placeholder = 'Listening...';
                this.sendButton.innerHTML = '🎤';
                this.sendButton.disabled = true;
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.messageInput.value = transcript;
                this.messageInput.focus();
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.resetVoiceInput();
            };
            
            recognition.onend = () => {
                this.resetVoiceInput();
            };
            
            recognition.start();
        } else {
            alert('Speech recognition not supported in this browser.');
        }
    }
    
    resetVoiceInput() {
        this.messageInput.placeholder = 'Type your message...';
        this.sendButton.textContent = 'Send';
        this.sendButton.disabled = false;
    }
    
    getVoiceLanguage() {
        const voiceLanguages = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'hi': 'hi-IN',
            'zh': 'zh-CN',
            'ja': 'ja-JP',
            'ar': 'ar-SA'
        };
        return voiceLanguages[this.languageSelect.value] || 'en-US';
    }
}

// Enhanced features
class ChatBotEnhanced extends ChatBot {
    constructor() {
        super();
        this.initEnhancedFeatures();
    }
    
    initEnhancedFeatures() {
        // Add keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to send message
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.sendMessage();
            }
            
            // Ctrl/Cmd + L to clear chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                this.clearChat();
            }
            
            // Ctrl/Cmd + E to export conversation
            if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                e.preventDefault();
                this.exportConversation();
            }
        });
        
        // Add context menu for additional options
        this.chatMessages.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showContextMenu(e.pageX, e.pageY);
        });
        
        // Auto-save conversation to localStorage
        this.loadConversationFromStorage();
        setInterval(() => this.saveConversationToStorage(), 30000); // Save every 30 seconds
    }
    
    showContextMenu(x, y) {
        // Remove existing context menu
        const existingMenu = document.getElementById('contextMenu');
        if (existingMenu) existingMenu.remove();
        
        const menu = document.createElement('div');
        menu.id = 'contextMenu';
        menu.style.cssText = `
            position: fixed;
            top: ${y}px;
            left: ${x}px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            min-width: 150px;
        `;
        
        const menuItems = [
            { text: 'Clear Chat', action: () => this.clearChat() },
            { text: 'Export Conversation', action: () => this.exportConversation() },
            { text: 'Train Model', action: () => this.trainModel() }
        ];
        
        menuItems.forEach(item => {
            const menuItem = document.createElement('div');
            menuItem.textContent = item.text;
            menuItem.style.cssText = `
                padding: 10px 15px;
                cursor: pointer;
                border-bottom: 1px solid #eee;
            `;
            menuItem.addEventListener('click', () => {
                item.action();
                menu.remove();
            });
            menuItem.addEventListener('mouseenter', () => {
                menuItem.style.backgroundColor = '#f5f5f5';
            });
            menuItem.addEventListener('mouseleave', () => {
                menuItem.style.backgroundColor = 'white';
            });
            menu.appendChild(menuItem);
        });
        
        document.body.appendChild(menu);
        
        // Remove menu when clicking elsewhere
        setTimeout(() => {
            document.addEventListener('click', () => menu.remove(), { once: true });
        }, 100);
    }
    
    async trainModel() {
        try {
            this.addMessage('Training model... This may take a moment.', 'bot', 'normal');
            
            const response = await fetch('/train', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.addMessage(`Training failed: ${result.error}`, 'bot', 'error');
            } else {
                this.addMessage('Model trained successfully!', 'bot', 'success');
            }
        } catch (error) {
            this.addMessage('Training failed. Please try again.', 'bot', 'error');
        }
    }
    
    saveConversationToStorage() {
        try {
            const conversationData = {
                history: this.conversationHistory,
                timestamp: new Date().toISOString()
            };
            // Note: localStorage is not available in Claude artifacts, 
            // but this would work in a real browser environment
            // localStorage.setItem('chatbotConversation', JSON.stringify(conversationData));
        } catch (error) {
            console.warn('Could not save conversation to storage:', error);
        }
    }
    
    loadConversationFromStorage() {
        try {
            // Note: localStorage is not available in Claude artifacts,
            // but this would work in a real browser environment
            // const saved = localStorage.getItem('chatbotConversation');
            // if (saved) {
            //     const data = JSON.parse(saved);
            //     this.conversationHistory = data.history || [];
            //     this.reconstructChatFromHistory();
            // }
        } catch (error) {
            console.warn('Could not load conversation from storage:', error);
        }
    }
    
    reconstructChatFromHistory() {
        this.chatMessages.innerHTML = '';
        
        // Add welcome message
        this.addMessage('Hello! I\'m your multilingual customer support assistant. How can I help you today?', 'bot');
        
        // Reconstruct conversation
        this.conversationHistory.forEach(msg => {
            if (msg.text && msg.sender) {
                this.addMessage(msg.text, msg.sender, msg.type);
            }
        });
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatBotEnhanced();
    
    // Add help tooltip
    const helpTooltip = document.createElement('div');
    helpTooltip.innerHTML = `
        <div style="position: fixed; bottom: 20px; right: 20px; background: #4facfe; color: white; padding: 10px; border-radius: 20px; cursor: help; z-index: 1000;" title="Keyboard shortcuts: Ctrl+Enter (send), Ctrl+L (clear), Ctrl+E (export), Right-click for menu">
            ?
        </div>
    `;
    document.body.appendChild(helpTooltip);
});

// Add some utility functions for potential future use
const ChatUtils = {
    formatTime: (timestamp) => {
        return new Date(timestamp).toLocaleTimeString();
    },
    
    formatDate: (timestamp) => {
        return new Date(timestamp).toLocaleDateString();
    },
    
    sanitizeHtml: (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    copyToClipboard: (text) => {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    },
    
    detectMobile: () => {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Message formatting utilities
const MessageFormatter = {
    formatLinks: (text) => {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
    },
    
    formatEmails: (text) => {
        const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/g;
        return text.replace(emailRegex, '<a href="mailto:$1">$1</a>');
    },
    
    formatPhoneNumbers: (text) => {
        const phoneRegex = /(\+?1?-?\.?\s?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})/g;
        return text.replace(phoneRegex, '<a href="tel:$1">$1</a>');
    },
    
    formatOrderNumbers: (text) => {
        const orderRegex = /(#[A-Z0-9]{6,})/g;
        return text.replace(orderRegex, '<strong>$1</strong>');
    },
    
    formatAll: (text) => {
        let formatted = text;
        formatted = MessageFormatter.formatLinks(formatted);
        formatted = MessageFormatter.formatEmails(formatted);
        formatted = MessageFormatter.formatPhoneNumbers(formatted);
        formatted = MessageFormatter.formatOrderNumbers(formatted);
        return formatted;
    }
};

// Analytics and tracking
const ChatAnalytics = {
    sessionStart: Date.now(),
    messageCount: 0,
    languageUsage: {},
    intentCounts: {},
    
    trackMessage: (language, intent, confidence) => {
        ChatAnalytics.messageCount++;
        
        // Track language usage
        if (language) {
            ChatAnalytics.languageUsage[language] = (ChatAnalytics.languageUsage[language] || 0) + 1;
        }
        
        // Track intent usage
        if (intent) {
            ChatAnalytics.intentCounts[intent] = (ChatAnalytics.intentCounts[intent] || 0) + 1;
        }
        
        // Track confidence levels
        if (confidence !== undefined) {
            const confidenceLevel = confidence >= 0.8 ? 'high' : confidence >= 0.5 ? 'medium' : 'low';
            ChatAnalytics.confidenceLevels = ChatAnalytics.confidenceLevels || {};
            ChatAnalytics.confidenceLevels[confidenceLevel] = (ChatAnalytics.confidenceLevels[confidenceLevel] || 0) + 1;
        }
    },
    
    getSessionStats: () => {
        const sessionDuration = Date.now() - ChatAnalytics.sessionStart;
        return {
            duration: sessionDuration,
            messageCount: ChatAnalytics.messageCount,
            languageUsage: ChatAnalytics.languageUsage,
            intentCounts: ChatAnalytics.intentCounts,
            confidenceLevels: ChatAnalytics.confidenceLevels || {}
        };
    },
    
    exportStats: () => {
        const stats = ChatAnalytics.getSessionStats();
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(stats, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "chat-analytics.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }
};

// Theme manager
const ThemeManager = {
    currentTheme: 'light',
    
    init: () => {
        // Check for saved theme preference or default to light
        const savedTheme = localStorage.getItem('chatbotTheme') || 'light';
        ThemeManager.setTheme(savedTheme);
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!localStorage.getItem('chatbotTheme')) {
                    ThemeManager.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    },
    
    setTheme: (theme) => {
        ThemeManager.currentTheme = theme;
        document.body.className = theme === 'dark' ? 'dark-theme' : '';
        localStorage.setItem('chatbotTheme', theme);
    },
    
    toggleTheme: () => {
        const newTheme = ThemeManager.currentTheme === 'light' ? 'dark' : 'light';
        ThemeManager.setTheme(newTheme);
    }
};

// Notification manager
const NotificationManager = {
    requestPermission: () => {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    },
    
    showNotification: (title, message, options = {}) => {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/static/images/bot-icon.png',
                ...options
            });
        }
    },
    
    notifyNewMessage: (message) => {
        if (document.hidden) { // Only notify if page is not visible
            NotificationManager.showNotification('New Message', message);
        }
    }
};

// Enhanced error handling
const ErrorHandler = {
    logError: (error, context) => {
        console.error('ChatBot Error:', error, 'Context:', context);
        
        // You could send this to an error tracking service
        // ErrorTrackingService.logError(error, context);
    },
    
    handleNetworkError: (error) => {
        ErrorHandler.logError(error, 'Network');
        return 'Network error. Please check your connection and try again.';
    },
    
    handleAPIError: (error) => {
        ErrorHandler.logError(error, 'API');
        return 'Service temporarily unavailable. Please try again in a moment.';
    },
    
    handleUnknownError: (error) => {
        ErrorHandler.logError(error, 'Unknown');
        return 'An unexpected error occurred. Please refresh the page and try again.';
    }
};

// Performance monitoring
const PerformanceMonitor = {
    measurements: {},
    
    start: (name) => {
        PerformanceMonitor.measurements[name] = performance.now();
    },
    
    end: (name) => {
        if (PerformanceMonitor.measurements[name]) {
            const duration = performance.now() - PerformanceMonitor.measurements[name];
            console.log(`${name} took ${duration.toFixed(2)}ms`);
            delete PerformanceMonitor.measurements[name];
            return duration;
        }
    },
    
    measure: (name, func) => {
        PerformanceMonitor.start(name);
        const result = func();
        PerformanceMonitor.end(name);
        return result;
    }
};

// Initialize all managers when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    NotificationManager.requestPermission();
    
    // Add theme toggle button
    const themeToggle = document.createElement('button');
    themeToggle.innerHTML = '🌙';
    themeToggle.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: #4facfe;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s ease;
    `;
    themeToggle.addEventListener('click', () => {
        ThemeManager.toggleTheme();
        themeToggle.innerHTML = ThemeManager.currentTheme === 'dark' ? '☀️' : '🌙';
    });
    document.body.appendChild(themeToggle);
});

// Export for global access
window.ChatUtils = ChatUtils;
window.MessageFormatter = MessageFormatter;
window.ChatAnalytics = ChatAnalytics;
window.ThemeManager = ThemeManager;
window.NotificationManager = NotificationManager;
window.ErrorHandler = ErrorHandler;
window.PerformanceMonitor = PerformanceMonitor;