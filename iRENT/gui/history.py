import tkinter as tk

def create_history_page(main_frame, app):

    title = tk.Label(
        main_frame,
        text="RENTAL HISTORY",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.pack(pady=20)

    # container for all order cards
    container = tk.Frame(main_frame)
    container.pack(fill="both", expand=True, padx=20)

    # example rentee info
    orders = [
        {"id": "001", "name": "Daniel Padilla"},
        {"id": "002", "name": "Hughie Campbell"},
        {"id": "003", "name": "Kurt Cobain"},
        {"id": "004", "name": "Chappell Roan"},
        {"id": "005", "name": "Wally Bayola"},
    ]

    for order in orders:

        #card
        card = tk.Frame(
            container,
            highlightbackground="black",
            highlightthickness=1
        )
        card.pack(fill="x", pady=8)

        #left info
        left = tk.Frame(card)
        left.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        tk.Label(
            left,
            text=f"Rental ID {order['id']}",
            font=("Arial", 14, "bold"),
            fg="black"
        ).pack(anchor="w")

        tk.Label(
            left,
            text=f"Rentee Name: {order['name']}",
            font=("Arial", 12),
            fg="black"
        ).pack(anchor="w")

        #right (butotn)
        btn = tk.Button(
            card,
            text="See More",
            bg="#ffd735",
            fg="black",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            command=lambda o=order: show_history_details(app, o)
        )
        btn.pack(side="right", padx=10, pady=10)

def show_history_details(app, order):
    frame = app.pages["history_details"]
    for w in frame.winfo_children():
        w.destroy()

    container = tk.Frame(frame, padx=40, pady=40)
    container.pack(fill="both", expand=True)

    container.grid_columnconfigure(0, weight=1, minsize=300)
    container.grid_columnconfigure(1, weight=1, minsize=300)

    #renta info
    tk.Label(
        container, 
        text=f"Rental ID: {order['id']}", 
        font=("Arial", 14, "bold")
    ).grid(row=0, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text=f"Rentee Name: {order['name']}", 
        font=("Arial", 14, "bold")
    ).grid(row=0, column=1, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Contact Number: 123456789", 
        font=("Arial", 14, "bold")
    ).grid(row=1, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Email Address: testcase@gmail.com", 
        font=("Arial", 14, "bold")
    ).grid(row=1, column=1, sticky="w", pady=10)

    #line
    tk.Frame(
        container, 
        height=2, bg="black"
    ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)

    #device rented
    tk.Label(
        container, 
        text="Device Rented: Device 1", 
        font=("Arial", 14, "bold")
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

    tk.Frame(
        container, 
        height=2, 
        bg="black"
    ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=20)

    #dates
    tk.Label(
        container,
        text="Rental Date: 06/11/2026", 
        font=("Arial", 14, "bold")
    ).grid(row=5, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Must Return By: 06/12/2026", 
        font=("Arial", 14, "bold")
    ).grid(row=5, column=1, sticky="w", pady=10)
    
    tk.Label(
        container,
        text="Date Returned: 06/12/2026",
        font=("Arial", 14, "bold")
    ).grid(row=6, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Rental Total: 0.00 PHP", 
        font=("Arial", 14, "bold")
    ).grid(row=7, column=0, sticky="w", pady=20)

    tk.Label(
        container,
        text="Penalty Fee: 0.00 PHP",
        font=("Arial", 14, "bold")
    ).grid(row=7, column=1, sticky="w", pady=20)

    bottom_bar = tk.Frame(frame, padx=40, pady=20)
    bottom_bar.pack(fill="x", side="bottom")

    tk.Button(
      bottom_bar,
      text="Back",
      font=("Arial", 17),
      command=lambda: app.pages["history"].tkraise()
      ).pack(side="right", padx=5)
    
    app.pages["history_details"].tkraise()

