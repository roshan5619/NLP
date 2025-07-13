import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

class IntentClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.intents = {}
        self.load_intents()
    
    def load_intents(self):
        try:
            with open('app/data/intents.json', 'r', encoding='utf-8') as f:
                self.intents = json.load(f)
        except FileNotFoundError:
            print("intents.json not found. Please create the file with training data.")
    
    def prepare_training_data(self):
        X = []
        y = []
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data.get('patterns', []):
                X.append(pattern)
                y.append(intent_name)
        
        return X, y
    
    def train_model(self):
        X, y = self.prepare_training_data()
        
        if not X:
            print("No training data available.")
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('svm', SVC(kernel='linear', probability=True))
        ])
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        
        # Save model
        self.save_model()
    
    def predict_intent(self, text, threshold=0.5):
        if not self.model:
            self.load_model()
        
        if not self.model:
            return 'unknown', 0.0
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba([text])[0]
        max_prob = np.max(probabilities)
        
        if max_prob < threshold:
            return 'unknown', max_prob
        
        predicted_intent = self.model.predict([text])[0]
        return predicted_intent, max_prob
    
    def save_model(self):
        if self.model:
            with open('app/models/intent_model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
    
    def load_model(self):
        try:
            with open('app/models/intent_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            print("Model not found. Training new model...")
            self.train_model()
    
    def get_response(self, intent):
        if intent in self.intents:
            responses = self.intents[intent].get('responses', ['I apologize, but I don\'t have a response for that.'])
            return np.random.choice(responses)
        return "I'm sorry, I don't understand that request."