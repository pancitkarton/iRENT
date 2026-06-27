import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

from db.database import get_connection
from db.view_rentals_logic import (
    get_all_rentals,
    display_rentals,
    get_rentals_by_status,
    search_rentals,
    get_rental_details,
    mark_rental_as_completed
)

status_colors = {
        "Ongoing": "#ebc427",
        "Overdue": "#D9534F",
        "Completed": "#5CB85C"
    }

def add_hover(btn, enter_bg, leave_bg, enter_fg=None, leave_fg=None):
    def on_enter(e):
        btn.config(bg=enter_bg, cursor="hand2")
        if enter_fg:
            btn.config(fg=enter_fg)
    def on_leave(e):
        btn.config(bg=leave_bg, cursor="")
        if leave_fg:
            btn.config(fg=leave_fg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def refresh_rental_list(app, container, rentals_data):
    # Clear existing cards
    for widget in container.winfo_children():
        widget.destroy()

    # Recreate cards with new data
    for order in rentals_data:
        card = tk.Frame(
            container,
            bg="white",
            highlightbackground="black",
            highlightthickness=1
        )
        card.pack(fill="x", pady=4)

        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side="left", fill="y", padx=10, pady=5)

        tk.Label(info_frame, text=f"ID: {order['id']}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Rentee: {order['rentee']}", font=("Arial", 12), bg="white").pack(anchor="w")

        actions_frame = tk.Frame(card, bg="white")
        actions_frame.pack(side="right", padx=10)

        status_color = status_colors.get(order['status'], "black")
        tk.Label(
            actions_frame,
            text=f"Status: {order['status']}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=status_color,
            anchor="w",
            width=15
        ).pack(side="left", padx=30)

        btn = tk.Button(
            actions_frame, text="See More", bg="#ffd735", fg="black",
            font=("Arial", 11, "bold"), relief="flat", padx=15, pady=2,
            cursor="hand2",
            command=lambda a=app, oid=order['id']: show_details(a, oid)
        )
        btn.pack(side="left", padx=10)
        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")


def open_receipt(order):
    receipt_win = tk.Toplevel()
    receipt_win.title("Rental Receipt")
    receipt_win.configure(bg="white")

    tk.Label(
        receipt_win,
        text="OFFICIAL RECEIPT",
        font=("Arial", 20, "bold", "italic"),
        bg="white"
    ).pack(pady=20)

    details_frame = tk.Frame(receipt_win, bg="white")
    details_frame.pack(fill="x", padx=40)

    # SAFELY PARSE DYNAMIC FEE CALCULATION
    raw_fee = order.get('total_fee', 0.00)
    base_fee = float(raw_fee) if raw_fee is not None else 0.00

    is_overdue = (order.get('status') == "Overdue")
    penalty = 0.00

    # Calculate penalty based on exactly how many days late they are
    if is_overdue:
        try:
            expected_date = datetime.strptime(order.get('expected_return', ''), "%m-%d-%Y").date()
            today = datetime.today().date()
            days_late = max(1, (today - expected_date).days)
            penalty = 300.00 * days_late
        except Exception:
            penalty = 300.00 # Fallback

    total = base_fee + penalty

    items = [
        ("Rental ID:", order.get('id', 'N/A')),
        ("Rentee:", order.get('rentee', 'N/A')),
        ("------------------------------------------------------", ""),
        ("Rental Fee:", f"{base_fee:.2f} PHP"),
        ("Overdue Penalty Fee:", f"{penalty:.2f} PHP"),
        ("------------------------------------------------------", ""),
        ("TOTAL DUE:", f"{total:.2f} PHP")
    ]

    for label, val in items:
        row = tk.Frame(details_frame, bg="white")
        row.pack(fill="x", pady=2)

        tk.Label(
            row,
            text=label,
            font=("Arial", 12),
            bg="white"
        ).pack(side="left")

        tk.Label(
            row,
            text=val,
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side="right")

    close_btn = tk.Button(
        receipt_win,
        text="CLOSE",
        font=("Arial", 10, "bold"),
        command=receipt_win.destroy,
        bg="#ffd735"
    )
    close_btn.pack(pady=30)
    add_hover(close_btn, "#232624", "#ffd735", "#ffd735", "black")


def rentals_page(main_frame, app):
    main_frame.configure(bg="#eef2f7")

    title = tk.Label(
        main_frame,
        text="RENTALS",
        font=("Arial", 30, "bold"),
        fg="black",
        bg="#eef2f7")
    title.pack(pady=25)

    tk.Frame(
        main_frame,
        height=2,
        bg="black"
    ).pack(fill="x", padx=20, pady=5)

    searchfilter = tk.Frame(
        main_frame,
        bg="#eef2f7")
    searchfilter.pack(fill="x", padx=20, pady=10)

    swrap = tk.Frame(searchfilter, bg="#eef2f7", highlightthickness=0 )
    swrap.pack(side="right", padx=(10,0))

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_path = os.path.join(BASE_DIR, "assets", "search.png")
    search_icon = ImageTk.PhotoImage(Image.open(search_path).resize((20, 20)))

    icon_label = tk.Label(swrap, image=search_icon, bg="#eef2f7")
    icon_label.image=search_icon
    icon_label.pack(side="right")

    search = tk.Entry(searchfilter, font=("Arial", 12), width=15)
    search.insert(0, "Search...")
    search.pack(side="right")

    scroll_wrapper = tk.Frame(main_frame, bg="#eef2f7")
    scroll_wrapper.pack(fill="both", expand=True, padx=20)

    canvas = tk.Canvas(scroll_wrapper, bg="#eef2f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    container = tk.Frame(canvas, bg="#eef2f7")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas_window = canvas.create_window((0,0), window=container, anchor="nw")

    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    app.rental_list_container = container

    def trigger_search(event=None):
        term = search.get().strip()
        if term == "" or term == "Search...":
            refresh_rental_list(app, container, get_rentals_by_status("Ongoing")) # Load Ongoing when cleared
        else:
            refresh_rental_list(app, container, search_rentals(term))

    search.bind("<KeyRelease>", trigger_search)

    def on_focus_in(event):
        if search.get() == "Search...":
            search.delete(0, "end")
            search.config(fg="black")

    def on_focus_out(event):
        if search.get() == "":
            search.insert(0, "Search...")
            search.config(fg="gray")

    search.bind("<FocusIn>", on_focus_in)
    search.bind("<FocusOut>", on_focus_out)
    search.config(fg="gray")

    def filter_menu(event):
        menu = tk.Menu(main_frame, tearoff=0)
        menu.add_command(label="Show All", command=lambda: refresh_rental_list(app, container, get_all_rentals())) # Added option to view all
        menu.add_command(label="Show Ongoing", command=lambda: refresh_rental_list(app, container, get_rentals_by_status("Ongoing")))
        menu.add_command(label="Show Overdue", command=lambda: refresh_rental_list(app, container, get_rentals_by_status("Overdue")))
        menu.add_command(label="Show Completed", command=lambda: refresh_rental_list(app, container, get_rentals_by_status("Completed")))
        menu.post(event.x_root, event.y_root)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filter_path = os.path.join(BASE_DIR, "assets", "filter.png")
    filter_icon = ImageTk.PhotoImage(Image.open(filter_path).resize((25, 25)))

    filter_label = tk.Label(
        searchfilter,
        text="Filter",
        image=filter_icon,
        compound="left",
        justify="center",
        font=("Arial", 12, "bold"),
        bg="#eef2f7",
        fg="#e6b800",
        cursor="hand2",
        padx=5
    )
    filter_label.image = filter_icon
    filter_label.pack(side="right", padx=10)
    filter_label.bind("<Button-1>", filter_menu)

    add_hover(filter_label, "#eef2f7", "#eef2f7", "black", "#e6b800")

    # Load initial data (Default to Ongoing)
    refresh_rental_list(app, container, get_rentals_by_status("Ongoing"))

    bottom = tk.Frame(main_frame, padx=40, pady=20, bg="#eef2f7")
    bottom.pack(fill="x", side="bottom")

    add_btn = tk.Button(
        bottom,
        text="Add Rental",
        font=("Arial", 17, "bold"),
        bg="#ffd735",
        command=lambda: app.set_active_page("add_rental")
    )
    add_btn.pack(side="right", padx=5)
    add_hover(add_btn, "#232624", "#ffd735", "#ffd735", "black")


def show_details(app, order_id):
    app.set_active_page("order_details")

    frame = app.pages["order_details"]
    for w in frame.winfo_children():
        w.destroy()

    frame.configure(bg="#eef2f7")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)

    order = get_rental_details(order_id)
    if not order:
        return

    for w in frame.winfo_children():
        w.destroy()

    container_details = tk.Frame(
        frame,
        padx=40,
        pady=40,
        bg="#eef2f7"
    )
    container_details.grid(row=0, column=0, sticky="nsew")

    container_details.grid_columnconfigure(0, weight=1, minsize=300)
    container_details.grid_columnconfigure(1, weight=1, minsize=300)

    tk.Label(
        container_details,
        text="RENTAL INFO",
        font=("Arial", 20, "bold"),
        bg="#eef2f7"
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    tk.Label(
        container_details,
        text=f"Rental ID: {order.get('id', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=1, column=0, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Rental Date: {order.get('start_date', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=2, column=0, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Must Return By: {order.get('expected_return', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
        ).grid(row=1, column=1, sticky="w",  pady=(0,10))

    raw_fee = order.get('total_fee', 0.00)
    base_fee = float(raw_fee) if raw_fee is not None else 0.00

    is_overdue = (order.get('status') == "Overdue")
    penalty = 0.00

    if is_overdue:
        try:
            expected_date = datetime.strptime(order.get('expected_return', ''), "%m-%d-%Y").date()
            today = datetime.today().date()
            days_late = max(1, (today - expected_date).days)
            penalty = 300.00 * days_late
        except Exception:
            penalty = 300.00

    total_due = base_fee + penalty

    tk.Label(
        container_details,
        text=f"Overdue Fee: ₱{penalty:.2f}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7",
        fg="red" if is_overdue else "black"
        ).grid(row=2, column=1, sticky="w",  pady=(0,10))

    tk.Frame(
        container_details,
        height=2,
        bg="black"
    ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)

    tk.Label(
        container_details,
        text="CUSTOMER INFO",
        font=("Arial", 20, "bold"),
        bg="#eef2f7"
    ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))

    tk.Label(
        container_details,
        text=f"Customer ID: {order.get('customer_id', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=5, column=0, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Contact Number: {order.get('contact number', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=5, column=1, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Rentee Name: {order.get('rentee', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=6, column=0, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Email Address: {order.get('email address', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=6, column=1, sticky="w",  pady=(0,10))

    tk.Frame(
        container_details,
        height=2,
        bg="black"
    ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=20)

    tk.Label(
        container_details,
        text="DEVICE INFORMATION",
        font=("Arial", 20, "bold"),
        bg="#eef2f7"
    ).grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 10))


    tk.Label(
        container_details,
        text=f"Device ID: {order.get('device_id', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=9, column=0, sticky="w",  pady=(0,10))

    tk.Label(
        container_details,
        text=f"Serial Number: {order.get('serial_number', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=9, column=1, sticky="w", pady=(0,10))


    tk.Label(
        container_details,
        text=f"Brand: {order.get('brand', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=10, column=0, sticky="w", pady=(0,10))

    tk.Label(
        container_details,
        text=f"Model: {order.get('model', 'N/A')}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=10, column=1, sticky="w", pady=(0,10))

    raw_dev_price = order.get('device_price', 0.00)
    dev_price = float(raw_dev_price) if raw_dev_price is not None else 0.00

    tk.Label(
        container_details,
        text=f"Daily Rate: ₱{dev_price:.2f}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=11, column=0, sticky="w", pady=(0,10))

    #bottom
    bottom_bar = tk.Frame(
        frame,
        padx=40,
        pady=20,
        bg="#eef2f7"
    )
    bottom_bar.grid(row=1, column=0, sticky="ew")

    scolor = status_colors.get(order['status'], "black")

    total_box = tk.Frame(
        bottom_bar,
        bg="white",
        highlightbackground="black",
        highlightthickness=1
    )
    total_box.pack(side="left", pady=5)

    tk.Label(
        total_box,
        text="TOTAL DUE",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#9B8F8F"
        ).pack(padx=10, pady=(5, 0))

    tk.Label(
        total_box,
        text=f"₱ {total_due:.2f}",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#D9534F" if is_overdue else "black"
    ).pack(padx=10, pady=(0, 5))

    tk.Label(
        bottom_bar,
        text=f"Rental Status: {order['status']}",
        font=("Arial", 18, "italic", "bold"),
        fg=scolor,
        bg="#eef2f7"
    ).pack(side="left", padx=20)

    back_btn = tk.Button(
        bottom_bar,
        text="Back",
        font=("Arial", 17, "bold"),
        bg="gray",
        cursor="hand2",
        command=lambda: app.pages["rentals"].tkraise()
    )
    back_btn.pack(side="right", padx=5)
    add_hover(back_btn, "#232624", "gray", "white", "black")

    if order['status'] != "Completed":
        def complete_action():
            try:
                # Safely execute the logic function
                mark_rental_as_completed(order['id'])

                # FORCE update as a failsafe, guaranteeing the button finishes its job
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE Rental SET RentalStatus = 'Completed' WHERE RentalID = ?", (order['id'],))
                if order.get('device_id'):
                    cursor.execute("UPDATE Device SET AvailabilityStatus = 'Available' WHERE DeviceID = ?", (order['device_id'],))
                conn.commit()
                conn.close()

                # Trigger GUI Updates
                open_receipt(order)
                app.pages["rentals"].tkraise()
                # Reload Ongoing rentals after completing one
                refresh_rental_list(app, app.rental_list_container, get_rentals_by_status("Ongoing"))

            except Exception as e:
                # Give a popup warning if anything actually breaks!
                messagebox.showerror("System Error", f"Failed to complete rental:\n{e}")

        complete_btn = tk.Button(
            bottom_bar,
            text="COMPLETE RENTAL",
            font=("Arial", 17, "bold"),
            bg="#ffd735",
            cursor="hand2",
            command=complete_action
        )
        complete_btn.pack(side="right", padx=5)
        add_hover(complete_btn, "#232624", "#ffd735", "#ffd735", "black")

    frame.tkraise()