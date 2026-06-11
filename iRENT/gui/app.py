import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os

from gui.orders import create_orders
from gui.overdue import create_overdue


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iRENT")
        self.root.state("zoomed")

        self.create_layout()
        self.create_pages()
        self.create_sidebar()
        self.create_dataentry()
        self.create_orders_page()
        self.create_overdue_page()

        self.pages["dataentry"].tkraise()



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


    #pages
    def create_pages(self):
        self.pages = {}

        for name in ["dataentry", "orders", "order_details", "history", "devices", "overdue"]:
            frame = tk.Frame(self.right)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[name] = frame

            frame.grid_rowconfigure(0,weight=1)
            frame.grid_columnconfigure(0, weight=1)



    #sidebar
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
        ).pack( padx=10,fill="x")

        tk.Entry(
            search_box,
            font=("Arial", 12),
            width=28
        ).pack(pady=(5,40), padx=10,ipady=6, anchor="w")

        buttons = [
            ("View Rental Orders", "orders"),
            ("View Overdue Rental", "overdue"),
            ("View Rental History", "history"),
            ("View List of Devices", "devices")
        ]

        for text,page in buttons:
            tk.Button(
                search_box,
                text=text,
                bg="#ffd735",
                fg="black",
                width=25,
                font=("Arial", 12, "bold"),
                command=lambda p=page: self.pages[p].tkraise()
            ).pack(pady=15, padx=10, ipady=6, anchor="w")


    #view rental orders
    def create_orders_page(self):
        create_orders(self.pages["orders"], self)

    #view overdue rentals
    def create_overdue_page(self):
        create_overdue(self.pages["overdue"], self)



    #data entry
    def create_dataentry(self):
        form_frame = tk.LabelFrame(
            self.pages["dataentry"],
            relief="flat",    
            labelanchor="n",
            bd=0
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_rowconfigure(3, weight=1)


        rentee_info_frame = tk.LabelFrame(
            form_frame,
            bd=0,
            relief="flat"
        )
        rentee_info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))
        for col in range(4):
            rentee_info_frame.grid_columnconfigure(col, weight=1, uniform="cols")
        
        rentee_title = tk.Label(
            rentee_info_frame,
            text="RENTEE INFO",
            font=("Arial", 20, "bold")
        )
        rentee_title.grid(row=0,column=0,sticky="w", padx=5, pady=5, columnspan=4)

        fields = ["First Name", "Middle Name", "Last Name", "Suffix"]

        self.entries = {}

        for index, field_name in enumerate(fields):
            label = tk.Label(
                rentee_info_frame,
                text=field_name,
                fg="black",
                font=("Arial", 12)
            )
            label.grid(row=1, column=index, padx=5, pady=(5,0))

            entry = tk.Entry(rentee_info_frame, width=20)
            entry.grid(row=2, column=index, padx=10, pady=(10,20), ipady=6, sticky="ew")

            self.entries[field_name] = entry


        #contact frame
        contact_frame = tk.LabelFrame(
            form_frame,
            text="CONTACT INFO",
            font=("Arial", 20, "bold"),
            bd=0
        )
        contact_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(10,20))

        
        tk.Label(
            contact_frame, 
            text="Contact Number:"
        ).grid(row=1, column=0, sticky="w", padx=5)

        self.contact_entry = tk.Entry(contact_frame)
        self.contact_entry.grid(row=1, column=1, padx=5, ipady=6)


        tk.Label(
            contact_frame, 
            text="Email Address:"
        ).grid(row=1, column=2, sticky="w", padx=5)

        self.email_entry = tk.Entry(contact_frame)
        self.email_entry.grid(row=1, column=3, padx=5, ipady=6)



        #device rental
        device_frame = tk.Frame(form_frame)
        device_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(10,20))
        
        tk.Label(
            device_frame, 
            text="DEVICE RENTAL", 
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, sticky="w", columnspan=4)
        
        # row 1 device to rent
        tk.Label(
            device_frame, 
            text="Device to Rent:", 
            font=("Arial", 12, "bold")
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.device_combobox = ttk.Combobox(device_frame, values=["Device 1", "Device 2"])
        self.device_combobox.grid(row=1, column=1, sticky="w", padx=5, pady=5, ipady=6)
        

        # row 2 rental date and return date
        tk.Label(
            device_frame, 
            text="Rental Date:", 
            font=("Arial", 12, "bold")
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.rental_calendar = DateEntry(device_frame, width=12, date_pattern="mm-dd-yyyy")
        self.rental_calendar.grid(row=2, column=1, sticky="w", padx=5, pady=5, ipady=6)
        
        tk.Label(
            device_frame, 
            text="Must Return By:", 
            font=("Arial", 12, "bold")
        ).grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.return_by = ttk.Combobox(device_frame, values=["1 day", "3 days"])
        self.return_by.grid(row=2, column=3, sticky="w", padx=5, pady=5, ipady=6)


        #bottom
        tk.Label(
            form_frame, 
            text="Rental Total: ₱0.00",
            font=("Arial", 20, "bold")
        ).grid(row=3, column=0, sticky="sw", padx=10, pady=10)

        tk.Button(
            form_frame,
            text="Create Rental",
            font=("Arial", 17, "bold"),
            bg="#ffd735"
        ).grid(row=3, column=2, sticky="se", padx=10, pady=10)

        tk.Button(
            form_frame,
            text="Reset",
            font=("Arial", 17, "bold"),
            bg="gray"
        ).grid(row=3, column=3, sticky="se", padx=10, pady=10)

        