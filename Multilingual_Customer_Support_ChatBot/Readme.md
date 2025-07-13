# 🌍 Multilingual NLP Customer Support Chatbot

A powerful and extensible AI chatbot for customer support with multilingual capabilities, built using Flask, spaCy, NLTK, scikit-learn, and Google Translate. This chatbot can detect user language, classify intents, analyze sentiment, extract entities, and respond in the user's native language.

---

## 📌 Features

- ✅ **Multilingual Support**: Automatically detects and translates between 8+ languages.
- 🧠 **Intent Classification**: Custom-trained SVM model for identifying user intent.
- 💬 **Entity Recognition**: Extracts key data from user queries using spaCy.
- 😊 **Sentiment Analysis**: Determines emotional tone of customer messages.
- 🗣️ **Text Preprocessing**: Cleans, tokenizes, and lemmatizes user input.
- 🌐 **Web Interface**: Clean, responsive HTML/CSS/JavaScript frontend.
- 🔄 **Customizable Intents**: Easily add or update intent patterns and responses.

---

## 📂 Project Structure
```
multilingual-chatbot/
├── app/
│ ├── data/ # intents.json, responses.json
│ ├── models/ # NLPProcessor, IntentClassifier
│ ├── templates/ # index.html (UI)
│ ├── static/ # CSS & JS files
│ ├── utils/ # Translator and Language Detector
│ └── main.py # Flask application
├── config.py # App configuration
├── requirements.txt # Python dependencies
└── run.py # Entrypoint (optional)
```


---

## 🛠️ Setup Guide

### ✅ Prerequisites

- Python 3.8+
- pip (Python package manager)
- VS Code (recommended)
- Internet connection for downloading models

### 📦 Install Dependencies
```
# Clone the repository
git clone https://github.com/your-username/multilingual-chatbot.git
cd multilingual-chatbot

# Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

```
🔤 Download spaCy Models
```
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download de_core_news_sm

```
🚀 Running the Application
```
# Run the Flask app
python app/main.py
```
🧪 API Endpoints
POST /chat

Send a message to the chatbot.

Request:
```
{
  "message": "Hi, where is my order?",
  "language": "auto"
}
{
  "response": "I can help you track your order. Please provide your order number.",
  "language": "en",
  "intent": "order_status",
  "confidence": 0.92,
  "sentiment": "neutral",
  "entities": []
}

```
POST /train

Trigger model training manually.
```
curl -X POST http://localhost:5000/train
```
🧠 Training Your Model

To update or expand the chatbot's knowledge:

    Edit app/data/intents.json

    Add new patterns and responses

    Retrain:

  ```
curl -X POST http://localhost:5000/train
```
🧰 Troubleshooting
| Issue                 | Solution                                                     |
| --------------------- | ------------------------------------------------------------ |
| spaCy model not found | Run the `spacy download` commands above                      |
| Translation errors    | Ensure internet connectivity and retry                       |
| Model training fails  | Check formatting in `intents.json`                           |
| Port already in use   | Modify the port in `main.py` or stop the conflicting process |

🧭 Next Steps & Enhancements

    🔐 Add user authentication & session management

    🧠 Integrate BERT or multilingual transformer models

    📊 Analytics dashboard for chatbot performance

    ☁️ Dockerize and deploy on a cloud platform (e.g., AWS, GCP, Azure)

    💾 Store conversation history in a database

  📬 Contact

Feel free to reach out via issues or submit pull requests to contribute.

---

Let me know if you’d like this README adapted for publishing on a documentation site like ReadTheDocs, or if you'd like a `LICENSE`, `.gitignore`, or `Dockerfile` added.

