import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os


from gui.orders import create_orders
from gui.overdue import create_overdue
from gui.rental import create_dataentry


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iRENT")
        self.root.state("zoomed")

        self.create_layout()
        self.create_pages()
        self.create_sidebar()

        self.create_dashboard()
        self.create_dataentry_page()
        self.create_orders_page()
        self.create_overdue_page()

        self.pages["dashboard"].tkraise()

    def add_hover(self, btn, enter_bg, leave_bg, enter_fg=None, leave_fg=None):

        def on_enter(e):
            btn.config(bg=enter_bg)
            btn.config(cursor="hand2")
            if enter_fg:
                btn.config(fg=enter_fg)

        def on_leave(e):
            btn.config(bg=leave_bg)
            btn.config(cursor="")
            if leave_fg:
                btn.config(fg=leave_fg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def create_layout(self):

        header = tk.Frame(
            self.root,
            bg="#ffd735",
            height=60
        )
        header.pack(side="top", fill="x")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(BASE_DIR, "assets", "iRENT_logo3.png")

        img = Image.open(logo_path)
        img.thumbnail((150, 150))

        self.logo = ImageTk.PhotoImage(img)

        logo_label = tk.Label(header, image=self.logo, bg="#ffd735")
        logo_label.pack(side="left", padx=20, pady=15)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

        self.left = tk.Frame(main_frame, bg="#313338", width=300)
        self.left.grid(row=0, column=0, sticky="ns")

        self.right = tk.Frame(main_frame, width=800, bg="#ffffff")
        self.right.grid(row=0, column=1, sticky="nsew")
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_columnconfigure(0, weight=1)
        
    def create_pages(self):
        self.pages = {}

        for name in ["dashboard","dataentry", "orders", "order_details", "history", "devices", "overdue"]:
            frame = tk.Frame(self.right)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[name] = frame

            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

    def create_sidebar(self):
        search_box = tk.LabelFrame(self.left, bg="#313338", bd=0)
        search_box.pack(pady=20, fill="x")

        tk.Label(
            search_box,
            text="Search",
            bg="#313338",
            fg="white",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(padx=10, fill="x")

        tk.Entry(
            search_box,
            font=("Arial", 12),
            width=28,
            bg="#313338",
            fg="white",
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2,
            insertbackground="white"
        ).pack(pady=(5, 40), padx=10, ipady=6, anchor="w")

        buttons = [
            ("Dashboard", "dashboard"),
            ("Create Rental", "dataentry"),
            ("View Rental Orders", "orders"),
            ("View Overdue Rentals", "overdue"),
            ("View Rental History", "history"),
            ("View List of Devices", "devices")
        ]

        for text, page in buttons:
            btn = tk.Button(
                search_box,
                text=text,
                bg="#ffd735",
                fg="black",
                width=25,
                font=("Arial", 12, "bold"),
                cursor="hand2",
                command=lambda p=page: self.pages[p].tkraise()
            )
            btn.pack(pady=15, padx=10, ipady=6, anchor="w")

            self.add_hover(
                btn,
                enter_bg="#232624",
                leave_bg="#ffd735",
                enter_fg="#ffd735",
                leave_fg="black"
            )

    def create_orders_page(self):
        create_orders(self.pages["orders"], self)

    def create_overdue_page(self):
        create_overdue(self.pages["overdue"], self)

    def create_dataentry_page(self):
        create_dataentry(self.pages["dataentry"], self)

    def create_dashboard(self):
        frame = tk.LabelFrame(
            self.pages["dashboard"],
            relief="flat",
            labelanchor="n",
            bd=0,
            bg ="#eef2f7"
        )

        frame.grid(row=0,column=0, sticky="nsew", padx=20, pady=20)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0) 
        frame.grid_columnconfigure(2, weight=0) 
        frame.grid_columnconfigure(3, weight=0) 
        frame.grid_columnconfigure(4, weight=1)

        tk.Label (
            frame,
            text="Welcome, admin!",
            font=("Arial", 24, "bold"),
            bg ="#eef2f7",
            fg="black"
        ).grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="w")

        self.create_card(frame, "#5CB85C", "active.png", "5", "Active Rentals", 1, row=1)
        self.create_card(frame, "#D9534F", "overdue.png", "5", "Overdue Rentals", 2, row=1)
        self.create_card(frame, "#ebc427", "available.png", "5", "Available for Rent", 3, row=1)
        self.create_card(frame, "#675DB7", "device.png", "5", "Total Devices", 1, row=2)
        self.create_card(frame, "#337AB7", "customers.png", "5", "Total Rentees", 2, row=2)
        self.create_card(frame, "#888E93", "employees.png", "5", "Total Employees", 3, row=2)




    def create_card(self, parent, color, icon_name, number, title, column, row=1):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(BASE_DIR, "assets", icon_name)
        icon = ImageTk.PhotoImage(Image.open(icon_path).resize((90, 90)))
        
        if not hasattr(self, 'icons'): self.icons = []
        self.icons.append(icon) 

        card = tk.Frame(
            parent,
            bg=color,
            width=200,
            height=200,
            highlightbackground="black",
            highlightthickness=2
        )
        card.grid(row=row, column=column, sticky="n", padx=23, pady=17)
        card.pack_propagate(False)

        tk.Label(card, image=icon, bg=color).pack(pady=(15, 5))

        tk.Label(
            card,
            text=number,
            font=("Arial", 25, "bold"),
            fg="white",
            bg=color
        ).pack()

        tk.Label(
            card, 
            text=title, 
            font=("Arial", 13, "bold", "italic"), 
            fg="white", 
            bg=color
        ).pack(pady=(0, 20))
