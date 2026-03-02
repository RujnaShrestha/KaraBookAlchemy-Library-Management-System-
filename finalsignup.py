import tkinter as tk
from tkinter import messagebox
from backendsignup import SignupBackend
from signupdesign import SignupUI
from Uiconfig import *

class SignupPage:
    def __init__(self, root, db_manager, on_signup_success, on_back_to_login):
        self.root = root
        self.db_manager = db_manager
        
        # Initialize backend
        self.backend = SignupBackend(db_manager)
        
        # Store callbacks
        self.on_signup_success = on_signup_success
        self.on_back_to_login = on_back_to_login
        
        # Create callbacks dictionary for UI
        callbacks = {
            'on_signup': self.signup,
            'on_back_to_login': self.on_back_to_login
        }
        
        # Initialize UI
        self.ui = SignupUI(root, callbacks)
    
    def show(self):
        """Show signup page"""
        self.ui.clear_window()
        self.root.configure(bg=BG)
        
        # Build all UI components
        self.ui.build_header()
        self.ui.build_content()
    
    def signup(self):
        """Handle user signup - coordinates between UI and backend"""
        # Get form data from UI
        username, password = self.ui.get_form_data()
        
        # Validate inputs
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        # Validate password
        is_valid, message = self.backend.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        # Validate username
        is_valid, message = self.backend.validate_username(username)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        # Create user in database
        success, message = self.backend.create_user(username, password)
        
        if success:
            messagebox.showinfo("Success", "Account created! Please login.")
            self.ui.clear_form()  # Clear form for next use
            self.on_back_to_login()
        else:
            messagebox.showerror("Error", message)