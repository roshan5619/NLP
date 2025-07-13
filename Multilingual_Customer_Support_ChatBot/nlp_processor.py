import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class NLPProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.spacy_models = {
            'en': 'en_core_web_sm',
            'es': 'es_core_news_sm',
            'fr': 'fr_core_news_sm',
            'de': 'de_core_news_sm'
        }
        self.nlp_models = {}
        self.load_spacy_models()
    
    def load_spacy_models(self):
        for lang, model_name in self.spacy_models.items():
            try:
                self.nlp_models[lang] = spacy.load(model_name)
            except OSError:
                print(f"Warning: {model_name} not found. Install with: python -m spacy download {model_name}")
    
    def clean_text(self, text):
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize_and_lemmatize(self, text, language='en'):
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = word_tokenize(cleaned_text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        
        # Lemmatize
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return lemmatized_tokens
    
    def extract_entities(self, text, language='en'):
        if language in self.nlp_models:
            doc = self.nlp_models[language](text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            return entities
        return []
    
    def get_sentiment(self, text, language='en'):
        # Simple sentiment analysis based on keywords
        positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied', 'love', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'disappointed', 'problem']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'