from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sentiment import analyze_sentiment
from models import create_journal_table, create_users_table
from llm import generate_motivation
from reflect import calculate_asp, classify_emotion, calculate_eds, calculate_evi, detect_cognitive_distortions, calculate_eri, generate_reflect_feedback
from werkzeug.security import generate_password_hash, check_password_hash
from ml.predict import predict_emotion
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

# CONFIG

app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "https://reflect-ai-ml-journal.vercel.app"
            ]
        }
    },
    supports_credentials=True
)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized(reason):
    print(f"[DEBUG] JWT Unauthorized: {reason}")
    auth_header = request.headers.get("Authorization", "NOT FOUND")
    print(f"[DEBUG] Authorization header present: {auth_header != 'NOT FOUND'}")
    if auth_header != "NOT FOUND":
        print(f"[DEBUG] Authorization header preview: {auth_header[:50]}...")
    return jsonify({"error": "Missing Authorization Header"}), 401

@jwt.invalid_token_loader
def invalid(reason):
    print(f"[DEBUG] JWT Invalid Token: {reason}")
    auth_header = request.headers.get("Authorization", "NOT FOUND")
    print(f"[DEBUG] Authorization header present: {auth_header != 'NOT FOUND'}")
    if auth_header != "NOT FOUND":
        print(f"[DEBUG] Authorization header preview: {auth_header[:50]}...")
    return jsonify({"error": "Invalid token"}), 401

# ===============================
# DB INIT
# ===============================
create_users_table()
create_journal_table()

# ===============================
# ROUTES
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running"})

# ---------- AUTH ----------
@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    emergency_contact_name = data.get("emergency_contact_name")
    emergency_contact_phone = data.get("emergency_contact_phone")

    if not username or not password:
        return jsonify({"error": "Required"}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, emergency_contact_name, emergency_contact_phone) VALUES (?, ?, ?, ?)",
            (username, password_hash, emergency_contact_name, emergency_contact_phone)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User registered"})

@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
            
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user[1], password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Flask-JWT-Extended requires identity to be a string
        token = create_access_token(identity=str(user[0]))
        # Debug: log token shape (not full token)
        print(f"[DEBUG] Issued token for user_id={user[0]} (as string) len={len(token)} preview={token[:25]}...")
        return jsonify({"access_token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- JOURNAL ----------
@app.route("/journal", methods=["POST"])
@jwt_required()
def add_journal():
    try:
        # Debug: Check Authorization header
        auth_header = request.headers.get("Authorization", "NOT FOUND")
        print(f"[DEBUG] Authorization header: {auth_header[:50] if auth_header != 'NOT FOUND' else 'NOT FOUND'}")
        
        # get_jwt_identity() returns a string, convert to int for database queries
        user_id = int(get_jwt_identity())
        print(f"[DEBUG] User ID from token: {user_id}")
        text = request.json.get("text", "")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        emotion, score = analyze_sentiment(text)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT score, emotion FROM journal WHERE user_id = ? ORDER BY created_at ASC", (user_id,))
        rows = cursor.fetchall()
        
        history_scores = [r[0] for r in rows]
        history_emotions = [r[1] for r in rows]

        # 1. Adaptive Sentiment Personalization (ASP)
        mean, std_dev, T_pos, T_neg = calculate_asp(history_scores)
        emotion = classify_emotion(score, T_pos, T_neg)

        # 2. Emotional Drift Modeling (EDM)
        eds = calculate_eds(score, mean, std_dev)

        # 3. Cognitive Pattern Detection (CPD) & LLM Crisis
        from llm import analyze_crisis_with_llm
        cpd_count, found_distortions = detect_cognitive_distortions(text)
        crisis_type = analyze_crisis_with_llm(text)

        # 4. Emotional Risk Index (ERI)
        recent_emotions = history_emotions[-10:] + [emotion]
        k_risk_ratio = cpd_count / 3.0 # arbitrary normalization
        eri = calculate_eri(recent_emotions, eds, k_risk_ratio)

        # 5. Feedback/Motivation Module
        motivation = generate_reflect_feedback(eri, eds, cpd_count, found_distortions)
        if not motivation:
            motivation = generate_motivation(text, emotion)

        # 6. Intercept Strategy (do not auto-dispatch SMS here)
        ml_res = predict_emotion(text)

        cursor.execute(
            "INSERT INTO journal (user_id, text, emotion, score) VALUES (?, ?, ?, ?)",
            (user_id, text, emotion, score)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Saved",
            "emotion": emotion,
            "sentiment_score": score,
            "motivation": motivation,
            "eds": eds,
            "eri": eri,
            "cpd_count": cpd_count,
            "crisis_type": crisis_type,
            "ml_emotion": ml_res["predicted_emotion"],
            "ml_confidence": ml_res["confidence_score"],
            "ml_probabilities": ml_res["emotion_probabilities"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/journal/trigger_sms_alert", methods=["POST"])
@jwt_required()
def trigger_sms():
    try:
        user_id = int(get_jwt_identity())
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, emergency_contact_name, emergency_contact_phone FROM users WHERE id = ?", (user_id,))
        contact = cursor.fetchone()
        conn.close()

        if contact and contact[0] and contact[1] and contact[2]:
            from sms_service import send_emergency_sms
            send_emergency_sms(contact[0], contact[1], contact[2])
            return jsonify({"status": "Sent SMS successfully"})
        else:
            return jsonify({"error": "No valid emergency phone number on file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/journal/metrics", methods=["GET"])
@jwt_required()
def get_metrics():
    try:
        user_id = int(get_jwt_identity())
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT score, emotion, text FROM journal WHERE user_id = ? ORDER BY created_at ASC", (user_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({
                "mean": 0, "std_dev": 0, "T_pos": 0.5, "T_neg": -0.5,
                "evi": 0, "eri": 0, "eds_avg": 0, "distortions": []
            })
            
        history_scores = [r[0] for r in rows]
        history_emotions = [r[1] for r in rows]
        last_text = rows[-1][2]
        last_score = rows[-1][0]
        
        # ASP metrics
        mean, std_dev, T_pos, T_neg = calculate_asp(history_scores)
        
        # EVI
        evi = calculate_evi(history_emotions)
        
        # EDS
        last_eds = calculate_eds(last_score, mean, std_dev)
        
        # CPD
        cpd_count, found_d = detect_cognitive_distortions(last_text)
        
        # ERI
        eri = calculate_eri(history_emotions[-10:], last_eds, cpd_count / 3.0)

        # ML predicted emotion for the latest entry
        ml_res = predict_emotion(last_text)

        return jsonify({
            "mean": mean,
            "std_dev": std_dev,
            "T_pos": T_pos,
            "T_neg": T_neg,
            "evi": evi,
            "eri": eri,
            "eds_latest": last_eds,
            "distortions": found_d,
            "ml_emotion": ml_res["predicted_emotion"],
            "ml_confidence": ml_res["confidence_score"],
            "ml_probabilities": ml_res["emotion_probabilities"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/journal/weekly", methods=["GET"])
@jwt_required()
def weekly():
    try:
        # Debug: check header and identity
        auth_header = request.headers.get("Authorization", "NOT FOUND")
        print(f"[DEBUG] /journal/weekly Authorization: {auth_header[:60] if auth_header != 'NOT FOUND' else 'NOT FOUND'}")

        # get_jwt_identity() returns a string, convert to int for database queries
        user_id = int(get_jwt_identity())
        print(f"[DEBUG] /journal/weekly user_id from token: {user_id}")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT emotion, COUNT(*)
                       FROM journal
                       WHERE user_id = ?
                         AND created_at >= datetime('now', '-7 days')
                       GROUP BY emotion
                       """, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        result = {"Happy": 0, "Sad": 0, "Neutral": 0, "Anxious": 0}
        for e, c in rows:
            result[e] = c

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/journal/weekly/mean", methods=["GET"])
@jwt_required()
def weekly_mean():
    try:
        # Debug: check header and identity
        auth_header = request.headers.get("Authorization", "NOT FOUND")
        print(f"[DEBUG] /journal/weekly/mean Authorization: {auth_header[:60] if auth_header != 'NOT FOUND' else 'NOT FOUND'}")
        
        # get_jwt_identity() returns a string, convert to int for database queries
        user_id = int(get_jwt_identity())
        print(f"[DEBUG] /journal/weekly/mean user_id from token: {user_id}")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT emotion FROM journal
                       WHERE user_id = ?
                         AND created_at >= datetime('now', '-7 days')
                       """, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({"mean_label": "No data"})

        scores = {"Happy": 1, "Neutral": 0, "Anxious": -0.5, "Sad": -1}
        mean = sum(scores.get(e[0], 0) for e in rows) / len(rows)

        label = "Happy" if mean > 0.4 else "Neutral" if mean > -0.1 else "Sad"
        return jsonify({"mean_label": label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/journal/by-date", methods=["GET"])
@jwt_required()
def get_journal_by_date():
    try:
        # get_jwt_identity() returns a string, convert to int for database queries
        user_id = int(get_jwt_identity())
        date = request.args.get("date")

        if not date:
            return jsonify({"error": "Date is required"}), 400

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT text, emotion, created_at
                       FROM journal
                       WHERE user_id = ?
                         AND date(datetime(created_at, '+5 hours', '+30 minutes')) = ?
                       ORDER BY created_at ASC
                       """, (user_id, date))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({
                "date": date,
                "entries": [],
                "overall_emotion": "No data"
            })

        emotion_scores = {
            "Happy": 1.0,
            "Neutral": 0.0,
            "Anxious": -0.5,
            "Sad": -1.0
        }

        total_score = 0
        entries = []

        for row in rows:
            text, emotion, created_at = row
            total_score += emotion_scores.get(emotion, 0)
            entries.append({"text": text})

        mean_score = total_score / len(rows)

        if mean_score >= 0.5:
            overall_emotion = "Happy"
        elif mean_score >= 0.1:
            overall_emotion = "Slightly Positive"
        elif mean_score > -0.1:
            overall_emotion = "Neutral"
        elif mean_score > -0.5:
            overall_emotion = "Anxious"
        else:
            overall_emotion = "Sad"

        return jsonify({
            "date": date,
            "entries": entries,
            "overall_emotion": overall_emotion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)


