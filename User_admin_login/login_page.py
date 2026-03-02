# login_page.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui_config import *

class LoginPage:
    def __init__(self, root, db_manager, on_login_success, on_show_signup, on_show_forget):
        self.root = root
        self.db = db_manager
        self.on_login_success = on_login_success
        self.on_show_signup = on_show_signup
        self.on_show_forget = on_show_forget
        
        self.login_username = None
        self.login_password = None
        self.admin_id = None
        self.admin_password = None
        self.admin_code = None
        
        # Create instances of other pages
        from user_frame import UserLoginFrame
        from admin_frame import AdminLoginFrame
        self.user_login_frame = UserLoginFrame(root, db_manager, on_login_success, on_show_forget)
        self.admin_login_frame = AdminLoginFrame(root, db_manager, on_login_success, on_show_forget)
    
    def show(self):
        """Show login page with user/admin toggle"""
        self.clear_window()
        self.root.configure(bg=BG)
        self.logo_header()

        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Toggle buttons
        toggle = tk.Frame(content, bg=BG)
        toggle.pack(anchor="e", pady=(0,10))

        def set_user(): 
            user_btn.config(bg=BROWN, fg=WHITE)
            admin_btn.config(bg=FRAME, fg=TEXT)
            self.user_login_frame.show(login_frame)
            admin_frame.pack_forget()
            
        def set_admin(): 
            admin_btn.config(bg=BROWN, fg=WHITE)
            user_btn.config(bg=FRAME, fg=TEXT)
            self.admin_login_frame.show(admin_frame)
            login_frame.pack_forget()

        user_btn = tk.Button(toggle, text="User", font=FONT_BTN, bg=BROWN, fg=WHITE, 
                             relief="flat", width=10, command=set_user)
        admin_btn = tk.Button(toggle, text="Admin", font=FONT_BTN, bg=FRAME, fg=TEXT,  
                              relief="flat", width=10, command=set_admin)
        user_btn.pack(side="left")
        admin_btn.pack(side="left", padx=4)

        body = tk.Frame(content, bg=BG)
        body.pack(fill="both", expand=True)

        # Left panel
        left = tk.Frame(body, bg=FRAME, width=160, padx=16, pady=16, relief="solid", bd=1)
        left.pack(side="left", fill="y", padx=(0,20))
        left.pack_propagate(False)
        tk.Label(left, text="Join us", font=FONT_BTN, bg=FRAME, fg=BROWN).pack(anchor="w")
        tk.Frame(left, bg=BROWN, height=2).pack(fill="x", pady=4)
        tk.Label(left, text="Register to get access to millions of books.", font=FONT_SMALL,
                 bg=FRAME, fg=SUBTEXT, wraplength=130, justify="left").pack(anchor="w")
        
        signup_label = tk.Label(left, text="New Here? Sign-up", font=FONT_SMALL, fg=BROWN,
                 bg=FRAME, cursor="hand2")
        signup_label.pack(anchor="w", pady=(10,0))
        signup_label.bind("<Button-1>", lambda e: self.on_show_signup())

        
        login_frame = tk.Frame(body, bg=FRAME, padx=24, pady=20, relief="solid", bd=1)
        self.user_login_frame.show(login_frame)

        
        admin_frame = tk.Frame(body, bg=FRAME, padx=24, pady=20, relief="solid", bd=1)
        
        admin_frame.pack_forget()
    
    def brown_btn(self, parent, text, cmd, width=12):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                         relief="flat", width=width, pady=6, cursor="hand2",
                         command=cmd)
    
    def logo_header(self):
        h = tk.Frame(self.root, bg=BG, pady=10)
        h.pack(fill="x")
        logo = tk.Frame(h, bg=FRAME, width=80, height=60, relief="solid", bd=1)
        logo.pack(side="left", padx=16)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 9, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        tk.Label(h, text="WELCOME TO\nKARA BOOK-ALCHEMY",
                 font=FONT_TITLE, bg=BG, fg=TEXT, justify="left").pack(side="left", padx=10)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()