import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
from db.add_rental_logic import getcreate_customer, create_rental, get_devices, get_customers
from db.validation import validate_input
import re


def select_customer(rental, name_entries, contact_entry, email_entry):
    selector = tk.Toplevel()
    selector.title("Select Customer")
    selector.grab_set()
    selector.configure(bg="#ffd735")

    customers = get_customers()

    search_frame = tk.Frame(selector, bg="#ffd735")
    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(search_frame, text="Search:", bg="#ffd735").pack(side="left", padx=(0, 5))
    search_entry = tk.Entry(search_frame, width=35)
    search_entry.pack(side="left")

    columns = ("id", "first", "middle", "last", "suffix", "contact", "email", "region", "city", "brgy", "postal", "street")
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    tree = ttk.Treeview(selector, columns=columns, show="headings")

    tree.column("id", width=40, anchor="center")
    tree.column("first", width=100)
    tree.column("middle", width=100)
    tree.column("last", width=100)
    tree.column("suffix", width=100)
    tree.column("contact", width=100)
    tree.column("email", width=100)
    
    for col in ("region", "city", "brgy", "postal", "street"):
        tree.column(col, width=0, stretch=False)

    for col in columns:
        tree.heading(col, text=col.capitalize())

    h_scroll = ttk.Scrollbar(selector, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scroll.set)
    
    tree.pack(fill="both", expand=True, padx=10, pady=5)
    h_scroll.pack(fill="x", padx=10, pady=(0, 10))

    for cust in customers:
        tree.insert("", "end", values=cust)

    def filter_tree(event=None):
        query = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        for cust in customers:
            if query in str(cust[1]).lower() or query in str(cust[3]).lower():
                tree.insert("", "end", values=cust)

    search_entry.bind("<KeyRelease>", filter_tree)

    def on_select(event):
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")
        (cust_id, first, middle, last, suffix, contact, email, region, city, brgy, postal, street) = values

        rental.entries["First Name"].delete(0, tk.END)
        rental.entries["First Name"].insert(0, first)
        rental.entries["Middle Name"].delete(0, tk.END)
        rental.entries["Middle Name"].insert(0, middle)
        rental.entries["Last Name"].delete(0, tk.END)
        rental.entries["Last Name"].insert(0, last)
        rental.entries["Suffix"].delete(0, tk.END)
        rental.entries["Suffix"].insert(0, suffix)
        
        rental.contact_entry.delete(0, tk.END)
        rental.contact_entry.insert(0, contact)
        rental.email_entry.delete(0, tk.END)
        rental.email_entry.insert(0, email)

        rental.region_cb.set(region)
        rental.city_cb.set(city)
        rental.brgy_cb.set(brgy)
        rental.postal_entry.delete(0, tk.END)
        rental.postal_entry.insert(0, postal)
        rental.street_entry.delete(0, tk.END)
        rental.street_entry.insert(0, street)

        selector.destroy()

    tree.bind("<Double-1>", on_select)

def add_rental_page(container_frame,rental, prefill_device=None, prefill_model=None):
        
        vcmd_num = (container_frame.register(lambda P: validate_input(P, "numbers", length=11)), '%P')
        vcmd_alpha = (container_frame.register(lambda P: validate_input(P, "alpha", length=20)), '%P')
        vcmd_suffix = (container_frame.register(lambda P: validate_input(P, "suffix", length=5)), '%P')
        vcmd_email = (container_frame.register(lambda P: validate_input(P, "email", length=50)), '%P')
        
        for widget in container_frame.winfo_children():
            widget.destroy()

        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)

        form_frame = tk.Frame(container_frame, bg="#f0f0f0")
        form_frame.pack(fill="both", expand=True)

        def save_rental():

            fn = rental.entries["First Name"].get()
            ln = rental.entries["Last Name"].get()
            contact = rental.contact_entry.get()
            email = rental.email_entry.get()
            
            if not (fn and ln and contact and email):
                messagebox.showwarning("Error", "Please fill in all required fields!")
                return

            if len(contact) < 11:
                messagebox.showerror("Error", "Contact number must be 11 digits.")
                return
            
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                messagebox.showerror("Error", "Please enter a valid email address.")
                return

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
                
                total_text = total_label_text.get().replace("Rental Total: ₱", "").replace(",", "")
                total_fee = float(total_text)

                create_rental(
                    customer_id,
                    rental.staff_id,
                    rental.device_map[selected_device]["id"],
                    rental.rental_calendar.get(),
                    rental.return_calendar.get(),
                    total_fee
                )

                messagebox.showinfo("Success", "Rental saved successfully!")

            except Exception as e:
                messagebox.showerror("Database Error", str(e))



        def cframe(parent, label_text, width, is_cb=False, is_date=False, helper=None):

            c = tk.Frame(parent, bg="#f0f0f0")
            c.pack(side="left", padx=(0, 15), pady=0, anchor="n")

            
            tk.Label(c, text=label_text, bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w")
            
            if is_cb:
                widget = ttk.Combobox(c, width=width)
            elif is_date:
                widget = DateEntry(c, width=width, date_pattern="mm-dd-yyyy")
            else:
                widget = tk.Entry(c, width=width)
                
            widget.pack(anchor="w", ipady=3)

            if helper:
                tk.Label(c, text=helper, bg="#f0f0f0", fg="#7F7F7F", font=("Arial", 8)).pack(anchor="w", pady=(2,0))


            return widget


        rentee_info_frame = tk.LabelFrame(
            form_frame, 
            text="RENTEE INFO", 
            font=("Arial", 20, "bold"), 
            padx=10,
            pady=2, 
            bg="#f0f0f0"
        )
        rentee_info_frame.pack(fill="x", padx=10, pady=5)


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

        rental.entries = {}
        
        rental.entries["First Name"] = cframe(row1, "First Name:", 20, helper="Ex: Juan")
        rental.entries["First Name"].config(validate="key", validatecommand=vcmd_alpha)

        rental.entries["Middle Name"] = cframe(row1, "Middle Name:", 20, helper="(Optional)")
        rental.entries["Middle Name"].config(validate="key", validatecommand=vcmd_alpha)

        rental.entries["Last Name"] = cframe(row1, "Last Name:", 20, helper = "Ex: Dela Cruz")
        rental.entries["Last Name"].config(validate="key", validatecommand=vcmd_alpha)

        rental.entries["Suffix"] = cframe(row1, "Suffix:", 8, helper="(Optional)")
        rental.entries["Suffix"].config(validate="key", validatecommand=vcmd_suffix)

        rental.entries["Birthday"] = cframe(row1, "Birthday:", 15, is_date=True)


        addr_frame = tk.Frame(rentee_info_frame, bg="#f0f0f0")
        addr_frame.pack(fill="x", pady=5)


        
        rental.region_cb = cframe(addr_frame, "Region:", 12, is_cb=True)
        rental.city_cb = cframe(addr_frame, "City:", 12, is_cb=True)
        rental.brgy_cb = cframe(addr_frame, "Brgy:", 12, is_cb=True)
        rental.postal_entry = cframe(addr_frame, "Postal:", 8, is_cb=False, helper="e.g. 1000")
        rental.street_entry = cframe(addr_frame, "Street/Bldg:", 30, is_cb=False, helper="Ex: 1234 Maple Street, Apt 5B")

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
            pady=2, 
            bg="#f0f0f0"
        )
        contact_frame.pack(fill="x", padx=10, pady=5)
        row_contact = tk.Frame(contact_frame, bg="#f0f0f0")
        row_contact.pack(fill="x")

        rental.contact_entry = cframe(row_contact, "Contact Number:", 30, helper="Ex: 09XX-XXX-YYYY")
        rental.contact_entry.config(validate="key", validatecommand=vcmd_num)

        rental.email_entry = cframe(row_contact, "Email Address:", 30, helper="Ex: example@gmail.com")
        rental.email_entry.config(validate="key", validatecommand=vcmd_email)


        device_frame = tk.LabelFrame(
            form_frame, 
            text="DEVICE RENTAL", 
            font=("Arial", 20, "bold"), 
            padx=10, 
            pady=5, 
            bg="#f0f0f0"
        )
        device_frame.pack(fill="x", padx=10, pady=5)
        
        row_dev = tk.Frame(device_frame, bg="#f0f0f0")
        row_dev.pack(fill="x")
        
        rental.device_combobox = cframe(row_dev, "Device to Rent:", 30, is_cb=True)

        devices = get_devices()

        rental.device_map = {}

        for device_id, model, price in devices:
            rental.device_map[model] = {"id": device_id, "price": price}

        rental.device_combobox["values"] = list(
            rental.device_map.keys()
        )

        if prefill_model:
            if prefill_model in rental.device_map:
                rental.device_combobox.set(prefill_model)



        d1 = tk.Frame(row_dev, bg="#f0f0f0")
        d1.pack(side="left", padx=10)

        tk.Label(
            d1, 
            text="Rental Date:",
            font=("Arial", 10), 
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.rental_calendar = DateEntry(d1, width=15, date_pattern="mm-dd-yyyy")
        rental.rental_calendar.pack(anchor="w", ipady=3)

        d2 = tk.Frame(row_dev, bg="#f0f0f0")
        d2.pack(side="left", padx=10)
        
        tk.Label(
            d2, 
            text="Return By:", 
            font=("Arial", 10), 
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.return_calendar = DateEntry(d2, width=15, date_pattern="mm-dd-yyyy")
        rental.return_calendar.pack(anchor="w", ipady=3)



        #bottom
        bottom_bar = tk.Frame(form_frame, padx=10, pady=20, bg="#eef2f7")
        bottom_bar.pack(fill="x", side="bottom")

        total_label_text = tk.StringVar(value="Rental Total: ₱0.00")
        total_label = tk.Label(
            bottom_bar, 
            textvariable=total_label_text, 
            font=("Arial", 20, "bold"), 
            bg="#eef2f7"
        )
        total_label.pack(side="left")


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

        def update_total(*args):
            try:
                selected_model = rental.device_combobox.get()
                if not selected_model or selected_model not in rental.device_map:
                    total_label_text.set("Rental Total: ₱0.00")
                    return
                
                price = rental.device_map[selected_model]["price"]
                
                start_date = rental.rental_calendar.get_date()
                end_date = rental.return_calendar.get_date()

                delta = (end_date - start_date).days
                days = max(1, delta)
                
                total = days * price
                total_label_text.set(f"Rental Total: ₱{total:,.2f}")
            except:
                total_label_text.set("Rental Total: ₱0.00")

        rental.device_combobox.bind("<<ComboboxSelected>>", update_total)
        rental.rental_calendar.bind("<<DateEntrySelected>>", update_total)
        rental.return_calendar.bind("<<DateEntrySelected>>", update_total)