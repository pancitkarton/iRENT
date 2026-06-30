import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os

from db.dashboard_logic import get_dashboard_summary, welcome_staff
from gui.rentals import rentals_page
from gui.rentals import refresh_rental_list, get_rentals_by_status
from gui.add_rental import add_rental_page
from gui.customers import customers_page
from gui.list import create_list




class MainApp:
    def __init__(self, root, staff_id):
        self.root = root
        self.root.title("iRENT")
        self.root.state("zoomed")
        self.active_label = None

        self.staff_id = staff_id
        self.staff_name = welcome_staff(staff_id)

        self.refresh_tasks = {
            "dashboard": self.create_dashboard,
            "customers": self.create_customers_page,
            "rentals": self.create_rentals_page,
            "devices": self.create_list_page
        }

        self.create_layout()
        self.create_pages()
        self.create_sidebar()

        self.page_to_sidebar = {
            "dashboard": self.sidebar_labels[0],
            "rentals": self.sidebar_labels[1],
            "add_rental": self.sidebar_labels[1],
            "order_details": self.sidebar_labels[1],
            "customers": self.sidebar_labels[2],
            "devices": self.sidebar_labels[3]
        }

        self.create_dashboard()
        self.create_rentals_page()
        self.create_customers_page()
        self.create_list_page()

        self.set_active_page("dashboard")


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

        self.left = tk.Frame(main_frame, bg="#313338", width=250)
        self.left.pack_propagate(False)
        self.left.grid(row=0, column=0, sticky="ns")

        self.right = tk.Frame(main_frame, width=800, bg="#ffffff")
        self.right.grid(row=0, column=1, sticky="nsew")
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_columnconfigure(0, weight=1)
        
    def create_pages(self):
        self.pages = {}

        for name in ["dashboard", 
                     "rentals", 
                     "order_details", 
                     "add_rental", 
                     "customers", "customer_details", 
                     "devices", "brand_devices", "brand_details", "add_device", "edit_details", "add_device_type", "add_device_brand"]:
            frame = tk.Frame(self.right)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[name] = frame

            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        add_rental_page(self.pages["add_rental"], self)


    def create_sidebar(self):
        
        menu = tk.LabelFrame(self.left, bg="#313338", bd=0)
        menu.pack(pady=20, fill="x")

        tk.Label(
            menu,
            text="MENU",
            bg="#313338",
            fg="#ffd735",
            font=("Arial", 20, "bold"),
            anchor="w"
        ).pack(padx=20, pady=(0, 5), fill="x")

        tk.Frame(menu, height=2, bg="#ffd735").pack(fill="x", padx=15, pady=(0, 20))

        self.sidebar_labels = []


        buttons = [
            ("Home", "dashboard"),
            ("Rentals", "rentals"),
            ("Customers", "customers"),
            ("Devices", "devices"),
        ]

        for i, (text, page) in enumerate(buttons):
            label = tk.Label (
                menu,
                text=text,
                bg="#313338",
                fg="white",
                font=("Arial", 15, "bold"),
                anchor="w",
                cursor="hand2"
            )
            label.pack(pady=10, padx=20, fill="x")
            self.sidebar_labels.append(label)

            tk.Frame(menu, height=2, bg="#ffd735").pack(fill="x", padx=15)

            label.bind("<Button-1>", lambda e, p=page: self.set_active_page(p))

            def on_enter(e, l=label):
                if l != self.active_label:
                    l.config(fg="#ffd735")
            
            def on_leave(e, l=label):
                if l != self.active_label:
                    l.config(fg="white")

            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)

        bot_frame = tk.Frame(self.left, bg="#313338")
        bot_frame.pack(side="bottom", fill="x", pady=20)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logout_path = os.path.join(BASE_DIR, "assets", "logout.png")
        logout_icon = ImageTk.PhotoImage(Image.open(logout_path).resize((30, 30)))

        logout_btn = tk.Button(
            bot_frame,
            text="LOG OUT",
            font=("Arial", 15, "bold"),
            bg="#313338",
            fg="#F44336",
            relief="flat",
            cursor="hand2",
            image=logout_icon,
            compound="left",
            highlightthickness=0,
            activebackground="#313338",
            activeforeground="#ff4d4d",
            command=self.logout
        )
        logout_btn.image = logout_icon
        logout_btn.pack(padx=10, ipady=5, side="left")

        def on_enter(e):
            logout_btn.config(fg="#cc0000")

        def on_leave(e):
            logout_btn.config(fg="#F44336")

        logout_btn.bind("<Enter>", on_enter)
        logout_btn.bind("<Leave>", on_leave)

    def set_active_page(self, page_name):

        if page_name in self.refresh_tasks:
            for widget in self.pages[page_name].winfo_children():
                widget.destroy()
            
            self.refresh_tasks[page_name]()

        self.pages[page_name].tkraise()

        if self.active_label:
            self.active_label.config(bg="#313338", fg="white")

        self.active_label = self.page_to_sidebar.get(page_name, self.sidebar_labels[0])

        self.active_label.config(bg="#313338", fg="#ffd735")

    def logout(self):
        confirm = messagebox.askyesno(
            "Log Out",
            "Are you sure you want to log out?"
        )

        if confirm:
            self.root.destroy()

    def create_rentals_page(self):
        rentals_page(self.pages["rentals"], self)

    def create_customers_page(self):
        customers_page(self.pages["customers"], self, refresh_callback=None)

    def create_list_page(self):
        create_list(self.pages["devices"], self)


    def create_dashboard(self):

        for w in self.pages["dashboard"].winfo_children():
            w.destroy()

        stats = get_dashboard_summary()

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
            text=f"Welcome, {self.staff_name}!",
            font=("Arial", 24, "bold"),
            bg ="#eef2f7",
            fg="black"
        ).grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="w")

        self.create_card(
            frame, 
            "#ebc427", 
            "active.png", 
            str(stats["active"]), 
            "Ongoing Rentals", 
            1, 
            row=1
        )

        self.create_card(
            frame,
            "#D9534F", 
            "overdue.png", 
            str(stats["overdue"]), 
            "Overdue Rentals", 
            2, 
            row=1
        )

        self.create_card(
            frame, 
            "#5CB85C",
            "available.png", 
            str(stats["available"]), 
            "Available Devices",
            3, 
            row=1
        )

        self.create_card(
            frame, 
            "#888E93", 
            "nostock.png", 
            str(stats["total_devices"]), 
            "Out of Stock Devices", 
            1, 
            row=2
        )

        self.create_card(
            frame, 
            "#675DB7", 
            "device.png", 
            str(stats["total_devices"]), 
            "Total Devices", 
            2, 
            row=2
        )

        self.create_card(
            frame, 
            "#337AB7", 
            "customers.png", 
            str(stats["total_rentees"]), 
            "Total Rentees", 
            3, 
            row=2
        )

    def create_card(self, parent, color, icon_name, number, title, column, row=1, command=None):

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
        )
        card.grid(row=row, column=column, sticky="n", padx=23, pady=17)
        card.pack_propagate(False)

        def on_enter(e):
            card.config(highlightbackground="black", highlightthickness=3)
            card.grid(pady=5)
            if command: card.config(cursor="hand2")

        def on_leave(e):
            card.config(highlightbackground="#eef2f7")
            card.grid(pady=17)
            card.config(cursor="")

        def bind_all(widget):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            if command:
                widget.bind("<Button-1>", lambda e: command())
            for child in widget.winfo_children():
                bind_all(child)

        if command:
            card.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: command())
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e: command())

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

        bind_all(card)