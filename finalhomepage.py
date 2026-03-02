import tkinter as tk
from tkinter import messagebox
from homepagebackend import HomeBackend
from Homepagedesign import HomeUI
from Uiconfig import *

class HomePage:
    def __init__(self, root, db_manager, current_user, current_user_type, 
                 on_nav, on_logout, show_support, show_profile, show_settings):
        self.root = root
        self.db_manager = db_manager
        
        # Initialize backend
        self.backend = HomeBackend(db_manager, current_user, current_user_type)
        
        # Store callbacks
        self.callbacks = {
            'on_logout': on_logout,
            'show_support': show_support,
            'show_profile': show_profile,
            'show_settings': show_settings,
            'refresh_home': self.show,
            'search_books': self.search_books,
            'show_genre_menu': self.show_genre_menu,
            'show_add_book_dialog': self.show_add_book_dialog,
            'add_to_list': self.add_to_reading_list,
            'reserve': self.reserve_book,
            'delete': self.delete_book
        }
        
        # Initialize UI
        self.ui = HomeUI(root, self.backend, self.callbacks)
        
        # UI elements
        self.genre_var = None
        self.search_entry = None
    
    def show(self):
        """Show home page"""
        self.ui.clear_window()
        self.root.configure(bg=BG)

        # Build all UI components
        self.ui.build_header(self.root)
        
        search_bar = self.ui.build_search_bar(self.root)
        # Store references to UI elements needed for search
        self.search_entry = self.ui.search_entry
        self.genre_var = self.ui.genre_var

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=8)
        
        self.ui.build_sidebar(body)
        self.ui.build_main_area(body)
        
        # Display books
        self.ui.display_books()

    def search_books(self):
        """Handle book search"""
        query = self.search_entry.get().strip()
        genre = self.genre_var.get()
        books = self.backend.search_books_db(query, genre)
        self.ui.display_books(books)

    def show_genre_menu(self):
        """Show genre selection menu"""
        genres = ["All","Fantasy","Fiction","Romance","Horror","Thriller","Sci-Fi"]
        self.ui.show_genre_menu(genres, self.select_genre)
    
    def select_genre(self, genre):
        """Handle genre selection"""
        self.genre_var.set(genre)
        self.search_books()

    def add_to_reading_list(self, book):
        """Add book to reading list"""
        success, message = self.backend.add_to_reading_list(book[0], book[1])
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def reserve_book(self, book):
        """Reserve a book"""
        success, message = self.backend.reserve_book(book[0], book[1])
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def delete_book(self, book):
        """Delete a book (admin only)"""
        if messagebox.askyesno("Delete", f"Delete '{book[1]}'?"):
            success, message = self.backend.delete_book(book[0])
            if success:
                self.show()
            else:
                messagebox.showerror("Error", message)

    def show_add_book_dialog(self):
        """Show dialog to add a new book"""
        self.ui.show_add_book_dialog(self.save_new_book)
    
    def save_new_book(self, title, author, genre, dialog):
        """Save new book to database"""
        success, message = self.backend.add_new_book(title, author, genre)
        if success:
            dialog.destroy()
            self.show()
        else:
            messagebox.showerror("Error", message)