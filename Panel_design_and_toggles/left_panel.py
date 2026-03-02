import tkinter as tk
from ui_config import *

class LeftPanel:
    def __init__(self, root, on_show_signup):
        self.root = root
        self.on_show_signup = on_show_signup
    
    def create(self, parent):
        """Create left panel"""
        left = tk.Frame(parent, bg=FRAME, width=160, padx=16, pady=16, relief="solid", bd=1)
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
        
        return left