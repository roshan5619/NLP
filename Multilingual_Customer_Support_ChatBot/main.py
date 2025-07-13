import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

# Try to import modules with error handling
try:
    from app.models.nlp_processor import NLPProcessor
    from app.models.intent_classifier import IntentClassifier
    from app.utils.language_detector import LanguageDetector
    from app.utils.translator import TextTranslator
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure all required files are created and in the correct locations")
    # Create fallback classes to prevent crashes
    class NLPProcessor:
        def __init__(self):
            pass
        def tokenize_and_lemmatize(self, text):
            return text.split()
        def extract_entities(self, text):
            return []
        def get_sentiment(self, text):
            return 'neutral'
    
    class IntentClassifier:
        def __init__(self):
            pass
        def predict_intent(self, text):
            return 'greeting', 0.5
        def get_response(self, intent):
            return "Hello! I'm still learning. Please make sure all files are properly set up."
    
    class LanguageDetector:
        def __init__(self):
            pass
        def detect_language(self, text):
            return 'en'
    
    class TextTranslator:
        def __init__(self):
            pass
        def translate_to_english(self, text, source_language):
            return text
        def translate_from_english(self, text, target_language):
            return text

app = Flask(__name__, 
            template_folder='templates',
            static_folder='../static')
CORS(app)

# Initialize components with error handling
try:
    nlp_processor = NLPProcessor()
    intent_classifier = IntentClassifier()
    language_detector = LanguageDetector()
    translator = TextTranslator()
    print("✓ All components initialized successfully")
except Exception as e:
    print(f"✗ Error initializing components: {e}")
    print("Using fallback components")

class ChatBot:
    def __init__(self):
        self.conversation_history = []
        self.default_responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Farewell! Don't hesitate to reach out if you need help."
            ],
            'unknown': [
                "I'm sorry, I don't understand that. Could you please rephrase?",
                "I'm not sure what you mean. Can you try asking differently?",
                "I don't have information about that. How else can I help you?"
            ]
        }
    
    def process_message(self, message, user_language=None):
        try:
            # Detect language if not provided
            if not user_language or user_language == 'auto':
                user_language = language_detector.detect_language(message)
            
            # Translate to English for processing if needed
            english_message = message
            if user_language != 'en':
                english_message = translator.translate_to_english(message, user_language)
            
            # Process with NLP
            processed_text = nlp_processor.tokenize_and_lemmatize(english_message)
            entities = nlp_processor.extract_entities(english_message)
            sentiment = nlp_processor.get_sentiment(english_message)
            
            # Classify intent
            intent, confidence = intent_classifier.predict_intent(english_message)
            
            # Get response
            english_response = intent_classifier.get_response(intent)
            
            # Fallback to default responses if needed
            if not english_response or english_response == "I'm sorry, I don't understand that request.":
                if intent in self.default_responses:
                    import random
                    english_response = random.choice(self.default_responses[intent])
                else:
                    import random
                    english_response = random.choice(self.default_responses['unknown'])
            
            # Translate response back to user's language
            response = english_response
            if user_language != 'en':
                response = translator.translate_from_english(english_response, user_language)
            
            # Store conversation
            self.conversation_history.append({
                'user_message': message,
                'response': response,
                'language': user_language,
                'intent': intent,
                'confidence': confidence,
                'sentiment': sentiment
            })
            
            return {
                'response': response,
                'language': user_language,
                'intent': intent,
                'confidence': float(confidence),
                'sentiment': sentiment,
                'entities': entities
            }
            
        except Exception as e:
            print(f"✗ Error processing message: {e}")
            return {
                'response': "I'm sorry, I encountered an error processing your message. Please try again.",
                'language': user_language or 'en',
                'intent': 'error',
                'confidence': 0.0,
                'sentiment': 'neutral',
                'entities': []
            }

# Initialize chatbot
chatbot = ChatBot()

@app.route('/')
def index():
    """Serve the main chat interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"✗ Error loading template: {e}")
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Multilingual Chatbot</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .error {{ color: red; }}
                .info {{ color: blue; }}
            </style>
        </head>
        <body>
            <h1>Multilingual Customer Support Chatbot</h1>
            <div class="error">Template file not found. Please create app/templates/index.html</div>
            <div class="info">
                <p>Basic chat interface:</p>
                <div id="chat"></div>
                <input type="text" id="message" placeholder="Type your message...">
                <button onclick="sendMessage()">Send</button>
            </div>
            <script>
                function sendMessage() {{
                    const message = document.getElementById('message').value;
                    fetch('/chat', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ message: message }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('chat').innerHTML += 
                            '<div>You: ' + message + '</div>' +
                            '<div>Bot: ' + data.response + '</div>';
                        document.getElementById('message').value = '';
                    }});
                }}
            </script>
        </body>
        </html>
        '''

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        user_language = data.get('language', None)
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if len(message) > 500:
            return jsonify({'error': 'Message too long. Please keep it under 500 characters.'}), 400
        
        result = chatbot.process_message(message, user_language)
        return jsonify(result)
    
    except Exception as e:
        print(f"✗ Chat error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'I apologize, but I encountered an error. Please try again.',
            'language': 'en',
            'intent': 'error',
            'confidence': 0.0,
            'sentiment': 'neutral',
            'entities': []
        }), 500

@app.route('/train', methods=['POST'])
def train_model():
    """Train the intent classification model"""
    try:
        intent_classifier.train_model()
        return jsonify({'message': 'Model trained successfully'})
    except Exception as e:
        print(f"✗ Training error: {e}")
        return jsonify({'error': f'Training failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'nlp_processor': 'initialized',
            'intent_classifier': 'initialized',
            'language_detector': 'initialized',
            'translator': 'initialized'
        }
    })

@app.route('/conversation-history')
def get_conversation_history():
    """Get conversation history"""
    return jsonify({
        'history': chatbot.conversation_history[-10:],  # Return last 10 messages
        'total_messages': len(chatbot.conversation_history)
    })

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    chatbot.conversation_history = []
    return jsonify({'message': 'Conversation history cleared'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print(f"📍 Current working directory: {os.getcwd()}")
    print(f"📍 Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    print("📍 Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)