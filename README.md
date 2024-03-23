# NLP Specific Projects

### Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#requirements)


### Introduction
This repository contains two key projects focusing on Natural Language Processing (NLP):

1. **Character Text Generation**: Training a character language model to predict the next character in a sequence and generate new text sequences. (Nov-Dec 2023)
2. **Text Pre-processing and Features**: Exploring text pre-processing techniques and feature extraction methods, including Bag of Words (BoW), TF-IDF, and manual word embeddings. (Nov-Dec 2023)

### Installation
To use the projects in this repository, ensure you have Python installed along with Jupyter Notebooks or JupyterLab. Follow these steps:

```bash
# Clone my repo
git clone <repository-url>

# Go to the repository directory
cd NLP-Projects

# Install necessary Python dependencies
pip install numpy matplotlib keras nltk scikit-learn
```
Additional Setup <br>
For Text Pre-processing and Features, you may need to download additional NLTK data:

```python
import nltk
nltk.download('punkt')
``` 


### Usage
**Character Text Generation:**
This notebook guides you through the process of training a LSTM model for character-based text generation using Keras. It includes:

* Data preparation and preprocessing.
* Model architecture and training.
* Generating text with different strategies like temperature sampling and beam search.

**Text Pre-processing and Features:**
This notebook explores various text pre-processing methods and features extraction techniques covering:

* Bag of Words and TF-IDF representations.
* Using Scikit-learn and NLTK for text processing.
* Manual extraction of word embeddings through dimension reduction.

### Requirements
- Python 3.x
- Jupyter Notebook or JupyterLab
- numpy
- matplotlib
- keras
- nltk
- scikit-learn
