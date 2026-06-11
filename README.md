# ReflectAI: ML-Powered Emotional Intelligence Journal 🧠✨

ReflectAI is an AI-powered journaling and emotional analytics platform that uses Natural Language Processing (NLP) and Machine Learning to analyze journal entries, classify emotions, and identify emotional well-being patterns.

The system combines traditional sentiment analysis techniques with supervised machine learning models to provide personalized emotional insights through a full-stack web application.

---

# 🚀 Features

- 📝 Secure personal journaling system
- 🤖 Machine Learning based emotion classification
- 🧠 NLP-powered sentiment analysis
- 📊 Emotional wellness analytics dashboard
- 📈 Long-term mood pattern tracking
- ⚡ Real-time emotion prediction through REST APIs
- 🔐 User authentication and journal management
- 📉 Cognitive and emotional trend analysis

---

# 🏗️ System Architecture

```text
                           ┌─────────────────────┐
                           │    React Frontend    │
                           │  Journal Dashboard   │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    Flask REST API    │
                           │ Backend Processing   │
                           └──────────┬──────────┘
                                      │
                  ┌───────────────────┴───────────────────┐
                  │                                       │
                  ▼                                       ▼
        ┌───────────────────┐              ┌──────────────────────┐
        │ VADER Sentiment   │              │ ML Emotion Classifier │
        │ Analysis Engine   │              │ TF-IDF + RandomForest │
        └─────────┬─────────┘              └───────────┬──────────┘
                  │                                    │
                  │                                    ▼
                  │                         ┌──────────────────────┐
                  │                         │ Emotion Prediction   │
                  │                         │ Confidence Scores    │
                  │                         └───────────┬──────────┘
                  │                                    │
                  └───────────────────┬────────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ ReflectAI Analytics      │
                         │ ERI | EVI | EDS Scores   │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ User Emotional Insights  │
                         │ Dashboard Visualization  │
                         └──────────────────────────┘
```

---

# 🧠 Machine Learning Pipeline

ReflectAI implements a supervised NLP classification pipeline for detecting emotions from textual journal data.

## Dataset Used

**HuggingFace `dair-ai/emotion` Dataset**

A labeled emotion classification dataset containing text samples mapped to six emotional categories:

- Joy
- Sadness
- Anger
- Fear
- Love
- Surprise

Dataset details:

| Property | Value |
|---|---|
| Task Type | Multi-Class Text Classification |
| Dataset Size | 20,000 text samples |
| Training Samples | 16,000 |
| Number of Classes | 6 |
| Feature Extraction | TF-IDF Vectorization |
| Vocabulary Size | 10,000 Features |

---

# ⚙️ ML Workflow

```text
Raw Journal Text
        |
        ▼
Text Cleaning & Preprocessing
        |
        ▼
TF-IDF Feature Extraction
        |
        ▼
Model Training Pipeline

        ├── Logistic Regression
        |
        ├── Random Forest Classifier
        |
        └── XGBoost Classifier

        |
        ▼

Model Evaluation

Accuracy
Precision
Recall
Weighted F1 Score
Confusion Matrix

        |
        ▼

Best Model Selection

        |
        ▼

Model Serialization

emotion_model.pkl
vectorizer.pkl

        |
        ▼

Flask ML Prediction API

        |
        ▼

Real-Time Emotion Analysis
```

---

# 🤖 Machine Learning Models

Multiple supervised learning models were implemented and compared.

## Logistic Regression

A baseline linear classifier used for efficient text classification.

## Random Forest Classifier

An ensemble learning approach using multiple decision trees to improve classification robustness.

## XGBoost Classifier

A gradient boosting algorithm optimized for high-performance classification.

---

# 📊 Model Evaluation Results

| Model | Validation Accuracy | Weighted F1 Score |
|---|---|---|
| Logistic Regression | 88.85% | 0.8852 |
| Random Forest | 89.65% | 0.8965 |
| XGBoost | 89.20% | 0.8922 |

## Selected Model

**Random Forest Classifier**

Final Test Performance:

| Metric | Score |
|---|---|
| Accuracy | 88.10% |
| Weighted F1 Score | 0.8811 |

The final trained model is integrated with Flask APIs for real-time emotion prediction.

---

# 📈 ReflectAI Emotional Intelligence Engine

Apart from ML classification, ReflectAI includes custom emotional analytics.

## Emotional Risk Index (ERI)

Analyzes emotional risk patterns based on sentiment behavior and journal history.

## Emotional Volatility Index (EVI)

Measures fluctuations in emotional states over time.

## Emotional Drift Score (EDS)

Tracks gradual emotional changes across multiple journal entries.

---

# 🛠️ Tech Stack

## Frontend

- React.js
- JavaScript
- HTML/CSS

## Backend

- Python
- Flask
- REST API
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

## Tools

- Git
- GitHub

## Deployment

- Vercel (Frontend Hosting)
- Render (Backend Deployment)

---
## 🌐 Live Demo

🔗 https://reflect-ai-ml-journal.vercel.app/

# ⚡ Installation & Setup

Clone the repository:

```bash
git clone https://github.com/kjohar45/ReflectAI-ML-Journal.git

cd ReflectAI-ML-Journal
```

---

## Backend Setup

Navigate to backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Flask server:

```bash
python app.py
```

---

## Train Machine Learning Model

Navigate:

```bash
cd backend/ml
```

Run training pipeline:

```bash
python train_model.py
```

The script performs:

- Dataset loading
- Text preprocessing
- Feature extraction
- Model training
- Model comparison
- Performance evaluation
- Model serialization

Generated artifacts:

```text
models/

emotion_model.pkl
vectorizer.pkl
metrics.json
```

---

## Frontend Setup

Navigate:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run React application:

```bash
npm start
```

---

# 🔮 Future Improvements

- Transformer-based emotion classification using BERT
- Personalized mental wellness recommendation system
- Emotion forecasting using sequential models
- Cloud deployment
- Mobile application support

---

# 🌟 Project Highlights

✔ End-to-end Machine Learning pipeline  
✔ Multiple ML model comparison  
✔ NLP-based emotion classification  
✔ Real-time ML inference using Flask APIs  
✔ Full-stack React + Python application  
✔ Custom emotional analytics system  

---

# 👩‍💻 Author

Developed by **Karuna Johar**
