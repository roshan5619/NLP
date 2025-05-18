# 🎬 IMDB Movie Review Sentiment Analysis using LSTM

This project demonstrates the use of **Long Short-Term Memory (LSTM)** networks for binary sentiment classification of movie reviews from the IMDB dataset. The goal is to predict whether a movie review expresses a positive or negative sentiment.

---

## 📌 Objective

To classify IMDB movie reviews into **positive** or **negative** categories using an LSTM-based deep learning model trained on preprocessed review text.

---

## 🧰 Tech Stack

- Python 3.x
- TensorFlow / Keras
- NLTK
- NumPy, Pandas, Matplotlib
- IMDB Dataset (from `keras.datasets.imdb`)

---

## 🧪 Features

- Word-level tokenization and padding for uniform sequence lengths.
- LSTM-based architecture to capture temporal dependencies in text.
- Validation using accuracy and loss metrics.
- Real-time testing on user-input movie reviews (optional).

---

## 🧼 Data Preprocessing

- The dataset is already pre-tokenized via `keras.datasets.imdb`.
- Reviews are converted into integer sequences.
- Padding is applied to a uniform length (typically 200 or 500 tokens).

---

## 🏗️ Model Architecture

```text
Embedding Layer
↓
LSTM Layer
↓
Dense Layer (with ReLU)
↓
Output Layer (with Sigmoid)

```
Clone the repository:

```
    git clone https://github.com/your-username/imdb-sentiment-lstm.git
    cd imdb-sentiment-lstm
```
Install dependencies:
```
    pip install -r requirements.txt
```
Run the notebook:

    jupyter notebook IMDB_Sentiment_using_LSTM_FDP.ipynb

