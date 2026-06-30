import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import messagebox
from db.add_rental_logic import getcreate_customer, create_rental, get_devices, get_customers, load_devices, all_avail_dev
from db.address_service import regionsdb, provincesdb, citiesdb, brgysdb
from db.validation import validate_input
import re

def select_customer(rental, name_entries, contact_entry, email_entry):
    selector = tk.Toplevel()
    selector.title("Select Customer")
    selector.grab_set()
    selector.configure(bg="#ffd735")
    selector.geometry("900x500")

    customers = get_customers()

    frame = tk.Frame(selector,bg="#ffd735", padx=5, pady=5)
    frame.pack(fill="x", padx=10, pady=5)

    search_con = tk.Frame(frame , bg="#ffd735")
    search_con.pack(side="left", padx=5, anchor="s")

    tk.Label(
        search_con,
        text="Search:",
        bg="#ffd735",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    search_entry = tk.Entry(search_con, width=30)
    search_entry.pack(ipady=3)

    columns = ("id", "first", "middle", "last", "suffix", "birthday", "contact", "email", "region", "province", "city", "brgy", "postal", "street")

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

    for col in ("birthday", "region", "province", "city", "brgy", "postal", "street"):
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
        (cust_id, first, middle, last, suffix, birthday, contact, email, region, province, city, brgy, postal, street) = values

        rental.entries["First Name"].delete(0, tk.END)
        rental.entries["First Name"].insert(0, first)

        rental.entries["Middle Name"].delete(0, tk.END)
        if middle and middle != 'None':
            rental.entries["Middle Name"].insert(0, middle)

        rental.entries["Last Name"].delete(0, tk.END)
        rental.entries["Last Name"].insert(0, last)

        rental.entries["Suffix"].delete(0, tk.END)
        if suffix and suffix != 'None':
            rental.entries["Suffix"].insert(0, suffix)

        # FIXED: Extract birthday and safely set it into the DateEntry widget
        if birthday and birthday != 'None':
            try:
                b_date = datetime.strptime(str(birthday), "%m-%d-%Y").date()
                rental.entries["Birthday"].set_date(b_date)
            except ValueError:
                pass # Defaults if the database holds invalid data

        rental.contact_entry.delete(0, tk.END)
        rental.contact_entry.insert(0, contact)

        rental.email_entry.delete(0, tk.END)
        rental.email_entry.insert(0, email)

        rental.region_cb.set(region)
        rental.province_cb.set(province)
        rental.city_cb.set(city)
        rental.brgy_cb.set(brgy)

        rental.postal_entry.delete(0, tk.END)
        rental.postal_entry.insert(0, postal)

        rental.street_entry.delete(0, tk.END)
        rental.street_entry.insert(0, street)

        selector.destroy()

    tree.bind("<Double-1>", on_select)


def update_total(event=None,rental=None, rental_total=None):
        try:
            if not hasattr(rental, 'selected_device_data'):
                rental_total.set("Rental Total: ₱ 0.00")
                return

            price = rental.selected_device_data["price"]

            start_date = rental.rental_calendar.get_date()
            end_date = rental.return_calendar.get_date()
            delta = (end_date - start_date).days
            days = max(1, delta)

            total = days * price
            rental_total.set(f"Rental Total: ₱ {total:,.2f}")
        except:
            rental_total.set("Rental Total: ₱ 0.00")

def dev_win(rental, rental_total):
    selector = tk.Toplevel()
    selector.title("Select Device")
    selector.grab_set()
    selector.configure(bg="#ffd735")
    selector.geometry("900x500")

    filter_frame = tk.Frame(selector,bg="#ffd735", padx=5, pady=5)
    filter_frame.pack(fill="x", padx=10, pady=5)

    search_con = tk.Frame(filter_frame , bg="#ffd735")
    search_con.pack(side="left", padx=5, anchor="s")

    tk.Label(
        search_con,
        text="Search:",
        bg="#ffd735",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    search_entry = tk.Entry(search_con, width=30)
    search_entry.pack(ipady=3)

    def view_all():
        type_cb.set('')
        brand_cb.set('')
        search_entry.delete(0, tk.END)
        brand_cb['values'] = sorted(list(set(d['brand'] for d in devices)))
        apply_filters()

    view_con = tk.Frame(filter_frame, bg="#ffd735")
    view_con.pack(side="right", padx=5, anchor="s")
    view_btn = tk.Button(
        view_con,
        text="View All",
        command=view_all,
        font=("Arial", 10, "bold"),
        fg = "#ffd735",
        bg= "#232624"
    )
    view_btn.pack (side="left", padx=5)
    rental.add_hover(view_btn,"#ffd735", "#232624", enter_fg="black", leave_fg="#ffd735")

    brand_con = tk.Frame(filter_frame, bg="#ffd735")
    brand_con.pack(side="right", padx=5)
    tk.Label(
        brand_con,
        text="Brand:",
        bg="#ffd735",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    brand_cb = ttk.Combobox(brand_con, state="readonly", width=23)
    brand_cb.pack(ipady=3)

    type_con = tk.Frame(filter_frame, bg="#ffd735")
    type_con.pack(side="right", padx=5)
    tk.Label(
        type_con,
        text="Device Type:",
        bg="#ffd735",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    type_cb = ttk.Combobox(type_con, state="readonly", width=23)
    type_cb.pack(ipady=3)

    devices = all_avail_dev()
    types = sorted(list(set(d['type'] for d in devices)))
    type_cb['values'] = types

    tree_frame = tk.Frame(selector, bg="#ffd735")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("id", "type", "brand", "model", "price")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=v_scroll.set)

    v_scroll.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        if col == "id": tree.column(col, width=0, stretch=False)

    def apply_filters(*args):
        selected_type = type_cb.get()
        selected_brand = brand_cb.get()
        query = search_entry.get().lower()

        if selected_type:
            brand_cb['values'] = sorted(list(set(d['brand'] for d in devices if d['type'] == selected_type)))

        for item in tree.get_children(): tree.delete(item)

        for d in devices:
            if (not selected_type or d['type'] == selected_type) and \
               (not selected_brand or d['brand'] == selected_brand) and \
               (query in d['model'].lower() or
                query in d['brand'].lower() or
                query in d['type'].lower()):
                tree.insert("", "end", values=(d['id'], d['type'], d['brand'], d['model'], d['price']))

    type_cb.bind("<<ComboboxSelected>>", lambda e: apply_filters())
    brand_cb.bind("<<ComboboxSelected>>", lambda e: apply_filters())
    search_entry.bind("<KeyRelease>", apply_filters)

    def click_dev(event=None):
        selected = tree.focus()
        if not selected:
            return
        vals = tree.item(selected, "values")
        rental.selected_device_data = {"id": vals[0], "model": vals[3], "price": float(vals[4])}

        rental.model_display.config(state="normal")
        rental.model_display.delete(0, tk.END)
        rental.model_display.insert(0, vals[3])
        rental.model_display.config(state="readonly")

        update_total(None,rental, rental_total)
        selector.destroy()

    tree.bind("<Double-1>", click_dev)
    apply_filters()


def add_rental_page(container_frame,rental, prefill_device=None):

        vcmd_num = (container_frame.register(lambda P: validate_input(P, "numbers", length=11)), '%P')
        vcmd_alpha = (container_frame.register(lambda P: validate_input(P, "alpha", length=20)), '%P')
        vcmd_suffix = (container_frame.register(lambda P: validate_input(P, "suffix", length=5)), '%P')
        vcmd_email = (container_frame.register(lambda P: validate_input(P, "email", length=50)), '%P')
        vcmd_postal = (container_frame.register(lambda P: validate_input(P, "numbers", length=4)), '%P')

        default_year = datetime.now().year - 21
        default_bday = date(default_year, 1, 1)

        def on_region_select(event):
            selected_name = rental.region_cb.get()
            r_code = rental.region_map[selected_name]
            provinces = provincesdb(r_code)
            rental.province_cb["values"] = [p[1] for p in provinces]
            rental.province_map = {p[1]: p[0] for p in provinces}
            rental.city_cb.set('')
            rental.brgy_cb.set('')

        def on_province_select(event):
            p_code = rental.province_map[rental.province_cb.get()]
            cities = citiesdb(p_code)
            rental.city_cb["values"] = [c[1] for c in cities]
            rental.city_map = {c[1]: c[0] for c in cities}
            rental.brgy_cb.set('')

        def on_city_select(event):
            c_code = rental.city_map[rental.city_cb.get()]
            brgys = brgysdb(c_code)
            rental.brgy_cb["values"] = [b[1] for b in brgys]

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

            # --- NEW DATE VALIDATION ---
            start_date = rental.rental_calendar.get_date()
            end_date = rental.return_calendar.get_date()

            if end_date < start_date:
                messagebox.showerror("Invalid Date!", "The return date cannot be earlier than the rental date.")
                return
            # ---------------------------

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
                    rental.province_cb.get(),
                    rental.city_cb.get(),
                    rental.brgy_cb.get(),
                    rental.postal_entry.get(),
                    rental.street_entry.get()
                )

                # --- FIXED: USE EXPLICIT DEVICE ID ---
                if not hasattr(rental, 'selected_device_data'):
                    raise Exception("Please select a specific device from the list.")
                exact_device_id = rental.selected_device_data["id"]

                # --- FIXED: ROBUST FLOAT CONVERSION ---
                # Strips out all letters, currency symbols, spaces, and commas
                raw_total = rental_total.get()
                clean_total = re.sub(r'[^\d.]', '', raw_total)
                total_fee = float(clean_total) if clean_total else 0.00
                # --------------------------------------

                create_rental(
                    customer_id,
                    rental.staff_id,
                    exact_device_id,
                    rental.rental_calendar.get(),
                    rental.return_calendar.get(),
                    total_fee,
                    "",
                    0.0,
                    total_fee
                )

                if hasattr(rental, 'refresh_rentals'):
                    rental.refresh_rentals()

                messagebox.showinfo("Success", "Rental saved successfully!")
                rental.pages["rentals"].tkraise()
                reset_form()

            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        def reset_form():
            for entry in rental.entries.values():
                entry.delete(0, tk.END)

            rental.contact_entry.delete(0, tk.END)
            rental.email_entry.delete(0, tk.END)
            rental.postal_entry.delete(0, tk.END)
            rental.street_entry.delete(0, tk.END)

            rental.region_cb.set('')
            rental.province_cb.set('')
            rental.city_cb.set('')
            rental.brgy_cb.set('')

            rental.model_display.config(state="normal")
            rental.model_display.delete(0, tk.END)
            rental.model_display.config(state="readonly")

            rental_total.set("Rental Total: ₱ 0.00")
            if hasattr(rental, 'selected_device_data'):
                delattr(rental, 'selected_device_data')

        def cframe(parent, label_text, width, is_cb=False, is_date=False, helper=None, default_date=None):
            c = tk.Frame(parent, bg="#f0f0f0")
            c.pack(side="left", padx=(0, 15), pady=0, anchor="n")

            tk.Label(c, text=label_text, bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w")

            if is_cb:
                widget = ttk.Combobox(c, width=width)
            elif is_date:
                widget = DateEntry(c, width=width, date_pattern="mm-dd-yyyy", date=default_date)
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
        rental.entries["Birthday"].set_date(default_bday)

        addr_frame = tk.Frame(rentee_info_frame, bg="#f0f0f0")
        addr_frame.pack(fill="x", pady=5)

        rental.region_cb = cframe(addr_frame, "Region:", 30, is_cb=True)
        rental.province_cb = cframe(addr_frame, "Province:", 30, is_cb=True)
        rental.city_cb = cframe(addr_frame, "City:", 15, is_cb=True)
        rental.brgy_cb = cframe(addr_frame, "Brgy:", 15, is_cb=True)
        rental.postal_entry = cframe(addr_frame, "Postal:", 8, is_cb=False, helper="e.g. 1000")
        rental.postal_entry.config(validate="key", validatecommand=vcmd_postal)
        rental.street_entry = cframe(addr_frame, "Street/Bldg:", 30, is_cb=False, helper="Ex: 1234 Maple Street, Apt 5B")

        regions_data = regionsdb()
        rental.region_cb["values"] = [r[1] for r in regions_data]
        rental.region_map = {r[1]: r[0] for r in regions_data}

        rental.region_cb.bind("<<ComboboxSelected>>", on_region_select)
        rental.province_cb.bind("<<ComboboxSelected>>", on_province_select)
        rental.city_cb.bind("<<ComboboxSelected>>", on_city_select)

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

        seldev_con = tk.Frame(row_dev, bg="#f0f0f0")
        seldev_con.pack(side="left", anchor="n")

        tk.Label(
            seldev_con,
            text="Device to Rent:",
            bg="#f0f0f0",
            font=("Arial", 10),
        ).pack(anchor="w", padx=3)

        rental.model_display = tk.Entry(seldev_con, width=25, font=("Arial", 10, "bold", "italic"))
        rental.model_display.pack(side="left", padx=5, ipady=3)
        rental.model_display.config(state="readonly")

        select_dev = tk.Button(
            row_dev,
            text="Select Device",
            bg="#ffd735",
            font=("Arial", 10, "bold"),
            command= lambda: dev_win(rental, rental_total)
        )
        select_dev.pack(side="left", padx=(0,10), pady=(15,0))
        rental.add_hover(select_dev, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")

        devices = get_devices()
        rental.device_map = {}
        for device_id, model, price in devices:
            rental.device_map[model] = {"id": device_id, "price": price}


        d1 = tk.Frame(row_dev, bg="#f0f0f0")
        d1.pack(side="left", padx=10)
        tk.Label(
            d1,
            text="Rental Date:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.rental_calendar = DateEntry(d1, width=15, date_pattern="mm-dd-yyyy")
        rental.rental_calendar.pack(anchor="w", ipady=3, pady=(0,5))

        d2 = tk.Frame(row_dev, bg="#f0f0f0")
        d2.pack(side="left", padx=10)

        tk.Label(
            d2,
            text="Return By:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(anchor="w")
        rental.return_calendar = DateEntry(d2, width=15, date_pattern="mm-dd-yyyy")
        rental.return_calendar.pack(anchor="w", ipady=3, pady=(0,5))

        #bottom
        bottom_bar = tk.Frame(form_frame, padx=10, pady=20, bg="#eef2f7")
        bottom_bar.pack(fill="x", side="bottom")

        rental_total = tk.StringVar(value="Rental Total: ₱ 0.00")
        total_label = tk.Label(
            bottom_bar,
            textvariable=rental_total,
            font=("Arial", 20, "bold"),
            bg="#eef2f7"
        )
        total_label.pack(side="left")

        if prefill_device:
            model_name = prefill_device.get("model_name", prefill_device.get("model"))
            rental.model_display.config(state="normal")
            rental.model_display.delete(0, tk.END)
            rental.model_display.insert(0, model_name)
            rental.model_display.config(state="readonly")

            # --- FIXED ID ASSIGNMENT ---
            rental.selected_device_data = {
                "id": prefill_device.get("id", prefill_device.get("product_id", "")),
                "model": model_name,
                "price": prefill_device.get("price", 0)
            }
            update_total(None, rental, rental_total)

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
        relief="flat",
        command=reset_form
        )
        reset_btn.pack(side="right", padx=5)

        rental.add_hover(create_btn, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")
        rental.add_hover(back_btn, "#232624", "gray", "white", "black")
        rental.add_hover(reset_btn, "#232624", "#eef2f7", "white", "black")

        rental.rental_calendar.bind("<<DateEntrySelected>>", lambda e: update_total(e, rental, rental_total))
        rental.return_calendar.bind("<<DateEntrySelected>>", lambda e: update_total(e, rental, rental_total)) # test push