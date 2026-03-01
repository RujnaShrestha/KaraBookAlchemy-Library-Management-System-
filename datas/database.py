import sqlite3
from tkinter import messagebox

class DatabaseManager:
    def __init__(self, db_path='kara_books.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Create users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    user_type TEXT NOT NULL,
                    reading_list TEXT DEFAULT '',
                    reserved_books TEXT DEFAULT '',
                    email TEXT DEFAULT ''
                )
            ''')
            
            # Create admin table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    admin_code TEXT NOT NULL
                )
            ''')
            
            # Create books table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    reserved_by TEXT DEFAULT '',
                    reserved_date TEXT DEFAULT ''
                )
            ''')
            
            # Create reservations table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    book_title TEXT NOT NULL,
                    username TEXT NOT NULL,
                    reserved_date TEXT NOT NULL,
                    status TEXT DEFAULT 'reserved'
                )
            ''')
            
            # Add default admin if not exists
            self.cursor.execute("SELECT * FROM admins WHERE admin_id='admin'")
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO admins (admin_id, password, admin_code) VALUES (?,?,?)", 
                    ('admin', 'admin123', 'KARA2024')
                )
            
            # Add sample books if table is empty
            self.cursor.execute("SELECT COUNT(*) FROM books")
            if self.cursor.fetchone()[0] == 0:
                self._add_sample_books()
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def _add_sample_books(self):
        """Add sample books to the database"""
        sample_books = [
            # Fantasy
            ('Harry Potter 1', 'J.K. Rowling', 'Fantasy'),
            ('Harry Potter 2', 'J.K. Rowling', 'Fantasy'),
            ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy'),
            # Romance
            ('Pride and Prejudice', 'Jane Austen', 'Romance'),
            ('Romeo and Juliet', 'William Shakespeare', 'Romance'),
            # Fiction
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction'),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction'),
            # Horror
            ('Dracula', 'Bram Stoker', 'Horror'),
            ('Frankenstein', 'Mary Shelley', 'Horror'),
            # Thriller
            ('The Silent Patient', 'Alex Michaelides', 'Thriller'),
            ('Gone Girl', 'Gillian Flynn', 'Thriller'),
            # Self-Help
            ('Atomic Habits', 'James Clear', 'Self-Help'),
            ('Can\'t Hurt Me', 'David Goggins', 'Memoir'),
            # Mystery
            ('The Da Vinci Code', 'Dan Brown', 'Mystery'),
            # Sci-Fi
            ('Dune', 'Frank Herbert', 'Sci-Fi')
        ]
        
        for book in sample_books:
            self.cursor.execute(
                "INSERT INTO books (title, author, genre) VALUES (?,?,?)", 
                book
            )
    
    def get_cursor(self):
        """Get database cursor"""
        return self.cursor
    
    def get_connection(self):
        """Get database connection"""
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()