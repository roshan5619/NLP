from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for consistent results
DetectorFactory.seed = 0

class LanguageDetector:
    def __init__(self):
        self.supported_languages = ['en', 'es', 'fr', 'de', 'hi', 'zh', 'ja', 'ar']
    
    def detect_language(self, text):
        try:
            detected_lang = detect(text)
            if detected_lang in self.supported_languages:
                return detected_lang
            return 'en'  # Default to English
        except LangDetectException:
            return 'en'
    
    def get_language_name(self, lang_code):
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'hi': 'Hindi',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic'
        }
        return language_names.get(lang_code, 'Unknown')