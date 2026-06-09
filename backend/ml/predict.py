import os
import sys
import re
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Class Mapping for dair-ai/emotion
EMOTION_MAPPING = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# Lazily loaded model and vectorizer
_model = None
_vectorizer = None

def _load_artifacts():
    global _model, _vectorizer
    if _model is not None and _vectorizer is not None:
        return True
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "models", "emotion_model.pkl")
    vectorizer_path = os.path.join(current_dir, "models", "vectorizer.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print(f"Warning: ML model artifacts not found at {model_path} or {vectorizer_path}.")
        print("Please run 'python backend/ml/train_model.py' to train and save the model.")
        return False
        
    try:
        _model = joblib.load(model_path)
        _vectorizer = joblib.load(vectorizer_path)
        return True
    except Exception as e:
        print(f"Error loading model artifacts: {e}")
        return False

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    try:
        stop_words = set(stopwords.words("english"))
        tokens = [t for t in tokens if t not in stop_words]
    except Exception:
        pass
    return " ".join(tokens)

def predict_emotion(text):
    """
    Runs classification inference on the raw text.
    Returns a dictionary of:
    - predicted_emotion: str (sadness, joy, love, anger, fear, surprise)
    - confidence_score: float (0.0 to 1.0)
    - emotion_probabilities: dict mapping all 6 emotions to probability float values
    """
    # Attempt to load model and vectorizer
    artifacts_ready = _load_artifacts()
    
    # If not trained/ready, return a sensible default fallback
    if not artifacts_ready:
        return {
            "predicted_emotion": "neutral",
            "confidence_score": 0.0,
            "emotion_probabilities": {
                "sadness": 0.0,
                "joy": 0.0,
                "love": 0.0,
                "anger": 0.0,
                "fear": 0.0,
                "surprise": 0.0
            }
        }
        
    # Preprocess text
    cleaned = clean_text(text)
    
    # Vectorize
    vectorized = _vectorizer.transform([cleaned])
    
    # Predict probabilities
    try:
        prob = _model.predict_proba(vectorized)[0]
    except AttributeError:
        # Fallback if model doesn't support predict_proba
        pred = _model.predict(vectorized)[0]
        prob = [0.0] * 6
        prob[pred] = 1.0
        
    # Get index of max probability
    max_idx = int(prob.argmax())
    predicted_emotion = EMOTION_MAPPING.get(max_idx, "unknown")
    confidence_score = float(prob[max_idx])
    
    # Map probabilities
    probs_dict = {}
    for idx, name in EMOTION_MAPPING.items():
        probs_dict[name] = float(prob[idx])
        
    return {
        "predicted_emotion": predicted_emotion,
        "confidence_score": confidence_score,
        "emotion_probabilities": probs_dict
    }

if __name__ == "__main__":
    # Test inference output
    print("Testing ML inference:")
    sample = "I am so happy that everything is working out today!"
    res = predict_emotion(sample)
    print(f"Sample: \"{sample}\"")
    print(f"Result: {res}")
