# 😊 Emotion Detection using GloVe, CNN, and BiLSTM

This project demonstrates how to build an intelligent text classification model to detect emotions from short sentences using **pre-trained GloVe embeddings**, a **Convolutional Neural Network (CNN)**, and a **Bidirectional LSTM (BiLSTM)** layer. The model is trained to classify input text into one of several emotion categories, such as *joy*, *anger*, *sadness*, *fear*, etc.

---

## 🧠 Objective

To develop an emotion classification system using deep learning that can understand and predict the underlying emotion in a piece of text, combining the strengths of word embeddings (GloVe), CNNs for local feature detection, and BiLSTM for context-aware sequence modeling.

---

## 📦 Dataset

- Dataset used: **Emotion Dataset** (likely from Kaggle or a similar open-source source)
- Each sample consists of:
  - Input: Text sentence
  - Output: Emotion label (e.g., joy, anger, sadness, fear, love, surprise)
- The dataset is preprocessed to clean, tokenize, and prepare for embedding lookup.

---

## 🔍 Features Used

- **Word Embeddings**: Pre-trained [GloVe embeddings](https://nlp.stanford.edu/projects/glove/)
- **Tokenization**: Keras Tokenizer with padding for uniform input length
- **Embedding Matrix**: Constructed from GloVe for initializing the embedding layer

---

## 🏗️ Model Architecture
```
Embedding Layer (GloVe)
↓
1D Convolution (CNN) + MaxPooling
↓
Bidirectional LSTM
↓
Dense Layer + Dropout
↓
Softmax Output (Emotion classes)
```

- Loss Function: `categorical_crossentropy`
- Optimizer: `Adam`
- Evaluation: Accuracy

---

## 📊 Results

- Achieved high training and validation accuracy
- Model generalized well to unseen emotion inputs
- Performance visualization includes accuracy/loss curves

---

## 📈 Visualizations

- **Training vs Validation Accuracy**
- **Loss Curves**
- **Confusion Matrix** (optional)
- **Sample Predictions** with correct/incorrect emotion labels

---

## 🧪 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/emotion-detection-cnn-bilstm
   cd emotion-detection-cnn-bilstm
    ```
2. Install the required libraries:
```
    pip install -r requirements.txt
```
3. Launch the notebook:
```
    jupyter notebook Emotion_Detection_using_GloVe,_CNN,_and_BiLSTM.ipynb
```
