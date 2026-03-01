import tkinter as tk
from tkinter import messagebox
from constantUI import *

class SupportPageBase:
    def __init__(self, root, show_home, show_profile, show_settings, on_logout):
        self.root = root
        self.show_home = show_home
        self.show_profile = show_profile
        self.show_settings = show_settings
        self.on_logout = on_logout

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_header(self):
        """Create support page header"""
        hdr = tk.Frame(self.root, bg=BG, pady=8)
        hdr.pack(fill="x")
        
        # Logo
        logo = tk.Frame(hdr, bg=FRAME, width=70, height=50, relief="solid", bd=1)
        logo.pack(side="left", padx=12)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI",8,"bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        
        # Title
        tk.Label(hdr, text="Support", font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left", padx=8)
        
        # Contact button
        tk.Button(
            hdr, text="Contact Us", font=FONT_BTN, bg=BROWN, fg=WHITE,
            relief="flat", cursor="hand2",
            command=lambda: messagebox.showinfo("Contact", "📞 +977-98********")
        ).pack(side="right", padx=12, ipadx=8, ipady=4)
        
        return hdr

    def _create_nav(self, parent, current):
        """Create navigation sidebar"""
        nav = tk.Frame(parent, bg=FRAME, width=90, pady=10)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        
        pages = [
            ("Home", self.show_home),
            ("Support", lambda: None),  # Will be overridden
            ("Profile", self.show_profile),
            ("Settings", self.show_settings if self.show_settings else None),
            ("Log-out", self.on_logout)
        ]

        for name, cmd in pages:
            if cmd is None:
                continue
            fg = BROWN if name == current else TEXT
            btn = tk.Button(
                nav, text=name, font=FONT_SMALL, bg=FRAME, fg=fg,
                relief="flat", anchor="w", padx=8, pady=4,
                cursor="hand2", command=cmd,
                activebackground=BG, activeforeground=BROWN
            )
            btn.pack(fill="x", pady=1)
        
        return nav