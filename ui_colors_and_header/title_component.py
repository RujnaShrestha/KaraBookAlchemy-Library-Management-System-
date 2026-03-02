import tkinter as tk
from ui_config import *

class Header:
    def __init__(self, root):
        self.root = root
    
    def create(self):
        """Create header"""
        h = tk.Frame(self.root, bg=BG, pady=10)
        h.pack(fill="x")
        logo = tk.Frame(h, bg=FRAME, width=80, height=60, relief="solid", bd=1)
        logo.pack(side="left", padx=16)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 9, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        tk.Label(h, text="WELCOME TO\nKARA BOOK-ALCHEMY",
                 font=FONT_TITLE, bg=BG, fg=TEXT, justify="left").pack(side="left", padx=10)
        
        return h