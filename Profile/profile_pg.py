import tkinter as tk
from constantUI import *

class ProfilePageBase:
    def __init__(self, root, db_manager, current_user, current_user_type,
                 show_home, show_support, show_settings, on_logout):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        self.current_user_type = current_user_type
        self.show_home = show_home
        self.show_support = show_support
        self.show_settings = show_settings
        self.on_logout = on_logout

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_header(self):
        """Create the profile page header"""
        hdr = tk.Frame(self.root, bg=BG, pady=8)
        hdr.pack(fill="x")

        # Avatar
        av = tk.Canvas(hdr, width=60, height=60, bg=FRAME, highlightthickness=1,
                       highlightbackground=SUBTEXT)
        av.pack(side="left", padx=14)
        av.create_oval(8,8,52,52, fill=BG, outline=SUBTEXT)
        av.create_text(30,30, text="👤", font=("Segoe UI",20))

        # Username
        tk.Label(hdr, text=self.current_user, font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left")

        # User dropdown indicator
        username_display = self.current_user
        tk.Label(
            hdr, text=f" {username_display} ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
            relief="solid", bd=1, padx=8, pady=4
        ).pack(side="right", padx=12, pady=4)
        
        return hdr

    def _create_nav(self, parent, current):
        """Create navigation sidebar"""
        nav = tk.Frame(parent, bg=FRAME, width=90, pady=10)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)

        pages = [
            ("Home", self.show_home),
            ("Support", self.show_support),
            ("Profile", lambda: None),  # Will be overridden
            ("Settings", self.show_settings if self.show_settings else None),
            ("Log-out", self.on_logout)
        ]

        for name, cmd in pages:
            if cmd is None:
                continue
            fg = BROWN if name == "Profile" else TEXT
            btn = tk.Button(
                nav, text=name, font=FONT_SMALL, bg=FRAME, fg=fg,
                relief="flat", anchor="w", padx=8, pady=4,
                cursor="hand2", command=cmd
            )
            btn.pack(fill="x", pady=1)
        
        return nav