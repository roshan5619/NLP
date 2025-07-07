# 🧠 Multi-Document Summarization using PageRank (TextRank)

This project demonstrates how to generate summaries from multiple documents using unsupervised techniques in NLP. The core of the approach is based on **PageRank**, originally used by Google for web ranking, now adapted to rank sentences by importance (TextRank). This method allows for efficient, extractive summarization of large document collections.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Notebook Summary](#notebook-summary)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Overview

In the age of information overload, automatic summarization helps distill key insights from large text corpora. This notebook focuses on:

- Loading and preprocessing multiple documents
- Building a similarity matrix of sentences
- Applying the **PageRank algorithm** to rank sentences
- Extracting top-ranked sentences as a coherent summary

Ideal for news aggregation, research paper summarization, or legal/document analysis systems.

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multidoc-pagerank-nlp.git
cd multidoc-pagerank-nlp
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
If requirements.txt is not included, install manually:
```
pip install numpy pandas networkx nltk scikit-learn matplotlib
```
📂 Getting Started

To run the notebook:

jupyter notebook

Then open: MultiDoc_&_PageRank_NLP.ipynb

Ensure that your text documents are available in the appropriate folder or as defined in the notebook.
📓 Notebook Summary

The notebook includes:

    Data Ingestion

        Load and parse multiple documents

        Sentence tokenization (using NLTK)

    Text Preprocessing

        Stopword removal

        Lowercasing, punctuation stripping

    Sentence Embedding & Similarity

        Bag-of-Words or TF-IDF vectorization

        Cosine similarity between sentences

    Graph Construction

        Sentences as nodes

        Similarity scores as edge weights

    PageRank for Ranking

        Apply NetworkX's PageRank to extract top N sentences

    Summary Generation

        Output ranked, concise summaries

⚙️ Technologies Used

    Python 3.x

    Jupyter Notebook

    NetworkX

    NLTK

    scikit-learn

    NumPy

    Pandas

    Matplotlib

✨ Use Cases

    News summarization engines

    Multi-document briefing tools

    Research paper digesters

    Legal/compliance report simplifiers

🤝 Contributing

Contributions are welcome!

    Found a bug? Open an issue.

    Want to improve the summarization technique (e.g. add BERT embeddings)? Submit a pull request!

📄 License

This project is licensed under the MIT License.
