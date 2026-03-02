import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui_config import *

class UserLoginFrame:
    def __init__(self, root, db_manager, on_login_success, on_show_forget):
        self.root = root
        self.db = db_manager
        self.on_login_success = on_login_success
        self.on_show_forget = on_show_forget
        self.login_username = None
        self.login_password = None
    
    def show(self, parent_frame):
        """Show user login frame"""
        
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        tk.Label(parent_frame, text="LOGIN →", font=FONT_BTN, bg=FRAME, fg=TEXT).pack(anchor="w")
        
        tk.Label(parent_frame, text="Username", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.login_username = tk.Entry(parent_frame, font=FONT_INPUT, bg=FRAME, relief="solid", bd=1)
        self.login_username.pack(fill="x", ipady=5)
        
        tk.Label(parent_frame, text="Password", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.login_password = tk.Entry(parent_frame, font=FONT_INPUT, bg=FRAME, relief="solid", bd=1, show="•")
        self.login_password.pack(fill="x", ipady=5)
        
        bot = tk.Frame(parent_frame, bg=FRAME)
        bot.pack(fill="x", pady=(12,0))
        
        forget_label = tk.Label(bot, text="Forget password?", font=FONT_SMALL, fg=BROWN, bg=FRAME, cursor="hand2")
        forget_label.pack(side="left")
        forget_label.bind("<Button-1>", lambda e: self.on_show_forget())
        
        self.brown_btn(bot, "login", self.login, width=8).pack(side="right")
    
    def login(self):
        """Handle user login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            
            if user:
                self.on_login_success(username, user[0], "user")
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Login failed: {e}")
    
    def brown_btn(self, parent, text, cmd, width=12):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                         relief="flat", width=width, pady=6, cursor="hand2",
                         command=cmd)