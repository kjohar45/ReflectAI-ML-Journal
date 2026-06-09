import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def migrate_journal_table():
    """Migrate existing journal table to include user_id column if missing"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='journal'
    """)
    table_exists = cursor.fetchone() is not None
    
    if table_exists:
        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(journal)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "user_id" not in columns:
            # Table exists but missing user_id column
            # We need to recreate the table with the new schema
            # Note: This will lose existing data, but is necessary for proper functionality
            cursor.execute("DROP TABLE journal")
            conn.commit()
    
    conn.close()

def create_journal_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Migrate existing table if needed
    migrate_journal_table()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS journal (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          user_id INTEGER NOT NULL,
                                                          text TEXT NOT NULL,
                                                          emotion TEXT NOT NULL,
                                                          score REAL NOT NULL,
                                                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                          FOREIGN KEY (user_id) REFERENCES users(id)
                   )
                   """)

    conn.commit()
    conn.close()

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Migrate users table to add emergency columns if missing
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if columns and "emergency_contact_phone" not in columns:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN emergency_contact_name TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass
            
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN emergency_contact_phone TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        username TEXT UNIQUE NOT NULL,
                                                        password_hash TEXT NOT NULL,
                                                        emergency_contact_name TEXT,
                                                        emergency_contact_phone TEXT,
                                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """)

    conn.commit()
    conn.close()
