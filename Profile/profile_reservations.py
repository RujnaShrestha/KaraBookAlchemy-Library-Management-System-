import tkinter as tk
from tkinter import messagebox
import sqlite3
from constantUI import *

class ReservationManager:
    def __init__(self, parent, db, username, refresh_callback):
        self.parent = parent
        self.db = db
        self.username = username
        self.refresh_callback = refresh_callback

    def display(self):
        """Display user's reserved books with cancel option"""
        cursor = self.db.get_cursor()
        cursor.execute(
            "SELECT * FROM reservations WHERE username=? AND status='reserved'", 
            (self.username,)
        )
        reservations = cursor.fetchall()
        
        if reservations:
            for r in reservations:
                self._create_reservation_item(r)
        else:
            tk.Label(self.parent, text="No reserved books.", bg=FRAME, fg=TEXT).pack(pady=10)

    def _create_reservation_item(self, reservation):
        """Create a reservation item with cancel button"""
        res_item_frame = tk.Frame(self.parent, bg=FRAME)
        res_item_frame.pack(fill="x", pady=2, padx=5)
        
        tk.Label(res_item_frame, text=f"📖 {reservation[2]}", bg=FRAME, fg=BROWN).pack(side="left")
        tk.Label(res_item_frame, text=f"  (📅 {reservation[4]})", bg=FRAME, fg=TEXT).pack(side="left")
        
        cancel_btn = tk.Button(
            res_item_frame, text="Cancel", bg="#8B3A3A", fg=WHITE,
            font=FONT_SMALL, relief="flat", cursor="hand2",
            command=lambda res_id=reservation[0]: self.cancel_reservation(res_id)
        )
        cancel_btn.pack(side="right", padx=5)

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation"""
        if messagebox.askyesno("Confirm Cancel", "Cancel this reservation?"):
            try:
                cursor = self.db.get_cursor()
                conn = self.db.get_connection()
                
                # Delete the reservation
                cursor.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
                conn.commit()
                
                messagebox.showinfo("Success", "Reservation cancelled.")
                self.refresh_callback()
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to cancel reservation: {e}")