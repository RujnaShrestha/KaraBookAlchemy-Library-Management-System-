# karamain.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Import all project modules
from rujna import UserAdminLogin
from kashyabi import HomePage, SignupPage, AuthPage
from avigya import SettingsPage, ForgetPasswordPage
from apekshya import ProfilePage, SupportPage

# ── Color Scheme ──────────────────────────────────────────
BG      = "#CEC1A8"   # main background (tan/beige)
FRAME   = "#F1EADA"   # off-white frame / card
BROWN   = "#584738"   # dark brown (buttons, headers)
TEXT    = "#2C1A0E"   # dark text
SUBTEXT = "#7A6550"   # muted text
WHITE   = "#FFFFFF"
INPUT_BG= "#F1EADA"
# ─────────────────────────────────────────────────────────

FONT_TITLE = ("Georgia", 18, "bold")
FONT_H2    = ("Georgia", 13, "bold")
FONT_NAV   = ("Segoe UI", 10)
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN   = ("Segoe UI", 10, "bold")
FONT_INPUT = ("Segoe UI", 10)


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        try:
            self.conn = sqlite3.connect('kara_books.db')
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
            
            # Add default admin
            self.cursor.execute("SELECT * FROM admins WHERE admin_id='admin'")
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO admins (admin_id, password, admin_code) VALUES (?,?,?)", 
                                  ('admin', 'admin123', 'KARA2024'))
            
            # Add sample books
            self.cursor.execute("SELECT COUNT(*) FROM books")
            if self.cursor.fetchone()[0] == 0:
                sample_books = [
                    ('Harry Potter 1', 'J.K. Rowling', 'Fantasy'),
                    ('Harry Potter 2', 'J.K. Rowling', 'Fantasy'),
                    ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy'),
                    ('Pride and Prejudice', 'Jane Austen', 'Romance'),
                    ('Romeo and Juliet', 'William Shakespeare', 'Romance'),
                    ('To Kill a Mockingbird', 'Harper Lee', 'Fiction'),
                    ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction'),
                    ('Dracula', 'Bram Stoker', 'Horror'),
                    ('Frankenstein', 'Mary Shelley', 'Horror'),
                    ('The Silent Patient', 'Alex Michaelides', 'Thriller'),
                    ('Gone Girl', 'Gillian Flynn', 'Thriller'),
                    ('Atomic Habits', 'James Clear', 'Self-Help'),
                    ('Can\'t Hurt Me', 'David Goggins', 'Memoir'),
                    ('The Da Vinci Code', 'Dan Brown', 'Mystery'),
                    ('Dune', 'Frank Herbert', 'Sci-Fi')
                ]
                for book in sample_books:
                    self.cursor.execute("INSERT INTO books (title, author, genre) VALUES (?,?,?)", book)
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def get_cursor(self):
        return self.cursor
    
    def get_connection(self):
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()


class KaraBookAlchemy:
    def __init__(self, root):
        self.root = root
        self.root.title("KARA BOOK-ALCHEMY")
        self.root.geometry("900x650")
        self.root.configure(bg=BG)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Current user
        self.current_user = None
        self.current_user_id = None
        self.current_user_type = None
        
        # Authentication flag
        self.authenticated = False
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Initialize page objects
        self.login_page = None
        self.signup_page = None
        self.auth_page = None
        self.forget_page = None
        self.home_page = None
        self.profile_page = None
        self.support_page = None
        self.settings_page = None
        
        # Show login page
        self.show_login_page()
    
    def show_login_page(self):
        """Show login page"""
        self.login_page = UserAdminLogin(
            self.root, 
            self.db, 
            self.on_login_success,
            self.show_signup_page,
            self.show_forget_page
        )
        self.login_page.show()
    
    def show_signup_page(self):
        """Show signup page"""
        self.signup_page = SignupPage(
            self.root,
            self.db,
            self.on_signup_success,
            self.show_login_page
        )
        self.signup_page.show()
    
    def show_forget_page(self):
        """Show forget password page"""
        self.forget_page = ForgetPasswordPage(
            self.root,
            self.db,
            self.show_login_page
        )
        self.forget_page.show()
    
    def show_auth_page(self):
        """Show authentication page"""
        self.auth_page = AuthPage(
            self.root,
            self.db,
            self.on_auth_success,
            self.show_login_page
        )
        self.auth_page.show()
    
    def on_login_success(self, username, user_id, user_type):
        """Handle successful login - show authentication page"""
        self.current_user = username
        self.current_user_id = user_id
        self.current_user_type = user_type
        self.authenticated = False
        
        # Show authentication page instead of directly going to home
        self.show_auth_page()
    
    def on_auth_success(self):
        """Handle successful authentication - initialize and show home page"""
        self.authenticated = True
        
        # Initialize all pages
        self.init_pages()
        
        # Show home page
        self.show_home_page()
    
    def on_signup_success(self):
        """Handle successful signup"""
        self.show_login_page()
    
    def init_pages(self):
        """Initialize all page objects"""
        # Support page
        self.support_page = SupportPage(
            self.root,
            self.show_home_page,
            self.show_profile_page,
            self.show_settings_page,
            self.logout
        )
        
        # Settings page
        self.settings_page = SettingsPage(
            self.root,
            self.db,
            self.current_user,
            self.get_nav_callback,
            self.update_current_user,
            self.show_home_page,
            self.support_page.show,
            self.show_profile_page,
            self.logout
        )
        
        # Profile page
        self.profile_page = ProfilePage(
            self.root,
            self.db,
            self.current_user,
            self.current_user_type,
            self.show_home_page,
            self.support_page.show,
            self.show_settings_page,
            self.logout
        )
        
        # Home page
        self.home_page = HomePage(
            self.root,
            self.db,
            self.current_user,
            self.current_user_type,
            self.get_nav_callback,
            self.logout,
            self.support_page.show,
            self.show_profile_page,
            self.show_settings_page
        )
    
    def get_nav_callback(self, page_name):
        """Return callback function for navigation"""
        def callback():
            if not self.authenticated:
                self.show_login_page()
                return
                
            if page_name == "Home":
                self.show_home_page()
            elif page_name == "Support":
                if self.support_page:
                    self.support_page.show()
            elif page_name == "Profile":
                self.show_profile_page()
            elif page_name == "Settings":
                self.show_settings_page()
            elif page_name == "Logout":
                self.logout()
        return callback
    
    def update_current_user(self, new_username):
        """Update current username after settings change"""
        self.current_user = new_username
        # Reinitialize pages with new username
        self.init_pages()
    
    def show_home_page(self):
        """Show home page"""
        if self.home_page and self.authenticated:
            self.home_page.current_user = self.current_user
            self.home_page.current_user_type = self.current_user_type
            self.home_page.show()
    
    def show_profile_page(self):
        """Show profile page"""
        if self.profile_page and self.authenticated:
            self.profile_page.current_user = self.current_user
            self.profile_page.current_user_type = self.current_user_type
            self.profile_page.show()
    
    def show_settings_page(self):
        """Show settings page"""
        if self.settings_page and self.authenticated:
            self.settings_page.current_user = self.current_user
            self.settings_page.show()
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.current_user_id = None
            self.current_user_type = None
            self.authenticated = False
            self.home_page = None
            self.profile_page = None
            self.support_page = None
            self.settings_page = None
            self.show_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = KaraBookAlchemy(root)
    root.mainloop()