import sqlite3
import datetime
from werkzeug.security import generate_password_hash

DB_NAME = "database.db"

def seed_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create dummy user
    username = "demo"
    password = "password"
    pwd_hash = generate_password_hash(password)
    
    # Insert user or get ID if exists
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pwd_hash))
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

    # Delete existing test data for this user to avoid duplicates
    cursor.execute("DELETE FROM journal WHERE user_id = ?", (user_id,))

    # Today
    today = datetime.datetime.now()
    
    # 7 sample entries
    samples = [
        # 6 days ago
        (today - datetime.timedelta(days=6), "Had a wonderful start to the week!", "Happy", 0.75),
        # 5 days ago
        (today - datetime.timedelta(days=5), "Felt a bit overwhelmed with work today.", "Anxious", -0.25),
        # 4 days ago
        (today - datetime.timedelta(days=4), "Just a normal day, nothing special.", "Neutral", 0.05),
        # 3 days ago
        (today - datetime.timedelta(days=3), "I am absolutely terrible and this is always a disaster.", "Sad", -0.85),
        # 2 days ago
        (today - datetime.timedelta(days=2), "Felt better after reaching out to a friend.", "Happy", 0.60),
        # 1 day ago
        (today - datetime.timedelta(days=1), "Still feeling a tiny bit anxious.", "Anxious", -0.15),
        # Today
        (today, "Feeling very productive and positive today!", "Happy", 0.80),
    ]

    for timestamp, text, emotion, score in samples:
        cursor.execute(
            "INSERT INTO journal (user_id, text, emotion, score, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, text, emotion, score, timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        )

    conn.commit()
    conn.close()
    print("Database successfully seeded! Login with Username: 'demo', Password: 'password'")

if __name__ == "__main__":
    seed_db()
