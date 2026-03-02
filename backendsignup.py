import sqlite3
from tkinter import messagebox

class SignupBackend:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 4:
            return False, "Password too short! Minimum 4 characters required."
        return True, "Password valid"
    
    def validate_username(self, username):
        """Validate username"""
        if not username or not username.strip():
            return False, "Username cannot be empty"
        return True, "Username valid"
    
    def create_user(self, username, password):
        """Create a new user in the database"""
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?,?,'user')",
                               (username, password))
            conn.commit()
            return True, "Account created successfully!"
            
        except sqlite3.IntegrityError:
            return False, "Username already exists!"
        except sqlite3.Error as e:
            return False, f"Signup failed: {e}"