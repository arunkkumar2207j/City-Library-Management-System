import sqlite3
from datetime import datetime
import os

DB_DIR = "db"
os.makedirs(DB_DIR, exist_ok=True)

DB_NAME = os.path.join(DB_DIR, "library.db")

def init_db():
    """Initialize database and create tables if not exists."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create book table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            available INTEGER DEFAULT 1,
            borrower TEXT
        );
    """)

    # Create members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            contact_info TEXT
        );
    """)

    # Create borrowed_books table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            borrow_date TEXT,
            return_date TEXT,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
        );
    """)

    conn.commit()
    conn.close()

def execute_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # ✅ makes cursor results behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    if fetch:
        rows = cur.fetchall()
        data = [dict(row) for row in rows]  # convert sqlite Row → dict
        conn.close()
        return data
    conn.close()


def seed_data():
    """Insert sample books and members if tables are empty."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # --- Check if already seeded ---
    cur.execute("SELECT COUNT(*) FROM books;")
    book_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM members;")
    member_count = cur.fetchone()[0]

    # --- Seed books ---
    if book_count == 0:
        sample_books = [
            ("The Alchemist", "Paulo Coelho", "Fiction"),
            ("Atomic Habits", "James Clear", "Self-Help"),
            ("To Kill a Mockingbird", "Harper Lee", "Classic")
        ]
        cur.executemany(
            "INSERT INTO books (title, author, genre, available) VALUES (?, ?, ?, 1);",
            sample_books
        )
        print("📚 Sample books added.")

    # --- Seed members ---
    if member_count == 0:
        sample_members = [
            ("Arun", 25, "arun@email.com"),
            ("Priya", 30, "priya@email.com")
        ]
        cur.executemany(
            "INSERT INTO members (name, age, contact_info) VALUES (?, ?, ?);",
            sample_members
        )
        print("👥 Sample members added.")

    conn.commit()
    conn.close()
    print("✅ Seeding completed successfully!")
