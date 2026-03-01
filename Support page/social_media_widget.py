import tkinter as tk
from tkinter import messagebox
from constantUI import *

class SocialMediaWidget:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        """Display social media icons"""
        social = tk.Frame(self.parent, bg=BG)
        social.pack(fill="x", padx=80)

        social_media = [
            ("in", "LinkedIn"), 
            ("f", "Facebook"), 
            ("IG", "Instagram"),
            ("TT", "Twitter"), 
            ("𝕏", "X")
        ]

        for icon, platform in social_media:
            label = tk.Label(
                social, text=icon, font=("Segoe UI",10,"bold"), 
                bg=FRAME, fg=TEXT, width=3, relief="solid", bd=1, 
                cursor="hand2"
            )
            label.pack(side="right", padx=2, pady=2)
            label.bind(
                "<Button-1>", 
                lambda e, p=platform: self._on_click(p)
            )

    def _on_click(self, platform):
        """Handle social media icon click"""
        messagebox.showinfo(
            "Social Media",
            f"Our username on {platform} is: karabook_alchemy"
        )