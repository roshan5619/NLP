# Twitter Sentiment Analysis Using Convolutional Neural Networks (CNN)

This project demonstrates how to perform sentiment analysis on Twitter data using a deep learning model based on Convolutional Neural Networks (CNNs). The goal is to classify tweets into three categories: Positive, Negative, and Neutral.

## Objective

To classify tweets as positive, negative, or neutral based on their text content using a CNN-based model.

## Tech Stack

- **Python 3.x**
- **TensorFlow/Keras**
- **NLTK**
- **Pandas, NumPy**

## Dataset

The dataset used in this project is preprocessed and structured similarly to the Sentiment140 dataset. It contains tweets labeled as:

- `0`: Negative
- `2`: Neutral
- `4`: Positive

These labels are internally mapped to 0 (Negative), 1 (Neutral), and 2 (Positive).

## Data Preprocessing

The text data is cleaned and tokenized using NLTK. Stopwords are removed, and the sequences are padded to ensure uniform input length. Tokenization is done using the `Tokenizer` from Keras, and padding is applied to a maximum length of 50.

## Model

The deep learning model is a Convolutional Neural Network (CNN) that processes the text data. The architecture is as follows:

1. **Embedding Layer**: Converts word indices into dense vectors of fixed size.
2. **Convolutional Layers**: Multiple 1D convolution layers with ReLU activation.
3. **Max Pooling Layers**: Used to reduce the spatial dimensions.
4. **Global Max Pooling**: To select the most important features.
5. **Dense Layer**: Outputs the final prediction using the softmax activation function for multi-class classification.

## Training

The model is trained using the sparse categorical cross-entropy loss function and the Adam optimizer. The dataset is split into training and testing sets, and the model is trained for 5 epochs with a batch size of 100.

## Setup Instructions

To run this project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/twitter-sentiment-analysis-cnn.git
2. Install the required dependencies:
```
    pip install -r requirements.txt
```
3.Download the dataset or use the provided one.

Run the project:
```
    jupyter notebook
