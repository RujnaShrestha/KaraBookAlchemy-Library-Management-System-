import tkinter as tk
from tkinter import messagebox, ttk
from Uiconfig import *


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
class HomeUI:
    def __init__(self, root, backend, callbacks):
        self.root = root
        self.backend = backend
        self.callbacks = callbacks  # Contains on_logout, show_support, show_profile, show_settings, refresh_home
        
        self.search_entry = None
        self.genre_var = None
        self.books_frame = None
    
    def build_header(self, parent):
        """Build the header section"""
        hdr = tk.Frame(parent, bg=BG, pady=6)
        hdr.pack(fill="x")
        
        # Logo
        logo = tk.Frame(hdr, bg=FRAME, width=70, height=50, relief="solid", bd=1)
        logo.pack(side="left", padx=12)
        logo.pack_propagate(False)
        tk.Label(logo, text="KARA\n📚", font=("Segoe UI", 8, "bold"), bg=FRAME, fg=BROWN).pack(expand=True)
        
        # Welcome text
        tk.Label(hdr, text="WELCOME", font=FONT_TITLE, bg=BG, fg=TEXT).pack(side="left", padx=6)
        
        # Username display
        username_display = self.backend.current_user if self.backend.current_user else "Username"
        tk.Label(hdr, text=f" {username_display} ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
                 relief="solid", bd=1, padx=8, pady=4).pack(side="right", padx=12, pady=4)
        
        return hdr
    
    def build_search_bar(self, parent):
        """Build the search bar section"""
        search_bar = tk.Frame(parent, bg=BG, pady=4)
        search_bar.pack(fill="x", padx=100)
        
        self.search_entry = tk.Entry(search_bar, font=FONT_INPUT, bg=INPUT_BG, relief="solid", bd=1, width=36)
        self.search_entry.pack(side="left", ipady=4, padx=(0,4))
        
        self.brown_btn(search_bar, "search", self.callbacks['search_books'], width=7).pack(side="left")
        
        self.genre_var = tk.StringVar(value="All")
        genre_btn = tk.Button(search_bar, text="Genre ▾", font=FONT_SMALL, bg=FRAME, fg=TEXT,
                             relief="solid", bd=1, cursor="hand2", command=self.callbacks['show_genre_menu'])
        genre_btn.pack(side="left", padx=6, ipady=4)
        
        # Add Book button for admin
        if self.backend.current_user_type == "admin":
            add_btn = tk.Button(search_bar, text="+ Add Book", font=FONT_SMALL, bg=BROWN, fg=WHITE,
                               relief="flat", cursor="hand2", command=self.callbacks['show_add_book_dialog'])
            add_btn.pack(side="left", padx=6, ipady=4)
        
        return search_bar
    
    def build_sidebar(self, parent):
        """Build the navigation sidebar"""
        nav = tk.Frame(parent, bg=FRAME, width=90, pady=10)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        
        pages = [
            ("Home", self.callbacks['refresh_home']),
            ("Support", self.callbacks['show_support']),
            ("Profile", self.callbacks['show_profile']),
            ("Settings", self.callbacks['show_settings'] if self.callbacks['show_settings'] else None), 
            ("Log-out", self.callbacks['on_logout'])
        ]
        
        for name, cmd in pages:
            if cmd is None:
                continue
            fg = BROWN if name == "Home" else TEXT
            btn = tk.Button(nav, text=name, font=FONT_SMALL, bg=FRAME, fg=fg,
                           relief="flat", anchor="w", padx=8, pady=4,
                           cursor="hand2", command=cmd)
            btn.pack(fill="x", pady=1)
        
        return nav
    
    def build_main_area(self, parent):
        """Build the main content area with book display"""
        main_area = tk.Frame(parent, bg=FRAME, relief="solid", bd=1, padx=14, pady=10)
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
        
        return main_area
    
    def display_books(self, books=None):
        """Display books in the UI"""
        for widget in self.books_frame.winfo_children():
            widget.destroy()
            
        if books is None:
            books = self.backend.get_all_books()
        
        if not books:
            no_books = tk.Label(self.books_frame, text="No books found.", bg=FRAME, fg=TEXT)
            no_books.pack(pady=20)
            return
        
        row = None
        for i, book in enumerate(books):
            if i % 3 == 0:
                row = tk.Frame(self.books_frame, bg=FRAME)
                row.pack(fill="x", pady=10)
            
            self.create_book_card(row, book, i)
    
    def create_book_card(self, parent, book, index):
        """Create a single book card"""
        color = BOOK_COLORS[index % len(BOOK_COLORS)]
        card = tk.Frame(parent, bg=color, width=180, height=200, relief="raised", bd=2)
        card.pack(side="left", padx=10, expand=True)
        card.pack_propagate(False)
        
        # Book details
        tk.Label(card, text=book[1][:20], font=("Segoe UI", 9, "bold"),
                bg=color, fg=WHITE, wraplength=160).pack(pady=(10,5))
        
        tk.Label(card, text=f"by {book[2][:15]}", font=("Segoe UI", 7),
                bg=color, fg=WHITE).pack()
        
        tk.Label(card, text=f"[{book[3]}]", font=("Segoe UI", 6, "italic"),
                bg=color, fg=WHITE).pack()
        
        # Action buttons based on user type
        if self.backend.current_user_type == "user":
            add_btn = tk.Button(card, text="📚 Add to List", font=("Segoe UI", 7, "bold"),
                               bg=WHITE, fg=BROWN, relief="flat", cursor="hand2",
                               command=lambda b=book: self.callbacks['add_to_list'](b))
            add_btn.pack(pady=(5,2))
            
            reserve_btn = tk.Button(card, text="🔖 Reserve", font=("Segoe UI", 7, "bold"),
                                   bg="#FFD700", fg=BROWN, relief="flat", cursor="hand2",
                                   command=lambda b=book: self.callbacks['reserve'](b))
            reserve_btn.pack(pady=(0,5))
        
        elif self.backend.current_user_type == "admin":
            del_btn = tk.Button(card, text="❌ Delete", font=("Segoe UI", 7, "bold"),
                               bg="#8B3A3A", fg=WHITE, relief="flat", cursor="hand2",
                               command=lambda b=book: self.callbacks['delete'](b))
            del_btn.pack(pady=(5,2))
    
    def show_genre_menu(self, genres, on_select):
        """Show genre selection menu"""
        menu = tk.Toplevel(self.root)
        menu.title("Genre")
        menu.geometry("150x200")
        menu.configure(bg=FRAME)
        
        for g in genres:
            tk.Button(menu, text=g, bg=FRAME, command=lambda g=g: on_select(g)).pack(fill="x", pady=2)
    
    def show_add_book_dialog(self, on_save):
        """Show dialog to add a new book"""
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
                on_save(title.get(), author.get(), genre.get(), dialog)
            else:
                messagebox.showerror("Error", "Fill all fields!")
        
        tk.Button(dialog, text="Save", bg=BROWN, fg=WHITE, command=save).pack(pady=10)
    
    def brown_btn(self, parent, text, cmd, width=12):
        """Create a brown themed button"""
        return tk.Button(parent, text=text, font=FONT_BTN, bg=BROWN, fg=WHITE,
                        relief="flat", width=width, pady=6, cursor="hand2",
                        command=cmd)
    
    def clear_window(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()