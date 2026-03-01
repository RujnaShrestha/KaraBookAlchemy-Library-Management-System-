import tkinter as tk
from constantUI import *

class SupportContent:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        """Display all support content"""
        # Title
        tk.Label(
            self.parent, text="KARA BOOK ALCHEMY SUPPORT SYSTEM",
            font=("Segoe UI", 11, "bold"), bg=FRAME, fg=BROWN
        ).pack(anchor="w")
        
        # Welcome message
        tk.Label(
            self.parent,
            text="Welcome to KARA Book-Alchemy, your digital e-library for books and learning resources.",
            font=FONT_SMALL, bg=FRAME, fg=TEXT, wraplength=700, justify="left"
        ).pack(anchor="w", pady=4)

        # Content sections
        sections = [
            ("About Us", "KARA Book-Alchemy is an online library that offers digital books and educational\n"
                         "materials for students and readers with access."),
            ("Privacy",  "We protect your personal data and guarantee the security of accessing your account.\n"
                         "User data is kept confidential and used only to improve your experience."),
            ("Support",  "For help with accounts, books, or technical issues:\n"
                         "✉ support@karabookalchemy.com\n📞 +977-98XXXXXXXX"),
        ]
        
        for heading, content in sections:
            self._create_section(heading, content)

    def _create_section(self, heading, content):
        """Create a content section"""
        tk.Label(
            self.parent, text=heading, font=("Segoe UI",10,"bold"), 
            bg=FRAME, fg=BROWN
        ).pack(anchor="w", pady=(8,2))
        
        tk.Label(
            self.parent, text=content, font=FONT_SMALL, bg=FRAME, fg=TEXT,
            justify="left", wraplength=700
        ).pack(anchor="w")