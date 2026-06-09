# ReflectAI: ML-Powered Emotional Intelligence Journal 🧠

ReflectAI is an AI-powered journaling and emotional analytics platform that uses Natural Language Processing and Machine Learning to analyze user journal entries, classify emotions, and track mental well-being patterns over time.

The system combines traditional NLP-based sentiment analysis with supervised machine learning models to provide personalized emotional insights through an interactive full-stack application.

---

## 🚀 Features

- 📝 Secure personal journaling system
- 🤖 Machine Learning based emotion classification
- 📊 Emotional wellness analytics dashboard
- 📈 Long-term mood and sentiment tracking
- 🧠 Cognitive pattern analysis
- ⚡ Real-time journal analysis using REST APIs
- 🔐 User authentication and data management

---

# 🏗️ System Architecture


User Journal Entry
        |
        ↓
React Frontend
        |
        ↓
Flask REST API
        |
        ↓
Text Preprocessing Layer
        |
        ├─────────────────────────┐
        |                         |
        ↓                         ↓
VADER Sentiment Engine     ML Emotion Classifier
        |                         |
Sentiment Polarity       TF-IDF Feature Extraction
                                  |
                                  ↓
                    Random Forest Emotion Model
                                  |
                                  ↓
                      Emotion Prediction
                                  |
        └─────────────────────────┘
                    |
                    ↓
            ReflectAI Analytics Engine
                    |
        ┌───────────┼───────────┐
        ↓           ↓           ↓
       ERI         EVI         EDS

                    |
                    ↓
              User Dashboard


---

# 🧠 Machine Learning Pipeline

ReflectAI implements a supervised NLP classification pipeline to predict emotional states from journal text.

## Dataset

**Dataset Used:** HuggingFace `dair-ai/emotion`

The dataset consists of labeled text samples categorized into six emotional classes:

- Joy
- Sadness
- Anger
- Fear
- Love
- Surprise


Dataset Details:

| Property | Value |
|---|---|
| Dataset Type | Text Classification |
| Total Samples | 20,000 |
| Training Samples | 16,000 |
| Number of Classes | 6 |
| Feature Extraction | TF-IDF |
| Vocabulary Size | 10,000 Features |

---

# ⚙️ ML Workflow


Raw Journal Text
        |
        ↓
Text Cleaning
        |
        ↓
Tokenization & Preprocessing
        |
        ↓
TF-IDF Vectorization
        |
        ↓
Model Training
        |
        ↓
Model Evaluation
        |
        ↓
Best Model Selection
        |
        ↓
Emotion Prediction


---

# 🤖 Models Implemented

Multiple machine learning models were trained and evaluated:

## Logistic Regression

A baseline linear classification model for text-based emotion prediction.

## Random Forest Classifier

An ensemble learning model using multiple decision trees for robust emotion classification.

## XGBoost Classifier

A gradient boosting model optimized for high-performance classification tasks.

---

# 📊 Model Performance

| Model | Validation Accuracy | Weighted F1 Score |
|---|---|---|
| Logistic Regression | 88.85% | 0.8852 |
| Random Forest | 89.65% | 0.8965 |
| XGBoost | 89.20% | 0.8922 |

## Best Performing Model

**Random Forest Classifier**

Final Test Performance:

| Metric | Score |
|---|---|
| Accuracy | 88.10% |
| Weighted F1 Score | 0.8811 |

The trained model is serialized and integrated with the backend for real-time inference.

---

# 📈 ReflectAI Emotional Analytics

Along with ML-based classification, ReflectAI calculates advanced emotional indicators.

## Emotional Risk Index (ERI)

Measures emotional risk patterns based on journal sentiment and emotional history.

## Emotional Volatility Index (EVI)

Tracks emotional fluctuations across multiple journal entries.

## Emotional Drift Score (EDS)

Detects gradual shifts in emotional patterns over time.

---

# 🛠️ Tech Stack

## Frontend

- React.js
- JavaScript
- HTML/CSS

## Backend

- Python
- Flask
- REST APIs
- SQLite

## Machine Learning & NLP

- Scikit-learn
- XGBoost
- NLTK
- VADER Sentiment Analyzer
- TF-IDF Vectorization

## Data Processing

- Pandas
- NumPy

## Development Tools

- Git
- GitHub

---

# 📁 Project Structure


ReflectAI-ML-Journal

├── backend
│
│   ├── ml
│   │   ├── train_model.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   │
│   │   └── models
│   │       ├── emotion_model.pkl
│   │       ├── vectorizer.pkl
│   │       └── metrics.json
│   │
│   ├── app.py
│   └── requirements.txt
│
├── frontend
│
└── README.md


---

# ⚡ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/kjohar45/ReflectAI-ML-Journal.git

cd ReflectAI-ML-Journal
```

---

## Backend Setup

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Flask server:

```bash
python app.py
```

---

## Machine Learning Training

Navigate to ML directory:

```bash
cd backend/ml
```

Train models:

```bash
python train_model.py
```

This performs:

- Dataset loading
- Text preprocessing
- Model training
- Model comparison
- Evaluation
- Model serialization

Generated artifacts:

```
models/
 ├── emotion_model.pkl
 ├── vectorizer.pkl
 └── metrics.json
```

---

## Frontend Setup

Navigate:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start React application:

```bash
npm start
```

---

# 🔮 Future Enhancements

- Transformer-based emotion classification using BERT
- Personalized recommendation system
- Advanced mental health trend forecasting
- Cloud deployment
- Mobile application support

---

# 📌 Project Highlights

✔ End-to-end ML pipeline implementation  
✔ Multiple model comparison and evaluation  
✔ Real-time ML inference through Flask APIs  
✔ Full-stack React + Python integration  
✔ NLP-based emotion understanding system  

---

# 👩‍💻 Author

Developed by Karuna Johar
