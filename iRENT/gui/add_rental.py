import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
import datetime

# DB imports: try package import first, fallback to module import when running from db folder
try:
    from db.sqlite_crudop import (
        make_database, get_connection, add_customer, create_rental_transaction,
        get_all_available_devices, update_device_availability
    )

except Exception:
    from db.sqlite_crudop import (
        make_database, get_connection, add_customer, create_rental_transaction,
        get_all_available_devices, update_device_availability
    )

def select_customer(rental, name_entries, contact_entry, email_entry):
    selector = tk.Toplevel()
    selector.title("Select Customer")
    selector.geometry("500x300")
    selector.grab_set()

    #hardcoded examples palang to
    customers = [
        (101, "FirstName LastName", "12312312312", "example@gmail.com"),
        (102, "Jose Manalo", "12123123123", "hello@gmail.com"),
        (103, "Skusta Clee", "123123123", "12312312@gmail.com")
    ]

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

    columns = ("id", "name", "contact", "email")
    tree = ttk.Treeview(selector, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("contact", text="Contact")
    tree.heading("email", text="Email")

    tree.column("id", width=50, anchor="center")
    tree.column("name", width=150)
    tree.column("contact", width=100)
    tree.column("email", width=150)
    tree.pack(fill="both", expand=True, padx=10, pady=5)

    for cust in customers:
        tree.insert("", "end", values=cust)


def add_rental_page(container_frame,rental):
        for widget in container_frame.winfo_children():
            widget.destroy()

        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)

        form_frame = tk.LabelFrame(
            container_frame,
            relief="flat",
            labelanchor="n",
            bd=0
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,0))
        form_frame.grid_rowconfigure(0, weight=0) #rentee info
        form_frame.grid_rowconfigure(1, weight=0) #contact infp
        form_frame.grid_rowconfigure(2, weight=0) #device rental
        form_frame.grid_rowconfigure(3, weight=1)
        form_frame.grid_rowconfigure(4, weight=0) #buttons/bottom bar
        form_frame.grid_columnconfigure(0, weight=1) #stretch horizontally

        rentee_info_frame = tk.LabelFrame(
            form_frame,
            bd=0,
            relief="flat"
        )
        rentee_info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(25, 25))
        for col in range(4):
            rentee_info_frame.grid_columnconfigure(col, weight=0)

        rentee_title = tk.Label(
            rentee_info_frame,
            text="RENTEE INFO",
            font=("Arial", 20, "bold")
        )
        rentee_title.grid(row=0, column=0, sticky="w", padx=(5,10), pady=5, columnspan=3)

        select_btn = tk.Button(
            rentee_info_frame,
            text="Select Customer",
            bg="#ffd735",
            font=("Arial", 10, "bold"),
            command=lambda: select_customer(rental, rental.entries, rental.contact_entry, rental.email_entry)
        )
        select_btn.grid(row=0, column=2, sticky="w", padx=0, pady=5)
        rental.add_hover(select_btn, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")

        fields = ["First Name", "Middle Name", "Last Name", "Suffix"]

        field_configs = [
            ("First Name", 20),
            ("Middle Name", 20),
            ("Last Name", 20),
            ("Suffix", 5),
        ]

        rental.entries = {}

        for index, (field_name, width) in enumerate(field_configs):
            label = tk.Label(rentee_info_frame, text=field_name + ":", font=("Arial", 12))
            label.grid(row=1, column=index * 2, padx=(10, 2), pady=5, sticky="w")

            entry = tk.Entry(rentee_info_frame, width=width)
            entry.grid(row=1, column=index * 2 + 1, padx=(0, 5), pady=5, ipady=4, sticky="ew")

            rental.entries[field_name] = entry

        contact_frame = tk.LabelFrame(
            form_frame,
            text="CONTACT INFO",
            font=("Arial", 20, "bold"),
            bd=0
        )
        contact_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(25, 25))

        tk.Label(
            contact_frame,
            text="Contact Number:",
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="w", padx=5)

        rental.contact_entry = tk.Entry(contact_frame)
        rental.contact_entry.grid(row=1, column=1, padx=5, ipady=6)

        tk.Label(
            contact_frame,
            text="Email Address:",
            font=("Arial", 12)
        ).grid(row=1, column=2, sticky="w", padx=5)

        rental.email_entry = tk.Entry(contact_frame)
        rental.email_entry.grid(row=1, column=3, padx=5, ipady=6)


        device_frame = tk.Frame(form_frame)
        device_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(25, 25))

        tk.Label(
            device_frame,
            text="DEVICE RENTAL",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, sticky="w", columnspan=4)

        tk.Label(
            device_frame,
            text="Device to Rent:",
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        rental.device_combobox = ttk.Combobox(device_frame, values=["Device 1", "Device 2"])
        rental.device_combobox.grid(row=1, column=1, sticky="w", padx=5, ipady=6)

        tk.Label(
            device_frame,
            text="Rental Date:",
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        rental.rental_calendar = DateEntry(device_frame, width=10, date_pattern="mm-dd-yyyy", font=("Arial", 9))
        rental.rental_calendar.grid(row=2, column=1, sticky="w", padx=5, ipady=6)

        tk.Label(
            device_frame,
            text="Return By:",
            font=("Arial", 12, "bold")
        ).grid(row=2, column=2, sticky="w", padx=5, pady=5)

        rental.return_calendar = DateEntry(device_frame, width=10, date_pattern="mm-dd-yyyy", font=("Arial", 9))
        rental.return_calendar.grid(row=2, column=3, sticky="w", padx=5, pady=5, ipady=6)


        #bottom
        bottom_bar = tk.Frame(form_frame, padx=10, pady=20, bg="#eef2f7")
        bottom_bar.grid(row =4, column =0, columnspan=4, sticky="ew", padx=10, pady=(0,10))

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
            cursor="hand2"
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
        rental.add_hover(back_btn, "#232624", "#eef2f7", "white", "black")
        rental.add_hover(reset_btn, "#232624", "#eef2f7", "white", "black")


        # Add the rental py logic below.
        # Wire up DB and button handlers
        make_database()

        def populate_devices():
            conn = get_connection()
            try:
                devices = get_all_available_devices(conn)
                # Store mapping device display -> (id, price)
                vals = []
                rental._device_map = {}
                for d in devices:
                    # d: (DeviceID, Model, SerialNumber, RentalPrice, TypeName, BrandName)
                    display = f"{d[1]} (ID {d[0]}) — ₱{d[3]:.2f}"
                    vals.append(display)
                    rental._device_map[display] = (d[0], float(d[3]))
                rental.device_combobox['values'] = vals
            finally:
                conn.close()

        def reset_form():
            for e in rental.entries.values():
                e.delete(0, 'end')
            rental.contact_entry.delete(0, 'end')
            rental.email_entry.delete(0, 'end')
            rental.device_combobox.set('')

        def submit_rental():
            # Gather rentee info
            first = rental.entries.get('First Name').get().strip()
            middle = rental.entries.get('Middle Name').get().strip()
            last = rental.entries.get('Last Name').get().strip()
            suffix = rental.entries.get('Suffix').get().strip()
            contact = rental.contact_entry.get().strip()
            email = rental.email_entry.get().strip()
            device_display = rental.device_combobox.get().strip()
            # UI uses a DateEntry named `return_calendar`
            return_date = rental.return_calendar.get_date()

            if not (first and last and contact and email and device_display and return_date):

                messagebox.showwarning("Missing Data", "Please fill in all required fields.")
                return

            device_info = rental._device_map.get(device_display)
            if not device_info:
                messagebox.showerror("Device Error", "Selected device is not available.")
                return

            device_id, price = device_info

            # Dates
            s_date = rental.rental_calendar.get_date()
            s_month, s_day, s_year = s_date.month, s_date.day, s_date.year

            # Expected return date comes directly from the DateEntry `return_calendar`
            ex_month, ex_day, ex_year = return_date.month, return_date.day, return_date.year


            conn = get_connection()
            try:
                # Try to add customer; if exists, find existing id.
                # NOTE: db.sqlite_crudop.add_customer requires address fields too.
                try:
                    customer_id = add_customer(
                        conn,
                        first, middle, last, suffix,
                        contact, email,
                        "", "", "", "", ""  # Street, Barangay, City, Province, ZIPCode (not collected in this form yet)
                    )

                except Exception:
                    # likely unique constraint; lookup existing customer by contact or email
                    cur = conn.cursor()
                    cur.execute('SELECT CustomerID FROM Customer WHERE ContactNumber = ? OR EmailAddress = ?', (contact, email))
                    row = cur.fetchone()
                    if row:
                        customer_id = row[0]
                    else:
                        raise

                # Use a default staff id (1). Adjust if you have staff login flow.
                staff_id = 1

                total_fee = price * 1  # single device; expand for multiple items

                rental_id = create_rental_transaction(conn, s_month, s_day, s_year, ex_month, ex_day, ex_year, 'Ongoing', total_fee, customer_id, staff_id)

                # Mark device as rented
                update_device_availability(conn, device_id, 'Rented')

                messagebox.showinfo("Success", f"Rental created (ID: {rental_id}).")
                reset_form()
                populate_devices()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

        # Attach handlers
        create_btn.config(command=submit_rental)
        reset_btn.config(command=reset_form)

        # initial population
        populate_devices()