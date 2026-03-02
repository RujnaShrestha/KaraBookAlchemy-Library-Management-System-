import tkinter as tk
from Uiconfig import *

class SignupUI:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks  # Contains on_signup, on_back_to_login
        
        self.signup_username = None
        self.signup_password = None
    
    def build_header(self):
        """Build the header section"""
        h = tk.Frame(self.root, bg=BG, pady=10)
        h.pack(fill="x")
        
        # Logo
        logo = tk.Frame(h, bg=FRAME, width=80, height=60, relief="solid", bd=1)
        logo.pack(side="left", padx=16)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 9, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        
        # Title
        tk.Label(h, text="WELCOME TO\nKARA BOOK-ALCHEMY",
                 font=FONT_TITLE, bg=BG, fg=TEXT, justify="left").pack(side="left", padx=10)
        
        return h
    
    def build_content(self):
        """Build the main content area"""
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel
        left = self.build_left_panel(content)
        
        # Right panel (signup form)
        right = self.build_right_panel(content)
        
        return content
    
    def build_left_panel(self, parent):
        """Build the left decorative panel"""
        left = tk.Frame(parent, bg=FRAME, width=200, padx=10, pady=10, relief="solid", bd=1)
        left.pack(side="left", fill="y", padx=(0,20))
        left.pack_propagate(False)
        
        tk.Label(left, text="Let's get\nStarted!!", font=FONT_H2, bg=FRAME, fg=BROWN).pack(anchor="w")
        
        # Decorative canvas
        canvas_img = tk.Canvas(left, bg=FRAME, width=170, height=120, highlightthickness=0)
        canvas_img.pack(pady=6)
        canvas_img.create_rectangle(10,10,160,110, fill=BG, outline=SUBTEXT)
        canvas_img.create_text(85, 60, text="📚🖥️", font=("Segoe UI", 22))
        
        return left
    
    def build_right_panel(self, parent):
        """Build the right panel with signup form"""
        right = tk.Frame(parent, bg=FRAME, padx=24, pady=16, relief="solid", bd=1)
        right.pack(side="left", fill="both", expand=True)
        
        # Title
        tk.Label(right, text="SIGN-UP →", font=FONT_H2, bg=FRAME, fg=TEXT).pack(anchor="w")
        
        # Username field
        tk.Label(right, text="Username", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.signup_username = tk.Entry(right, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1)
        self.signup_username.pack(fill="x", ipady=5)
        
        # Password field
        tk.Label(right, text="Password", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.signup_password = tk.Entry(right, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, show="•")
        self.signup_password.pack(fill="x", ipady=5)
        
        # Buttons frame
        bot = tk.Frame(right, bg=FRAME)
        bot.pack(fill="x", pady=(12,0))
        
        # Signup button
        self.brown_btn(bot, "Sign-up", self.callbacks['on_signup'], width=10).pack(side="right")
        
        # Login link
        login_link = tk.Label(right, text="Already have an account? Log in", font=FONT_SMALL,
                 fg=BROWN, bg=FRAME, cursor="hand2")
        login_link.pack(anchor="e", pady=(4,0))
        login_link.bind("<Button-1>", lambda e: self.callbacks['on_back_to_login']())
        
        return right
    
    def get_form_data(self):
        """Get the username and password from form fields"""
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        return username, password
    
    def clear_form(self):
        """Clear the form fields"""
        if self.signup_username:
            self.signup_username.delete(0, tk.END)
        if self.signup_password:
            self.signup_password.delete(0, tk.END)
    
    def brown_btn(self, parent, text, cmd, width=12):
        """Create a brown themed button"""
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                        relief="flat", width=width, pady=6, cursor="hand2",
                        command=cmd)
    
    def clear_window(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()