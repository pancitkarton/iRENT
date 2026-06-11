import tkinter as tk


def create_orders(main_frame, app):

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

    main_frame.configure(bg="#eef2f7")

    title = tk.Label(
        main_frame,
        text="RENTAL ORDERS",
        font=("Arial", 24, "bold"),
        fg="black",
        bg="#eef2f7"
    )
    title.pack(pady=20)

    container = tk.Frame(main_frame, bg="#eef2f7")
    container.pack(fill="both", expand=True, padx=20)

    orders = [
        {"id": "001", "name": "Hev Abi"},
        {"id": "002", "name": "Rue Bennett"},
        {"id": "003", "name": "William Butcher"},
        {"id": "004", "name": "Fiona Gallagher"},
        {"id": "005", "name": "Thom Yorke"},
    ]

    for order in orders:

        card = tk.Frame(
            container,
            bg="white",
            highlightbackground="black",
            highlightthickness=1
        )
        card.pack(fill="x", pady=8)

        left = tk.Frame(card, bg="white")
        left.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        tk.Label(
            left,
            text=f"Rental ID {order['id']}",
            font=("Arial", 14, "bold"),
            fg="black",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            left,
            text=f"Rentee Name: {order['name']}",
            font=("Arial", 12),
            fg="black",
            bg="white"
        ).pack(anchor="w")

        btn = tk.Button(
            card,
            text="See More",
            bg="#ffd735",
            fg="black",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda o=order: show_details(app, o)
        )
        btn.pack(side="right", padx=10, pady=10)

        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")


def show_details(app, order):
    frame = app.pages["order_details"]
    frame.configure(bg="#eef2f7")

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

    for w in frame.winfo_children():
        w.destroy()

    container = tk.Frame(
        frame,
        padx=40,
        pady=40,
        bg="#eef2f7"
    )
    container.pack(fill="both", expand=True)

    container.grid_columnconfigure(0, weight=1, minsize=300)
    container.grid_columnconfigure(1, weight=1, minsize=300)

    tk.Label(
        container,
        text=f"Rental ID: {order['id']}",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=0, column=0, sticky="w", pady=10)

    tk.Label(
        container,
        text=f"Rentee Name: {order['name']}",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=0, column=1, sticky="w", pady=10)

    tk.Label(
        container,
        text="Contact Number: 123456789",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=1, column=0, sticky="w", pady=10)

    tk.Label(
        container,
        text="Email Address: testcase@gmail.com",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=1, column=1, sticky="w", pady=10)

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)

    tk.Label(
        container,
        text="Device Rented: Device 1",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=20)

    tk.Label(
        container,
        text="Rental Date: 06/11/2026",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=5, column=0, sticky="w", pady=10)

    tk.Label(
        container,
        text="Must Return By: 06/12/2026",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=5, column=1, sticky="w", pady=10)

    tk.Label(
        container,
        text="Rental Total: 0.00 PHP",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=6, column=0, sticky="w", pady=20)

    bottom_bar = tk.Frame(
        frame,
        padx=40,
        pady=20,
        bg="#eef2f7"
    )
    bottom_bar.pack(fill="x", side="bottom")

    tk.Label(
        bottom_bar,
        text="Rental Status: Ongoing",
        font=("Arial", 20, "italic", "bold"),
        fg="green",
        bg="#eef2f7"
    ).pack(side="left")

    back_btn = tk.Button(
        bottom_bar,
        text="Back",
        font=("Arial", 17),
        cursor="hand2",
        command=lambda: app.pages["orders"].tkraise()
    )
    back_btn.pack(side="right", padx=5)

    complete_btn = tk.Button(
        bottom_bar,
        text="COMPLETE RENTAL",
        font=("Arial", 17, "bold"),
        bg="#ffd735",
        cursor="hand2"
    )
    complete_btn.pack(side="right", padx=5)

    add_hover(back_btn, "#232624", "#eef2f7", "white", "black")
    add_hover(complete_btn, "#232624", "#ffd735", "#ffd735", "black")

    frame.tkraise()