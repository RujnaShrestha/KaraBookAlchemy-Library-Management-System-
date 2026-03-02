# admin_login_frame.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui_config import *

class AdminLoginFrame:
    def __init__(self, root, db_manager, on_login_success, on_show_forget):
        self.root = root
        self.db = db_manager
        self.on_login_success = on_login_success
        self.on_show_forget = on_show_forget
        self.admin_id = None
        self.admin_password = None
        self.admin_code = None
    
    def show(self, parent_frame):
        """Show admin login frame"""
        # Clear parent frame
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        tk.Label(parent_frame, text="Admin ID", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.admin_id = tk.Entry(parent_frame, font=FONT_INPUT, bg=FRAME, relief="solid", bd=1)
        self.admin_id.pack(fill="x", ipady=5)
        
        tk.Label(parent_frame, text="Admin Password", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.admin_password = tk.Entry(parent_frame, font=FONT_INPUT, bg=FRAME, relief="solid", bd=1, show="•")
        self.admin_password.pack(fill="x", ipady=5)
        
        tk.Label(parent_frame, text="Admin Code", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.admin_code = tk.Entry(parent_frame, font=FONT_INPUT, bg=FRAME, relief="solid", bd=1, show="•")
        self.admin_code.pack(fill="x", ipady=5)
        
        bot2 = tk.Frame(parent_frame, bg=FRAME)
        bot2.pack(fill="x", pady=(12,0))
        
        forget_label2 = tk.Label(bot2, text="Forget password?", font=FONT_SMALL, fg=BROWN, bg=FRAME, cursor="hand2")
        forget_label2.pack(side="left")
        forget_label2.bind("<Button-1>", lambda e: self.on_show_forget())
        
        self.brown_btn(bot2, "login", self.admin_login, width=8).pack(side="right")
    
    def admin_login(self):
        """Handle admin login"""
        admin_id = self.admin_id.get().strip()
        password = self.admin_password.get()
        code = self.admin_code.get().strip()
        
        if not admin_id or not password or not code:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM admins WHERE admin_id=? AND password=? AND admin_code=?",
                               (admin_id, password, code))
            admin = cursor.fetchone()
            
            if admin:
                self.on_login_success(admin_id, admin[0], "admin")
            else:
                messagebox.showerror("Error", "Invalid admin credentials!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Login failed: {e}")
    
    def brown_btn(self, parent, text, cmd, width=12):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                         relief="flat", width=width, pady=6, cursor="hand2",
                         command=cmd)