import tkinter as tk
from ui_config import *

class ToggleButtons:
    def __init__(self, root, on_user_select, on_admin_select):
        self.root = root
        self.on_user_select = on_user_select
        self.on_admin_select = on_admin_select
        self.user_btn = None
        self.admin_btn = None
    
    def create(self, parent):
        """Create toggle buttons"""
        toggle = tk.Frame(parent, bg=BG)
        toggle.pack(anchor="e", pady=(0,10))

        def set_user(): 
            self.user_btn.config(bg=BROWN, fg=WHITE)
            self.admin_btn.config(bg=FRAME, fg=TEXT)
            self.on_user_select()
            
        def set_admin(): 
            self.admin_btn.config(bg=BROWN, fg=WHITE)
            self.user_btn.config(bg=FRAME, fg=TEXT)
            self.on_admin_select()

        self.user_btn = tk.Button(toggle, text="User", font=FONT_BTN, bg=BROWN, fg=WHITE, 
                             relief="flat", width=10, command=set_user)
        self.admin_btn = tk.Button(toggle, text="Admin", font=FONT_BTN, bg=FRAME, fg=TEXT,  
                              relief="flat", width=10, command=set_admin)
        self.user_btn.pack(side="left")
        self.admin_btn.pack(side="left", padx=4)
        
        return toggle