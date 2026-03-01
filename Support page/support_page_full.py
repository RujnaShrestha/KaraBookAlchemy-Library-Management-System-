import tkinter as tk
from constantUI import *
from support_pg import SupportPageBase
from support_content import SupportContent
from social_media_widget import SocialMediaWidget

class SupportPage(SupportPageBase):
    def __init__(self, root, show_home, show_profile, show_settings, on_logout):
        super().__init__(root, show_home, show_profile, show_settings, on_logout)

    def show(self):
        """Show support page"""
        self.clear_window()
        self.root.configure(bg=BG)

        # Create header
        self._create_header()

        # Social media section
        social_widget = SocialMediaWidget(self.root)
        social_widget.display()

        # Main body with sidebar
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=8)
        
        # Create navigation
        self._create_nav(body, "Support")

        # Main content area
        main_area = tk.Frame(body, bg=FRAME, relief="solid", bd=1, padx=16, pady=14)
        main_area.pack(side="left", fill="both", expand=True, padx=8, pady=4)

        # Display support content
        content = SupportContent(main_area)
        content.display()