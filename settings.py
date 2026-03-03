# settings_page.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from apekshya import BG, FRAME, BROWN, TEXT, SUBTEXT, WHITE, INPUT_BG
from apekshya import FONT_TITLE, FONT_H2, FONT_SMALL, FONT_BTN, FONT_BODY, FONT_INPUT

class SettingsPage:
    def __init__(self, root, db_manager, current_user, on_nav_callback, on_update_user):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        self.on_nav = on_nav_callback
        self.on_update_user = on_update_user
        
        self.new_email_entry = None
        self.new_password_entry = None
        self.confirm_password_entry = None
        self.new_username_entry = None
    
    def show(self):
        """Show settings page"""
        self.clear_window()
        self.root.configure(bg=BG)

        hdr = tk.Frame(self.root, bg=BG, pady=10)
        hdr.pack(fill="x")
        av = tk.Canvas(hdr, width=56, height=56, bg=FRAME, highlightthickness=1,
                       highlightbackground=SUBTEXT)
        av.pack(side="left", padx=14)
        av.create_oval(6,6,50,50, fill=BG, outline=SUBTEXT)
        av.create_text(28,28, text="👤", font=("Segoe UI",18))
        tk.Label(hdr, text="Settings", font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left", padx=8)
        
        username_display = self.current_user if self.current_user else "Username"
        tk.Label(hdr, text=f" {username_display} ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
                 relief="solid", bd=1, padx=8, pady=4).pack(side="right", padx=12, pady=4)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=8)
        self.create_nav(body, "Settings")

        main_area = tk.Frame(body, bg=FRAME, relief="solid", bd=1, padx=20, pady=16)
        main_area.pack(side="left", fill="both", expand=True, padx=8, pady=4)

        left_col = tk.Frame(main_area, bg=FRAME)
        left_col.pack(side="left", fill="both", expand=True, padx=(0,20))

        # Change email
        tk.Label(left_col, text="Change email", font=FONT_BODY, bg=FRAME, fg=TEXT, anchor="w").pack(fill="x", pady=(10,2))
        self.new_email_entry = tk.Entry(left_col, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1)
        self.new_email_entry.pack(fill="x", ipady=4)

        # Change password
        tk.Label(left_col, text="Change password", font=FONT_BODY, bg=FRAME, fg=TEXT, anchor="w").pack(fill="x", pady=(10,2))
        password_frame = tk.Frame(left_col, bg=FRAME)
        password_frame.pack(fill="x")
        self.new_password_entry = tk.Entry(password_frame, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, show="•")
        self.new_password_entry.pack(side="left", fill="x", expand=True, ipady=4)
        
        def toggle_new_pass():
            if self.new_password_entry.cget('show') == '':
                self.new_password_entry.config(show='•')
                new_pass_toggle.config(text="👁")
            else:
                self.new_password_entry.config(show='')
                new_pass_toggle.config(text="🔒")
        
        new_pass_toggle = tk.Button(password_frame, text="👁", font=("Segoe UI", 8), 
                                   bg=INPUT_BG, relief="flat", cursor="hand2",
                                   command=toggle_new_pass)
        new_pass_toggle.pack(side="right", padx=(2,0))

        # Confirm new password
        tk.Label(left_col, text="Confirm new password", font=FONT_BODY, bg=FRAME, fg=TEXT, anchor="w").pack(fill="x", pady=(10,2))
        confirm_frame = tk.Frame(left_col, bg=FRAME)
        confirm_frame.pack(fill="x")
        self.confirm_password_entry = tk.Entry(confirm_frame, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, show="•")
        self.confirm_password_entry.pack(side="left", fill="x", expand=True, ipady=4)
        
        def toggle_confirm_pass():
            if self.confirm_password_entry.cget('show') == '':
                self.confirm_password_entry.config(show='•')
                confirm_toggle.config(text="👁")
            else:
                self.confirm_password_entry.config(show='')
                confirm_toggle.config(text="🔒")
        
        confirm_toggle = tk.Button(confirm_frame, text="👁", font=("Segoe UI", 8), 
                                  bg=INPUT_BG, relief="flat", cursor="hand2",
                                  command=toggle_confirm_pass)
        confirm_toggle.pack(side="right", padx=(2,0))

        # Change username
        tk.Label(left_col, text="Change username", font=FONT_BODY, bg=FRAME, fg=TEXT, anchor="w").pack(fill="x", pady=(10,2))
        self.new_username_entry = tk.Entry(left_col, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1)
        self.new_username_entry.pack(fill="x", ipady=4)

        btns = tk.Frame(left_col, bg=FRAME)
        btns.pack(fill="x", pady=(14,0))
        tk.Button(btns, text="CANCEL", font=FONT_BTN, bg=FRAME, fg=BROWN,
                  relief="solid", bd=1, cursor="hand2", command=lambda: self.on_nav("Home")()).pack(side="left", padx=(0,8), ipadx=10, ipady=4)
        self.brown_btn(btns, "SAVE", self.save_settings, width=8).pack(side="left")

        right_col = tk.Frame(main_area, bg=FRAME, width=140)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)
        av2 = tk.Canvas(right_col, width=80, height=80, bg=FRAME, highlightthickness=1,
                        highlightbackground=SUBTEXT)
        av2.pack(pady=(10,14))
        av2.create_oval(6,6,74,74, fill=BG, outline=SUBTEXT)
        av2.create_text(40,40, text="👤", font=("Segoe UI",26))
        self.brown_btn(right_col, "CHANGE PROFILE", lambda: None, width=14).pack(pady=4)
        
        tk.Button(right_col, text="DELETE ACCOUNT", font=FONT_BTN, bg="#8B3A3A", fg=WHITE,
                  relief="flat", cursor="hand2", width=14, pady=6,
                  command=self.delete_account).pack()

    # ... rest of SettingsPage methods remain unchanged ...