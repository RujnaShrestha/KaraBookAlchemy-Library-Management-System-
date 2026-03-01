import tkinter as tk
from constantUI import *
from profile_pg import ProfilePageBase

class AdminProfileView:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def show(self):
        """Display admin profile content"""
        tk.Label(self.parent, text="All Reservations", font=FONT_H2, bg=FRAME, fg=TEXT).pack(anchor="w")

        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM reservations WHERE status='reserved'")
        reservations = cursor.fetchall()

        if not reservations:
            tk.Label(self.parent, text="No reservations found.", bg=FRAME, fg=TEXT).pack(pady=10)
            return

        for r in reservations:
            self._create_reservation_card(r)

    def _create_reservation_card(self, reservation):
        """Create a reservation card for admin view"""
        f = tk.Frame(self.parent, bg=FRAME, relief="solid", bd=1)
        f.pack(fill="x", pady=5)
        tk.Label(f, text=f"📖 {reservation[2]}", bg=FRAME, fg=BROWN).pack(anchor="w", padx=10)
        tk.Label(
            f, text=f"👤 {reservation[3]}  |  📅 {reservation[4]}", 
            bg=FRAME, fg=TEXT
        ).pack(anchor="w", padx=10)