# 🗣️ Collocations in Natural Language Processing

This project explores how to identify **collocations** — pairs or groups of words that frequently occur together — using natural language processing techniques. Collocations like “strong tea” or “make a decision” carry meaning that isn’t obvious from individual words. This notebook introduces statistical and linguistic methods to extract and analyze such patterns from text.

---

## 📚 Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Notebook Breakdown](#notebook-breakdown)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Project Overview

Collocations are essential for understanding the structure and semantics of language. This notebook walks through:

- What collocations are and why they matter
- Loading and tokenizing text corpora
- Measuring collocation strength using:
  - Frequency
  - Pointwise Mutual Information (PMI)
  - t-test and chi-square
- Extracting bigrams and trigrams
- Visualizing common collocations

The project is educational, compact, and ideal for those learning NLP fundamentals.

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nlp-collocations.git
cd nlp-collocations
```
2. (Optional) Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
Or manually:
```
pip install nltk matplotlib pandas
```
📂 Getting Started

To run the notebook:

jupyter notebook

Then open: Collocations.ipynb

📌 Tip: Run the following to download required NLTK datasets if prompted:
```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')  # if you're using a sample corpus
```
🧾 Notebook Breakdown

Here's a quick summary of what the notebook covers:

    Introduction to Collocations

        What they are and examples

    Corpus Preparation

        Load and clean raw text

        Tokenization and stopword removal

    Collocation Extraction

        Use of nltk.collocations.BigramAssocMeasures and TrigramAssocMeasures

        PMI, t-test, chi-squared scores

    Filtering and Ranking

        Thresholds for frequency and scores

        Sorting and displaying top results

    Visualization

        Frequency distribution plots

        Word pair networks (optional)

⚙️ Technologies Used

    Python 3.x

    NLTK — Natural Language Toolkit

    Matplotlib

    Jupyter Notebook

    Pandas (if used for tabular analysis)

✨ Use Cases

    Language modeling and generation

    Machine translation

    Grammar checking and correction

    Lexicographic studies

🤝 Contributing

Contributions are welcome!

    Found a bug or typo? Open an issue.

    Have a new collocation technique? Submit a pull request.

    Want to apply this to a different corpus (e.g., news, tweets)? Let's collaborate!
