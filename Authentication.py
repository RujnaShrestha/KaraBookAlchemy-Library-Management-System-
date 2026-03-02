import tkinter as tk
from tkinter import messagebox
import random
import string
from Uiconfig import *

class AuthPage:
    def __init__(self, root, db_manager, on_auth_success, on_back_to_login):
        self.root = root
        self.db = db_manager
        self.on_auth_success = on_auth_success
        self.on_back_to_login = on_back_to_login
        self.robot_var = None
        self.captcha_var = None
        self.captcha_text = None
        self.captcha_entry = None
    
    def show(self):
        """Show authentication page with I am not a robot and CAPTCHA"""
        self.clear_window()
        self.root.configure(bg=BG)
        
        # Center frame
        center = tk.Frame(self.root, bg=BG)
        center.pack(expand=True)
        
        # Card
        card = tk.Frame(center, bg=FRAME, padx=40, pady=30, relief="solid", bd=2)
        card.pack()
        
        tk.Label(card, text="Security Verification", font=FONT_TITLE,
                bg=FRAME, fg=BROWN).pack(pady=(0,20))
        
        # I am not a robot checkbox
        self.robot_var = tk.BooleanVar()
        robot_check = tk.Checkbutton(card, text="I am not a robot",
                                    variable=self.robot_var,
                                    bg=FRAME, font=FONT_H2,
                                    selectcolor=FRAME,
                                    padx=20, pady=10)
        robot_check.pack(pady=10)
        
        # Separator
        tk.Frame(card, bg=SUBTEXT, height=1).pack(fill="x", pady=15)
        
        # CAPTCHA verification
        tk.Label(card, text="CAPTCHA Verification", font=FONT_H2,
                bg=FRAME, fg=TEXT).pack(pady=(0,10))
        
        # Generate random CAPTCHA
        self.generate_captcha()
        
        # CAPTCHA display
        captcha_frame = tk.Frame(card, bg=FRAME)
        captcha_frame.pack(pady=5)
        
        self.captcha_display = tk.Label(captcha_frame, text=self.captcha_text,
                                        font=("Courier", 16, "bold"),
                                        bg=WHITE, fg=BROWN,
                                        relief="solid", bd=1,
                                        width=10, height=2)
        self.captcha_display.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(captcha_frame, text="↻", font=FONT_BTN,
                               bg=FRAME, fg=BROWN,
                               relief="flat", cursor="hand2",
                               command=self.refresh_captcha)
        refresh_btn.pack(side="left", padx=5)
        
        # CAPTCHA entry
        tk.Label(card, text="Enter the code above:", bg=FRAME).pack(pady=(5,0))
        self.captcha_entry = tk.Entry(card, width=20, font=FONT_INPUT,
                                      bg=INPUT_BG, relief="solid", bd=1)
        self.captcha_entry.pack(pady=5, ipady=3)
        
        # Buttons
        btn_frame = tk.Frame(card, bg=FRAME)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Back to Login", font=FONT_SMALL,
                 bg=FRAME, fg=BROWN, relief="flat", cursor="hand2",
                 command=self.on_back_to_login).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Verify", font=FONT_BTN,
                 bg=BROWN, fg=WHITE, relief="flat", cursor="hand2",
                 width=10, command=self.verify).pack(side="left", padx=5)
    
    def generate_captcha(self):
        """Generate random CAPTCHA text"""
        # Generate a 6-character CAPTCHA (mix of letters and numbers)
        self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def refresh_captcha(self):
        """Refresh CAPTCHA"""
        self.generate_captcha()
        self.captcha_display.config(text=self.captcha_text)
        self.captcha_entry.delete(0, tk.END)
    
    def verify(self):
        """Verify robot checkbox and CAPTCHA"""
        # Check robot checkbox
        if not self.robot_var.get():
            messagebox.showerror("Error", "Please confirm you are not a robot!")
            return
        
        # Check CAPTCHA
        entered_captcha = self.captcha_entry.get().strip().upper()
        if entered_captcha != self.captcha_text:
            messagebox.showerror("Error", "Incorrect CAPTCHA! Please try again.")
            self.refresh_captcha()
            return
        
        # Both verifications passed
        messagebox.showinfo("Success", "Verification successful!")
        self.on_auth_success()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()