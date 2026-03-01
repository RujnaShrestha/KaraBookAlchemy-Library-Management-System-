import tkinter as tk
from tkinter import messagebox
import sqlite3
from constantUI import *

class ReadingListManager:
    def __init__(self, parent, db, username, refresh_callback):
        self.parent = parent
        self.db = db
        self.username = username
        self.refresh_callback = refresh_callback

    def display(self):
        """Display user's reading list with remove option"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT reading_list FROM users WHERE username=?", (self.username,))
        result = cursor.fetchone()
        
        if result and result[0]:
            ids = result[0].split(',')
            if ids[0]:
                placeholders = ','.join('?' for _ in ids)
                cursor.execute(f"SELECT * FROM books WHERE id IN ({placeholders})", ids)
                books = cursor.fetchall()
                if books:
                    for b in books:
                        self._create_reading_list_item(b)
                else:
                    tk.Label(self.parent, text="No books in your reading list.", bg=FRAME, fg=TEXT).pack(pady=10)
        else:
            tk.Label(self.parent, text="Your reading list is empty.", bg=FRAME, fg=TEXT).pack(pady=10)

    def _create_reading_list_item(self, book):
        """Create a reading list item with remove button"""
        book_frame = tk.Frame(self.parent, bg=FRAME)
        book_frame.pack(fill="x", pady=2, padx=5)
        
        tk.Label(book_frame, text=f"📖 {book[1]}", bg=FRAME, fg=TEXT).pack(side="left")
        
        remove_btn = tk.Button(
            book_frame, text="Remove", bg="#8B3A3A", fg=WHITE,
            font=FONT_SMALL, relief="flat", cursor="hand2",
            command=lambda book_id=book[0]: self.remove_from_reading_list(book_id)
        )
        remove_btn.pack(side="right", padx=5)

    def remove_from_reading_list(self, book_id):
        """Remove a book from the user's reading list"""
        if messagebox.askyesno("Confirm Remove", "Remove this book from your reading list?"):
            try:
                cursor = self.db.get_cursor()
                conn = self.db.get_connection()
                
                cursor.execute("SELECT reading_list FROM users WHERE username=?", (self.username,))
                result = cursor.fetchone()
                
                if result and result[0]:
                    ids = result[0].split(',')
                    if str(book_id) in ids:
                        ids.remove(str(book_id))
                        new_list = ','.join(ids)
                        cursor.execute(
                            "UPDATE users SET reading_list=? WHERE username=?", 
                            (new_list, self.username)
                        )
                        conn.commit()
                        messagebox.showinfo("Success", "Book removed from reading list.")
                        self.refresh_callback()
                        
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to remove book: {e}")