
import sqlite3
from tkinter import messagebox
from datetime import datetime

class HomeBackend:
    def __init__(self, db_manager, current_user, current_user_type):
        self.db = db_manager
        self.current_user = current_user
        self.current_user_type = current_user_type
    
    def get_all_books(self):
        """Fetch all books from database"""
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()
        except sqlite3.Error:
            return []
    
    def search_books_db(self, query, genre):
        """Search books based on query and genre"""
        try:
            cursor = self.db.get_cursor()
            if query and genre != "All":
                cursor.execute("SELECT * FROM books WHERE title LIKE ? AND genre=?", 
                                   (f'%{query}%', genre))
            elif query:
                cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{query}%',))
            elif genre != "All":
                cursor.execute("SELECT * FROM books WHERE genre=?", (genre,))
            else:
                cursor.execute("SELECT * FROM books")
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Search failed: {e}")
            return []
    
    def add_to_reading_list(self, book_id, book_title):
        """Add book to user's reading list"""
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("SELECT reading_list FROM users WHERE username=?", (self.current_user,))
            result = cursor.fetchone()
            reading_list = result[0] if result[0] else ""
            
            if str(book_id) in reading_list:
                return False, f"'{book_title}' already in your list!"
            
            new_list = reading_list + f",{book_id}" if reading_list else str(book_id)
            cursor.execute("UPDATE users SET reading_list=? WHERE username=?", 
                               (new_list, self.current_user))
            conn.commit()
            return True, f"'{book_title}' added to your list!"
        except sqlite3.Error as e:
            return False, f"Failed: {e}"
    
    def reserve_book(self, book_id, book_title):
        """Reserve a book"""
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT * FROM reservations WHERE book_id=? AND status='reserved'", (book_id,))
            if cursor.fetchone():
                return False, f"'{book_title}' already reserved!"
            
            cursor.execute("INSERT INTO reservations (book_id, book_title, username, reserved_date) VALUES (?,?,?,?)",
                               (book_id, book_title, self.current_user, date))
            conn.commit()
            return True, f"'{book_title}' reserved!"
        except sqlite3.Error as e:
            return False, f"Failed: {e}"
    
    def delete_book(self, book_id):
        """Delete a book (admin only)"""
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            return True, "Book deleted successfully"
        except sqlite3.Error as e:
            return False, f"Failed: {e}"
    
    def add_new_book(self, title, author, genre):
        """Add a new book (admin only)"""
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("INSERT INTO books (title, author, genre) VALUES (?,?,?)",
                               (title, author, genre))
            conn.commit()
            return True, "Book added successfully"
        except sqlite3.Error as e:
            return False, f"Failed: {e}"