# 🧠 Emotion Detection from Text using Logistic Regression

This repository contains a simple machine learning project that classifies emotions from short text messages. It uses **TF-IDF vectorization** for feature extraction and **Logistic Regression** for classification.

---

## 📌 Project Overview

The goal of this project is to build a basic emotion classifier that can predict emotions such as:

* Happy
* Sad
* Angry
* Excited
* Scared
* Frustrated
* Anxious

This is a foundational text classification project and serves as a stepping stone for more advanced Natural Language Processing (NLP) applications.

---

## 🛠️ Tech Stack

* **Python 3.x**
* **pandas** – For data manipulation
* **numpy** – For basic numerical operations
* **scikit-learn** – For TF-IDF vectorization, model training, and evaluation

---

## 📁 Dataset

A small custom dataset of 8 text samples is used, each labeled with one of the target emotions.

Example:

| Text                                        | Emotion    |
| ------------------------------------------- | ---------- |
| I am so happy today!                        | happy      |
| This is so sad...                           | sad        |
| I am very angry right now.                  | angry      |
| Feeling excited about the trip!             | excited    |
| I am so scared of the exam tomorrow.        | scared     |
| What a wonderful day!                       | happy      |
| I am extremely frustrated with the service. | frustrated |
| Feeling very anxious about the results.     | anxious    |

> You can extend this dataset by adding more emotion-labeled text entries to improve accuracy and generalization.

---

## 🚀 How to Run

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/emotion-detector-logistic.git
   cd emotion-detector-logistic
   ```
2. Install Dependencies:

   ```
   pip install pandas scikit-learn numpy
   ```
3. Run the program:

   ```bash
    python emotion_detection.py
   ```
