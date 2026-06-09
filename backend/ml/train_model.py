import os
import sys
import re
import json
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# We import load_dataset from datasets
try:
    from datasets import load_dataset
except ImportError:
    print("CRITICAL ERROR: 'datasets' package is not installed. Please check backend/requirements.txt.")
    sys.exit(1)

# Import sklearn models and utilities
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    import xgboost as xgb
except ImportError as e:
    print(f"CRITICAL ERROR: ML dependency import failed: {e}. Please check installed packages.")
    sys.exit(1)

from evaluate import calculate_metrics

# Download NLTK datasets
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
except Exception as e:
    print(f"Warning: Failed to download NLTK resources: {e}")

# Class Mapping for dair-ai/emotion
EMOTION_MAPPING = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

def clean_and_preprocess(text):
    """
    Standard preprocessing:
    - Lowercase conversion
    - Punctuation removal
    - Tokenization
    - Stopword removal
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Punctuation removal
    text = re.sub(r"[^\w\s]", "", text)
    
    # Tokenization (fallback to split if word_tokenize fails)
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
        
    # Stopword removal
    try:
        stop_words = set(stopwords.words("english"))
        tokens = [t for t in tokens if t not in stop_words]
    except Exception:
        pass
        
    return " ".join(tokens)

def main():
    print("==================================================")
    print("ReflectAI Machine Learning Training Pipeline")
    print("==================================================")
    
    # 1. Load real HuggingFace dair-ai/emotion dataset
    print("Step 1: Loading 'dair-ai/emotion' dataset from HuggingFace...")
    try:
        dataset = load_dataset("dair-ai/emotion")
        print("[OK] Dataset loaded successfully!")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Failed to load HuggingFace dair-ai/emotion dataset: {e}")
        print("Terminating training process. Internet connection or HuggingFace hub is required for training.")
        sys.exit(1)

    train_df = dataset["train"].to_pandas()
    val_df = dataset["validation"].to_pandas()
    test_df = dataset["test"].to_pandas()
    
    # 2. Text Preprocessing
    print("\nStep 2: Cleaning and preprocessing texts...")
    train_df["clean_text"] = train_df["text"].apply(clean_and_preprocess)
    val_df["clean_text"] = val_df["text"].apply(clean_and_preprocess)
    test_df["clean_text"] = test_df["text"].apply(clean_and_preprocess)
    
    # 3. Feature Extraction
    print("\nStep 3: Extracting TF-IDF Features...")
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    
    X_train = vectorizer.fit_transform(train_df["clean_text"])
    y_train = train_df["label"].values
    
    X_val = vectorizer.transform(val_df["clean_text"])
    y_val = val_df["label"].values
    
    X_test = vectorizer.transform(test_df["clean_text"])
    y_test = test_df["label"].values
    
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"Training shapes: X_train={X_train.shape}, y_train={y_train.shape}")
    
    # 4. Train and Compare Models
    print("\nStep 4: Training and comparing models...")
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
    }
    
    results = {}
    trained_models = {}
    
    for name, model in models.items():
        print(f"Training model: {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # Predict on validation set
        y_val_pred = model.predict(X_val)
        val_metrics = calculate_metrics(y_val, y_val_pred)
        results[name] = val_metrics
        print(f"  Validation F1-score (weighted): {val_metrics['f1_score']:.4f}")
        print(f"  Validation Accuracy: {val_metrics['accuracy']:.4f}")
        
    # 5. Best Model Selection (based on Weighted F1-score)
    best_model_name = max(results, key=lambda n: results[n]["f1_score"])
    print(f"\nStep 5: Best Model Selected: {best_model_name} (F1: {results[best_model_name]['f1_score']:.4f})")
    
    # Evaluate the best model on test set for final performance
    print("Evaluating best model on Test split...")
    best_model = trained_models[best_model_name]
    y_test_pred = best_model.predict(X_test)
    test_metrics = calculate_metrics(y_test, y_test_pred)
    print(f"  Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"  Test F1-score: {test_metrics['f1_score']:.4f}")
    
    # 6. Save Model, Vectorizer, and Metrics
    print("\nStep 6: Saving model artifacts...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "emotion_model.pkl")
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")
    metrics_path = os.path.join(models_dir, "metrics.json")
    
    # Save files
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"[OK] Saved best model to: {model_path}")
    print(f"[OK] Saved vectorizer to: {vectorizer_path}")
    
    # Format metrics for JSON dump
    metrics_to_save = {}
    for name, r in results.items():
        metrics_to_save[name] = {
            "accuracy": r["accuracy"],
            "precision": r["precision"],
            "recall": r["recall"],
            "f1_score": r["f1_score"],
            "confusion_matrix": r["confusion_matrix"]
        }
    metrics_to_save["best_model"] = best_model_name
    
    with open(metrics_path, "w") as f:
        json.dump(metrics_to_save, f, indent=2)
    print(f"[OK] Saved comparison metrics to: {metrics_path}")
    
    print("\nTraining complete! Models successfully prepared for deployment.")

if __name__ == "__main__":
    main()
