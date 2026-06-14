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


def add_rental_page(container_frame,rental):
        for widget in container_frame.winfo_children():
            widget.destroy()

        form_frame = tk.LabelFrame(
            container_frame,
            relief="flat",
            labelanchor="n",
            bd=0
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_rowconfigure(0, weight=0) #rentee info
        form_frame.grid_rowconfigure(1, weight=0) #contact infp
        form_frame.grid_rowconfigure(2, weight=0) #device rental
        form_frame.grid_rowconfigure(3, weight=1) #buttons/bottom bar
        form_frame.grid_columnconfigure(0, weight=1) #stretch horizontally

        rentee_info_frame = tk.LabelFrame(
            form_frame,
            bd=0,
            relief="flat"
        )
        rentee_info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        for col in range(4):
            rentee_info_frame.grid_columnconfigure(col, weight=0)

        rentee_title = tk.Label(
            rentee_info_frame,
            text="RENTEE INFO",
            font=("Arial", 20, "bold")
        )
        rentee_title.grid(row=0, column=0, sticky="w", padx=5, pady=5, columnspan=4)

        fields = ["First Name", "Middle Name", "Last Name", "Suffix"]

        rental.entries = {}

        for index, field_name in enumerate(fields):
            label = tk.Label(
                rentee_info_frame,
                text=field_name,
                fg="black",
                font=("Arial", 12)
            )
            label.grid(row=1, column=index, padx=5, pady=(5, 0))

            entry = tk.Entry(rentee_info_frame, width=20)
            entry.grid(row=2, column=index, padx=10, pady=(10, 20), ipady=6, sticky="ew")

            rental.entries[field_name] = entry

        contact_frame = tk.LabelFrame(
            form_frame,
            text="CONTACT INFO",
            font=("Arial", 20, "bold"),
            bd=0
        )
        contact_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(40, 30))

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
        device_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(40, 30))

        tk.Label(
            device_frame,
            text="DEVICE RENTAL",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, sticky="w", columnspan=4)

        tk.Label(
            device_frame,
            text="Device to Rent:",
            font=("Arial", 12, "bold")
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        rental.device_combobox = ttk.Combobox(device_frame, values=["Device 1", "Device 2"])
        rental.device_combobox.grid(row=1, column=1, sticky="w", padx=5, pady=5, ipady=6)

        tk.Label(
            device_frame,
            text="Rental Date:",
            font=("Arial", 12, "bold")
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        rental.rental_calendar = DateEntry(device_frame, width=12, date_pattern="mm-dd-yyyy")
        rental.rental_calendar.grid(row=2, column=1, sticky="w", padx=5, pady=5, ipady=6)

        tk.Label(
            device_frame,
            text="Must Return By:",
            font=("Arial", 12, "bold")
        ).grid(row=2, column=2, sticky="w", padx=5, pady=5)

        rental.return_by = ttk.Combobox(device_frame, values=["1 day", "3 days"])
        rental.return_by.grid(row=2, column=3, sticky="w", padx=5, pady=5, ipady=6)

        bottom_bar = tk.Frame(form_frame, padx=40, pady=20, bg="#eef2f7")
        bottom_bar.grid(row =4, column =0, columnspan=4, sticky="sew", padx=10, pady=20)

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
        cursor="hand2",
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
        )
        reset_btn.pack(side="right", padx=5)

        rental.add_hover(create_btn, "#232624", "#ffd735", enter_fg="#ffd735", leave_fg="black")
        rental.add_hover(back_btn, "#232624", "gray", "white", "black")
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
            rental.return_by.set('')

        def submit_rental():
            # Gather rentee info
            first = rental.entries.get('First Name').get().strip()
            middle = rental.entries.get('Middle Name').get().strip()
            last = rental.entries.get('Last Name').get().strip()
            suffix = rental.entries.get('Suffix').get().strip()
            contact = rental.contact_entry.get().strip()
            email = rental.email_entry.get().strip()
            device_display = rental.device_combobox.get().strip()
            return_by_text = rental.return_by.get().strip()

            if not (first and last and contact and email and device_display and return_by_text):
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

            # Compute expected return date from `return_by` (e.g. "1 day", "3 days")
            days = 1
            try:
                days = int(return_by_text.split()[0])
            except Exception:
                days = 1
            ex_date = s_date + datetime.timedelta(days=days)
            ex_month, ex_day, ex_year = ex_date.month, ex_date.day, ex_date.year

            conn = get_connection()
            try:
                # Try to add customer; if exists, find existing id
                try:
                    customer_id = add_customer(conn, first, middle, last, suffix, contact, email)
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