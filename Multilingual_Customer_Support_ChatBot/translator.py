from googletrans import Translator
import time

class TextTranslator:
    def __init__(self):
        self.translator = Translator()
    
    def translate_text(self, text, target_language='en', source_language='auto'):
        try:
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
            
            result = self.translator.translate(
                text, 
                dest=target_language, 
                src=source_language
            )
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def translate_to_english(self, text, source_language):
        return self.translate_text(text, target_language='en', source_language=source_language)
    
    def translate_from_english(self, text, target_language):
        return self.translate_text(text, target_language=target_language, source_language='en')