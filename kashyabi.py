# kashyabi.py
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random
from datetime import datetime

# Color Scheme
BG = "#CEC1A8"
FRAME = "#F1EADA"
BROWN = "#584738"
TEXT = "#2C1A0E"
SUBTEXT = "#7A6550"
WHITE = "#FFFFFF"
INPUT_BG = "#F1EADA"

FONT_TITLE = ("Georgia", 18, "bold")
FONT_H2 = ("Georgia", 13, "bold")
FONT_NAV = ("Segoe UI", 10)
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN = ("Segoe UI", 10, "bold")
FONT_INPUT = ("Segoe UI", 10)

BOOK_COLORS = ["#4B6E3A","#2E5B8A","#8A3A2E","#5A2E8A",
               "#2E7A5B","#8A6E2E","#3A5B8A","#6E2E5B"]

class HomePage:
    def __init__(self, root, db_manager, current_user, current_user_type, 
                 on_nav, on_logout, show_support, show_profile, show_settings):
        self.root = root
        self.db = db_manager
        self.current_user = current_user
        self.current_user_type = current_user_type
        self.on_nav = on_nav
        self.on_logout = on_logout
        self.show_support = show_support
        self.show_profile = show_profile
        self.show_settings = show_settings
        
        self.search_entry = None
        self.genre_var = None
        self.books_frame = None
    
    def show(self):
        """Show home page"""
        self.clear_window()
        self.root.configure(bg=BG)

        # Header
        hdr = tk.Frame(self.root, bg=BG, pady=6)
        hdr.pack(fill="x")
        
        logo = tk.Frame(hdr, bg=FRAME, width=70, height=50, relief="solid", bd=1)
        logo.pack(side="left", padx=12)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 8, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        
        tk.Label(hdr, text="WELCOME", font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left", padx=6)
        
        username_display = self.current_user if self.current_user else "Username"
        tk.Label(hdr, text=f" {username_display} ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
                 relief="solid", bd=1, padx=8, pady=4).pack(side="right", padx=12, pady=4)

        # Search bar
        search_bar = tk.Frame(self.root, bg=BG, pady=4)
        search_bar.pack(fill="x", padx=100)
        
        self.search_entry = tk.Entry(search_bar, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, width=36)
        self.search_entry.pack(side="left", ipady=4, padx=(0,4))
        
        self.brown_btn(search_bar, "search", self.search_books, width=7).pack(side="left")
        
        self.genre_var = tk.StringVar(value="All")
        genre_btn = tk.Button(search_bar, text="Genre ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
                             relief="solid", bd=1, cursor="hand2", command=self.show_genre_menu)
        genre_btn.pack(side="left", padx=6, ipady=4)
        
        # Add Book button for admin
        if self.current_user_type == "admin":
            add_btn = tk.Button(search_bar, text="+ Add Book", font=FONT_SMALL, bg=BROWN, fg=WHITE,
                               relief="flat", cursor="hand2", command=self.show_add_book_dialog)
            add_btn.pack(side="left", padx=6, ipady=4)

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=8)
        
        # Sidebar
        nav = tk.Frame(body, bg=FRAME, width=90, pady=10)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        
        pages = [
            ("Home", self.show),
            ("Support", self.show_support),
            ("Profile", self.show_profile),
            ("Settings", self.show_settings if self.show_settings else None), 
            ("Log-out", self.on_logout)
        ]
        
        for name, cmd in pages:
            if cmd is None:
                continue
            fg = BROWN if name == "Home" else TEXT
            btn = tk.Button(nav, text=name, font=FONT_SMALL, bg=FRAME, fg=fg,
                           relief="flat", anchor="w", padx=8, pady=4,
                           cursor="hand2", command=cmd)
            btn.pack(fill="x", pady=1)

        # Main area
        main_area = tk.Frame(body, bg=FRAME, relief="solid", bd=1, padx=14, pady=10)
        main_area.pack(side="left", fill="both", expand=True, padx=8, pady=4)

        tk.Label(main_area, text="Books Available in the Library", font=FONT_H2, 
                bg=FRAME, fg=TEXT).pack(anchor="w", pady=(0,8))

        # Books display with scroll
        canvas_frame = tk.Frame(main_area, bg=FRAME)
        canvas_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=FRAME, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.books_frame = tk.Frame(canvas, bg=FRAME)
        
        self.books_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.books_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.display_books()

    def display_books(self, books=None):
        """Display books"""
        for widget in self.books_frame.winfo_children():
            widget.destroy()
            
        if books is None:
            try:
                cursor = self.db.get_cursor()
                cursor.execute("SELECT * FROM books")
                books = cursor.fetchall()
            except:
                books = []
        
        if not books:
            no_books = tk.Label(self.books_frame, text="No books found.", bg=FRAME, fg=TEXT)
            no_books.pack(pady=20)
            return
        
        row = None
        for i, book in enumerate(books):
            if i % 3 == 0:
                row = tk.Frame(self.books_frame, bg=FRAME)
                row.pack(fill="x", pady=10)
            
            # Book card
            color = BOOK_COLORS[i % len(BOOK_COLORS)]
            card = tk.Frame(row, bg=color, width=180, height=200, relief="raised", bd=2)
            card.pack(side="left", padx=10, expand=True)
            card.pack_propagate(False)
            
            tk.Label(card, text=book[1][:20], font=("Segoe UI", 9, "bold"),
                    bg=color, fg=WHITE, wraplength=160).pack(pady=(10,5))
            
            tk.Label(card, text=f"by {book[2][:15]}", font=("Segoe UI", 7),
                    bg=color, fg=WHITE).pack()
            
            tk.Label(card, text=f"[{book[3]}]", font=("Segoe UI", 6, "italic"),
                    bg=color, fg=WHITE).pack()
            
            if self.current_user_type == "user":
                add_btn = tk.Button(card, text="📚 Add to List", font=("Segoe UI", 7, "bold"),
                                   bg=WHITE, fg=BROWN, relief="flat", cursor="hand2",
                                   command=lambda b=book: self.add_to_reading_list(b))
                add_btn.pack(pady=(5,2))
                
                reserve_btn = tk.Button(card, text="🔖 Reserve", font=("Segoe UI", 7, "bold"),
                                       bg="#FFD700", fg=BROWN, relief="flat", cursor="hand2",
                                       command=lambda b=book: self.reserve_book(b))
                reserve_btn.pack(pady=(0,5))
            
            elif self.current_user_type == "admin":
                del_btn = tk.Button(card, text="❌ Delete", font=("Segoe UI", 7, "bold"),
                                   bg="#8B3A3A", fg=WHITE, relief="flat", cursor="hand2",
                                   command=lambda b=book: self.delete_book(b))
                del_btn.pack(pady=(5,2))

    def add_to_reading_list(self, book):
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("SELECT reading_list FROM users WHERE username=?", (self.current_user,))
            result = cursor.fetchone()
            reading_list = result[0] if result[0] else ""
            
            if str(book[0]) in reading_list:
                messagebox.showinfo("Info", f"'{book[1]}' already in your list!")
                return
            
            new_list = reading_list + f",{book[0]}" if reading_list else str(book[0])
            cursor.execute("UPDATE users SET reading_list=? WHERE username=?", 
                               (new_list, self.current_user))
            conn.commit()
            messagebox.showinfo("Success", f"'{book[1]}' added to your list!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def reserve_book(self, book):
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT * FROM reservations WHERE book_id=? AND status='reserved'", (book[0],))
            if cursor.fetchone():
                messagebox.showinfo("Info", f"'{book[1]}' already reserved!")
                return
            
            cursor.execute("INSERT INTO reservations (book_id, book_title, username, reserved_date) VALUES (?,?,?,?)",
                               (book[0], book[1], self.current_user, date))
            conn.commit()
            messagebox.showinfo("Success", f"'{book[1]}' reserved!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def delete_book(self, book):
        if messagebox.askyesno("Delete", f"Delete '{book[1]}'?"):
            try:
                cursor = self.db.get_cursor()
                conn = self.db.get_connection()
                cursor.execute("DELETE FROM books WHERE id=?", (book[0],))
                conn.commit()
                self.show()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed: {e}")

    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("300x250")
        dialog.configure(bg=FRAME)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Book", font=FONT_H2, bg=FRAME, fg=BROWN).pack(pady=10)
        
        tk.Label(dialog, text="Title:", bg=FRAME).pack()
        title = tk.Entry(dialog, width=30)
        title.pack(pady=5)
        
        tk.Label(dialog, text="Author:", bg=FRAME).pack()
        author = tk.Entry(dialog, width=30)
        author.pack(pady=5)
        
        tk.Label(dialog, text="Genre:", bg=FRAME).pack()
        genre = ttk.Combobox(dialog, values=["Fantasy","Fiction","Romance","Horror","Thriller","Sci-Fi"])
        genre.pack(pady=5)
        
        def save():
            if title.get() and author.get() and genre.get():
                cursor = self.db.get_cursor()
                conn = self.db.get_connection()
                cursor.execute("INSERT INTO books (title, author, genre) VALUES (?,?,?)",
                                   (title.get(), author.get(), genre.get()))
                conn.commit()
                dialog.destroy()
                self.show()
            else:
                messagebox.showerror("Error", "Fill all fields!")
        
        tk.Button(dialog, text="Save", bg=BROWN, fg=WHITE, command=save).pack(pady=10)

    def show_genre_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Genre")
        menu.geometry("150x200")
        menu.configure(bg=FRAME)
        
        genres = ["All","Fantasy","Fiction","Romance","Horror","Thriller","Sci-Fi"]
        for g in genres:
            tk.Button(menu, text=g, bg=FRAME, command=lambda g=g: self.select_genre(g)).pack(fill="x", pady=2)
    
    def select_genre(self, genre):
        self.genre_var.set(genre)
        self.search_books()

    def search_books(self):
        query = self.search_entry.get().strip()
        genre = self.genre_var.get()
        
        try:
            cursor = self.db.get_cursor()
            if query and genre != "All":
                cursor.execute("SELECT * FROM books WHERE title LIKE ? AND genre=?", 
                                   (f'%{query}%', genre))
            elif query:
                cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{query}%',))
            elif genre != "All":
                cursor.execute("SELECT * FROM books WHERE genre=?", (genre,))
            else:
                cursor.execute("SELECT * FROM books")
            
            self.display_books(cursor.fetchall())
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def brown_btn(self, parent, text, cmd, width=12):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                        relief="flat", width=width, pady=6, cursor="hand2",
                        command=cmd)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class SignupPage:
    def __init__(self, root, db_manager, on_signup_success, on_back_to_login):
        self.root = root
        self.db = db_manager
        self.on_signup_success = on_signup_success
        self.on_back_to_login = on_back_to_login
        
        self.signup_username = None
        self.signup_password = None
    
    def show(self):
        """Show signup page"""
        self.clear_window()
        self.logo_header()
        
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        left = tk.Frame(content, bg=FRAME, width=200, padx=10, pady=10, relief="solid", bd=1)
        left.pack(side="left", fill="y", padx=(0,20))
        left.pack_propagate(False)
        tk.Label(left, text="Let's get\nStarted!!", font=FONT_H2, bg=FRAME, fg=BROWN).pack(anchor="w")
        
        canvas_img = tk.Canvas(left, bg=FRAME, width=170, height=120, highlightthickness=0)
        canvas_img.pack(pady=6)
        canvas_img.create_rectangle(10,10,160,110, fill=BG, outline=SUBTEXT)
        canvas_img.create_text(85, 60, text="📚🖥️", font=("Segoe UI", 22))

        right = tk.Frame(content, bg=FRAME, padx=24, pady=16, relief="solid", bd=1)
        right.pack(side="left", fill="both", expand=True)
        tk.Label(right, text="SIGN-UP →", font=FONT_H2, bg=FRAME, fg=TEXT).pack(anchor="w")
        
        # Username
        tk.Label(right, text="Username", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.signup_username = tk.Entry(right, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1)
        self.signup_username.pack(fill="x", ipady=5)
        
        # Password
        tk.Label(right, text="Password", font=FONT_BODY, bg=FRAME, fg=TEXT).pack(anchor="w", pady=(8,2))
        self.signup_password = tk.Entry(right, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, show="•")
        self.signup_password.pack(fill="x", ipady=5)
        
        bot = tk.Frame(right, bg=FRAME)
        bot.pack(fill="x", pady=(12,0))
        
        self.brown_btn(bot, "Sign-up", self.signup, width=10).pack(side="right")
        
        login_link = tk.Label(right, text="Already have an account? Log in", font=FONT_SMALL,
                 fg=BROWN, bg=FRAME, cursor="hand2")
        login_link.pack(anchor="e", pady=(4,0))
        login_link.bind("<Button-1>", lambda e: self.on_back_to_login())
    
    def signup(self):
        """Handle user signup"""
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password too short!")
            return
        
        try:
            cursor = self.db.get_cursor()
            conn = self.db.get_connection()
            cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?,?,'user')",
                               (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created! Please login.")
            self.on_back_to_login()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Signup failed: {e}")
    
    def brown_btn(self, parent, text, cmd, width=12):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                        relief="flat", width=width, pady=6, cursor="hand2",
                        command=cmd)
    
    def logo_header(self):
        h = tk.Frame(self.root, bg=BG, pady=10)
        h.pack(fill="x")
        logo = tk.Frame(h, bg=FRAME, width=80, height=60, relief="solid", bd=1)
        logo.pack(side="left", padx=16)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 9, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        tk.Label(h, text="WELCOME TO\nKARA BOOK-ALCHEMY",
                 font=FONT_TITLE, bg=BG, fg=TEXT, justify="left").pack(side="left", padx=10)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ============= NEW AUTHENTICATION PAGE =============
class AuthPage:
    def __init__(self, root, db_manager, on_auth_success, on_back_to_login):
        self.root = root
        self.db = db_manager
        self.on_auth_success = on_auth_success
        self.on_back_to_login = on_back_to_login
        self.robot_var = None
        self.captcha_var = None
        self.captcha_text = None
        self.captcha_entry = None
    
    def show(self):
        """Show authentication page with I am not a robot and CAPTCHA"""
        self.clear_window()
        self.root.configure(bg=BG)
        
        # Center frame
        center = tk.Frame(self.root, bg=BG)
        center.pack(expand=True)
        
        # Card
        card = tk.Frame(center, bg=FRAME, padx=40, pady=30, relief="solid", bd=2)
        card.pack()
        
        tk.Label(card, text="Security Verification", font=FONT_TITLE,
                bg=FRAME, fg=BROWN).pack(pady=(0,20))
        
        # I am not a robot checkbox
        self.robot_var = tk.BooleanVar()
        robot_check = tk.Checkbutton(card, text="I am not a robot",
                                    variable=self.robot_var,
                                    bg=FRAME, font=FONT_H2,
                                    selectcolor=FRAME,
                                    padx=20, pady=10)
        robot_check.pack(pady=10)
        
        # Separator
        tk.Frame(card, bg=SUBTEXT, height=1).pack(fill="x", pady=15)
        
        # CAPTCHA verification
        tk.Label(card, text="CAPTCHA Verification", font=FONT_H2,
                bg=FRAME, fg=TEXT).pack(pady=(0,10))
        
        # Generate random CAPTCHA
        self.generate_captcha()
        
        # CAPTCHA display
        captcha_frame = tk.Frame(card, bg=FRAME)
        captcha_frame.pack(pady=5)
        
        self.captcha_display = tk.Label(captcha_frame, text=self.captcha_text,
                                        font=("Courier", 16, "bold"),
                                        bg=WHITE, fg=BROWN,
                                        relief="solid", bd=1,
                                        width=10, height=2)
        self.captcha_display.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(captcha_frame, text="↻", font=FONT_BTN,
                               bg=FRAME, fg=BROWN,
                               relief="flat", cursor="hand2",
                               command=self.refresh_captcha)
        refresh_btn.pack(side="left", padx=5)
        
        # CAPTCHA entry
        tk.Label(card, text="Enter the code above:", bg=FRAME).pack(pady=(5,0))
        self.captcha_entry = tk.Entry(card, width=20, font=FONT_INPUT,
                                      bg=INPUT_BG, relief="solid", bd=1)
        self.captcha_entry.pack(pady=5, ipady=3)
        
        # Buttons
        btn_frame = tk.Frame(card, bg=FRAME)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Back to Login", font=FONT_SMALL,
                 bg=FRAME, fg=BROWN, relief="flat", cursor="hand2",
                 command=self.on_back_to_login).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Verify", font=FONT_BTN,
                 bg=BROWN, fg=WHITE, relief="flat", cursor="hand2",
                 width=10, command=self.verify).pack(side="left", padx=5)
    
    def generate_captcha(self):
        """Generate random CAPTCHA text"""
        import random
        import string
        # Generate a 6-character CAPTCHA (mix of letters and numbers)
        self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def refresh_captcha(self):
        """Refresh CAPTCHA"""
        self.generate_captcha()
        self.captcha_display.config(text=self.captcha_text)
        self.captcha_entry.delete(0, tk.END)
    
    def verify(self):
        """Verify robot checkbox and CAPTCHA"""
        # Check robot checkbox
        if not self.robot_var.get():
            messagebox.showerror("Error", "Please confirm you are not a robot!")
            return
        
        # Check CAPTCHA
        entered_captcha = self.captcha_entry.get().strip().upper()
        if entered_captcha != self.captcha_text:
            messagebox.showerror("Error", "Incorrect CAPTCHA! Please try again.")
            self.refresh_captcha()
            return
        
        # Both verifications passed
        messagebox.showinfo("Success", "Verification successful!")
        self.on_auth_success()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()