# 🧠 Word Sense Disambiguation (WSD) using Lesk Algorithm

This project demonstrates how to perform **Word Sense Disambiguation** using the classic **Lesk algorithm** provided by the NLTK library. WSD helps determine the correct meaning of a word based on its context in a sentence.

---

## 📌 Overview

**Word Sense Disambiguation (WSD)** is the process of identifying the correct sense of a word when it has multiple meanings (polysemy). For example:

* **Bank** could mean a *financial institution* or the *side of a river*.
* **Bat** could refer to an *animal* or a *sports tool*.

This project uses the **Lesk algorithm**, which selects the sense of a word that shares the most words in common with the context.

---

## 🛠️ Tech Stack

* **Python 3.x**
* **NLTK (Natural Language Toolkit)**

---

## 📦 Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/wsd-lesk.git
   cd wsd-lesk
   ```
2. Install Dependendencies:

   ```
   pip install nltk

   ```
3. Download NLTK Resources:

   ```bash
   import nltk
   nltk.download('wordnet')
   nltk.download('omw-1.4')
   nltk.download('punkt')

   ```
