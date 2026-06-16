import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
from db.add_rental_logic import getcreate_customer, create_rental, get_devices, get_customers


def select_customer(rental, name_entries, contact_entry, email_entry):
    selector = tk.Toplevel()
    selector.title("Select Customer")
    selector.geometry("500x300")
    selector.grab_set()

    customers = get_customers()

    search_frame = tk.Frame(selector)
    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 5))

    search_entry = tk.Entry(search_frame, width=35)
    search_entry.pack(side="left")

    def filter_tree(event=None):
        query = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        for cust in customers:
            if query in cust[1].lower() or query in cust[2].lower():
                tree.insert("", "end", values=cust)

    search_entry.bind("<KeyRelease>", filter_tree)

    columns = ("id", "first", "middle", "last", "suffix", "contact", "email")
    tree = ttk.Treeview(selector, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("contact", text="Contact")
    tree.heading("email", text="Email")

    tree.column("id", width=50, anchor="center") 
    tree.heading("first", text="First Name")
    tree.heading("middle", text="Middle Name")
    tree.heading("last", text="Last Name")
    tree.heading("suffix", text="Suffix")
    tree.heading("contact", text="Contact")
    tree.heading("email", text="Email")
    tree.pack(fill="both", expand=True, padx=10, pady=5)

    def on_select(event):
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")

        customer_id, first, middle, last, suffix, contact, email = values

        name_entries["First Name"].delete(0, tk.END)
        name_entries["First Name"].insert(0, first)

        name_entries["Middle Name"].delete(0, tk.END)
        name_entries["Middle Name"].insert(0, middle)

        name_entries["Last Name"].delete(0, tk.END)
        name_entries["Last Name"].insert(0, last)

        name_entries["Suffix"].delete(0, tk.END)
        name_entries["Suffix"].insert(0, suffix)

        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, contact)

        email_entry.delete(0, tk.END)
        email_entry.insert(0, email)

        selector.destroy()

    tree.bind("<Double-1>", on_select)

def add_rental_page(container_frame,rental):
        for widget in container_frame.winfo_children():
            widget.destroy()

        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)

        form_frame = tk.Frame(container_frame, bg="#f0f0f0")
        form_frame.pack(fill="both", expand=True)

        def save_rental():

            try:
                customer_id = getcreate_customer(
                    rental.entries["First Name"].get(),
                    rental.entries["Middle Name"].get(),
                    rental.entries["Last Name"].get(),
                    rental.entries["Suffix"].get(),
                    rental.entries["Birthday"].get(),
                    rental.contact_entry.get(),
                    rental.email_entry.get(),
                    rental.region_cb.get(),
                    rental.city_cb.get(),
                    rental.brgy_cb.get(),
                    rental.postal_entry.get(),
                    rental.street_entry.get()
                )
                

                selected_device = rental.device_combobox.get()

                if selected_device not in rental.device_map:
                    raise Exception("Please select a valid device")

                create_rental(
                    customer_id,
                    rental.staff_id,
                    rental.device_map[selected_device],

                    rental.rental_calendar.get(),
                    rental.return_calendar.get(),
                )

                messagebox.showinfo("Success", "Rental saved successfully!")

            except Exception as e:
                messagebox.showerror("Database Error", str(e))



        def cframe(parent, label_text, width, is_cb=False):
            f = tk.Frame(parent, bg="#f0f0f0")
            f.pack(side="left", padx=(0, 10), pady=0)
            tk.Label(f, text=label_text, bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w")
            
            if is_cb:
                widget = ttk.Combobox(f, width=width)
            else:
                widget = tk.Entry(f, width=width)
                
            widget.pack(anchor="w", ipady=3)
            return widget


        rentee_info_frame = tk.LabelFrame(
            form_frame, 
            text="RENTEE INFO", 
            font=("Arial", 20, "bold"), 
            padx=10,
            pady=10, 
            bg="#f0f0f0"
        )
        rentee_info_frame.pack(fill="x", padx=10, pady=10)


        row1 = tk.Frame(rentee_info_frame, bg="#f0f0f0")
        row1.pack(fill="x", pady=(0,5))

        select_btn = tk.Button(
            row1, 
            text="Select Customer", 
            bg="#ffd735", 
            font=("Arial", 10, "bold"),
            command=lambda: select_customer(rental, rental.entries, rental.contact_entry, rental.email_entry)
        )
        select_btn.pack(side="right", padx=10, ipady=3) 
        rental.add_hover(select_btn, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")

        rental.entries = {
            "First Name": cframe(row1, "First Name:", 20),
            "Middle Name": cframe(row1, "Middle Name:", 20),
            "Last Name": cframe(row1, "Last Name:", 20),
            "Suffix": cframe(row1, "Suffix:", 5),
        }
        bday_f = tk.Frame(row1, bg="#f0f0f0")
        bday_f.pack(side="left")

        tk.Label(
            bday_f, 
            text="Birthday:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(anchor="w")

        rental.entries["Birthday"] = DateEntry(bday_f, width=15, date_pattern="mm-dd-yyyy")
        rental.entries["Birthday"].pack(anchor="w", ipady=3)


        addr_frame = tk.Frame(rentee_info_frame, bg="#f0f0f0")
        addr_frame.pack(fill="x", pady=5)


        
        rental.region_cb = cframe(addr_frame, "Region:", 12, is_cb=True)
        rental.city_cb = cframe(addr_frame, "City:", 12, is_cb=True)
        rental.brgy_cb = cframe(addr_frame, "Brgy:", 12, is_cb=True)
        rental.postal_entry = cframe(addr_frame, "Postal:", 8, is_cb=False)
        rental.street_entry = cframe(addr_frame, "Street/Bldg:", 30, is_cb=False)

        #dummy values lng muna
        rental.region_cb["values"] = [
            "NCR"
        ]

        rental.city_cb["values"] = [
            "Quezon City"
        ]

        rental.brgy_cb["values"] = [
            "Brgy. 123"
        ]

        contact_frame = tk.LabelFrame(
            form_frame, 
            text="CONTACT INFO", 
            font=("Arial", 20, "bold"), 
            padx=10, 
            pady=10, 
            bg="#f0f0f0"
        )
        contact_frame.pack(fill="x", padx=10, pady=10)
        row_contact = tk.Frame(contact_frame, bg="#f0f0f0")
        row_contact.pack(fill="x")

        rental.contact_entry = cframe(row_contact, "Contact Number:", 30)
        rental.email_entry = cframe(row_contact, "Email Address:", 30)


        device_frame = tk.LabelFrame(
            form_frame, 
            text="DEVICE RENTAL", 
            font=("Arial", 20, "bold"), 
            padx=10, 
            pady=10, 
            bg="#f0f0f0"
        )
        device_frame.pack(fill="x", padx=10, pady=10)
        
        row_dev = tk.Frame(device_frame, bg="#f0f0f0")
        row_dev.pack(fill="x")
        
        rental.device_combobox = cframe(row_dev, "Device to Rent:", 30, is_cb=True)

        devices = get_devices()

        rental.device_map = {}

        for device_id, model in devices:
            rental.device_map[model] = device_id

        rental.device_combobox["values"] = list(
            rental.device_map.keys()
        )

        if devices:
            rental.device_combobox.current(0)



        d1 = tk.Frame(row_dev, bg="#f0f0f0")
        d1.pack(side="left", padx=10)

        tk.Label(
            d1, 
            text="Rental Date:",
            font=("Arial", 10, "bold"), 
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.rental_calendar = DateEntry(d1, width=15, date_pattern="mm-dd-yyyy")
        rental.rental_calendar.pack(anchor="w", ipady=3)

        d2 = tk.Frame(row_dev, bg="#f0f0f0")
        d2.pack(side="left", padx=10)
        
        tk.Label(
            d2, 
            text="Return By:", 
            font=("Arial", 10, "bold"), 
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.return_calendar = DateEntry(d2, width=15, date_pattern="mm-dd-yyyy")
        rental.return_calendar.pack(anchor="w", ipady=3)



        #bottom
        bottom_bar = tk.Frame(form_frame, padx=10, pady=20, bg="#eef2f7")
        bottom_bar.pack(fill="x", side="bottom")

        tk.Label(
            bottom_bar,
            text="Rental Total: ₱0.00",
            font=("Arial", 20, "bold")
        ).pack(side="left")


        back_btn = tk.Button(
            bottom_bar,
            text="Back",
            font=("Arial", 17, "bold"),
            bg="gray",
            cursor="hand2",
            command=lambda: rental.pages["rentals"].tkraise()
        )
        back_btn.pack(side="right", padx=5)

        create_btn = tk.Button(
            bottom_bar,
            text="Create Rental",
            font=("Arial", 17, "bold"),
            bg="#ffd735",
            cursor="hand2",
            command=save_rental
        )
        create_btn.pack(side="right", padx=5)

        reset_btn = tk.Button(
        bottom_bar,
        text="Reset",
        font=("Arial", 17, "bold"),
        bg="#eef2f7",
        fg="#ffd735",
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
        )
        reset_btn.pack(side="right", padx=5)

        rental.add_hover(create_btn, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")
        rental.add_hover(back_btn, "#232624", "gray", "white", "black")
        rental.add_hover(reset_btn, "#232624", "#eef2f7", "white", "black")