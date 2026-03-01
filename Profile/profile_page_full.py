import tkinter as tk
from tkinter import ttk
from constantUI import *
from profile_pg import ProfilePageBase
from profile_admin import AdminProfileView
from profile_readinglist import ReadingListManager
from profile_reservations import ReservationManager

class ProfilePage(ProfilePageBase):
    def __init__(self, root, db_manager, current_user, current_user_type,
                 show_home, show_support, show_settings, on_logout):
        super().__init__(root, db_manager, current_user, current_user_type,
                        show_home, show_support, show_settings, on_logout)
        self.reading_list_mgr = None
        self.reservation_mgr = None

    def show(self):
        """Show profile page"""
        self.clear_window()
        self.root.configure(bg=BG)

        # Create header
        self._create_header()

        # Main body with sidebar
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=8)
        
        # Create navigation sidebar
        self._create_nav(body, "Profile")

        # Main content area
        main_area = tk.Frame(body, bg=FRAME, relief="solid", bd=1, padx=14, pady=10)
        main_area.pack(side="left", fill="both", expand=True, padx=8, pady=4)

        # Show appropriate profile based on user type
        if self.current_user_type == "admin":
            self._show_admin_profile(main_area)
        else:
            self._show_user_profile(main_area)

    def _show_admin_profile(self, parent):
        """Show admin profile with all reservations"""
        admin_view = AdminProfileView(parent, self.db)
        admin_view.show()

    def _show_user_profile(self, parent):
        """Show user profile with tabs for reading list and reservations"""
        # Create notebook for tabs
        style = ttk.Style()
        style.configure("TNotebook", background=FRAME)
        style.configure("TNotebook.Tab", background=FRAME, padding=[10, 2])
        
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        # Reading List tab
        read_frame = tk.Frame(notebook, bg=FRAME)
        notebook.add(read_frame, text="Reading List")
        
        self.reading_list_mgr = ReadingListManager(
            read_frame, self.db, self.current_user, self.show
        )
        self.reading_list_mgr.display()

        # Reserved tab
        res_frame = tk.Frame(notebook, bg=FRAME)
        notebook.add(res_frame, text="Reserved")
        
        self.reservation_mgr = ReservationManager(
            res_frame, self.db, self.current_user, self.show
        )
        self.reservation_mgr.display()