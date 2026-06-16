import tkinter as tk
from PIL import Image, ImageTk
import os

orders = [
        {"id": "001", "rentee": "Jose Manalo", "contact": "123123123", "email": "asdasd@gmail.com", "address": "dyan lang sa tabi"},
        {"id": "002", "rentee": "William Butcher", "contact": "123123123", "email": "asdasd@gmail.com", "address": "New York, NY 10001, United States"},
        {"id": "003", "rentee": "Hev Abi", "contact": "123123123", "email": "asdasd@gmail.com", "address": "dyan lang sa tabi"},
    ]
        

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

def rental_customers(app, order):
    cframe = app.pages["show_details"]
    for w in cframe.winfo_children():
        w.destroy()
    
    cframe.configure(bg="#eef2f7")
    container = tk.Frame(cframe, padx=40, pady=40, bg="#eef2f7")
    container.pack(fill="both", expand=True)

    tk.Label(
        container, 
        text=f"ID: {order['id']}", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=0, column=0, sticky="w", pady=10)
    tk.Label(
        container, 
        text=f"Rentee: {order['rentee']}", 
        font=("Arial", 14, "bold"), bg="#eef2f7"
    ).grid(row=1, column=0, sticky="w", pady=10)

    back_btn = tk.Button(
        cframe, 
        text="Back", 
        font=("Arial", 14), 
        command=lambda: app.pages["rentals"].tkraise()
    )
    back_btn.pack(side="bottom", pady=20)
    
    cframe.tkraise()

def customers_page(main_frame, app):
    main_frame.configure(bg="#eef2f7")

    title = tk.Label(
        main_frame, 
        text="CUSTOMERS", 
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

    search = tk.Entry(
        searchfilter, 
        font=("Arial", 12), 
        width=15
    )
    search.insert(0, "Search...")
    search.pack(side="right")

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
        menu.add_command(label="Show Active", command=lambda: print("Filtering Active..."))
        menu.add_command(label="Show Overdue", command=lambda: print("Filtering Active..."))
        menu.add_command(label="Show Completed", command=lambda: print("Filtering Active..."))
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


    table_wrapper = tk.Frame(main_frame, bg="#eef2f7")
    table_wrapper.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(table_wrapper, bg="#eef2f7", highlightthickness=0)
    v_scroll = tk.Scrollbar(table_wrapper, orient="vertical", command=canvas.yview)
    #h_scroll = tk.Scrollbar(table_wrapper, orient="horizontal", command=canvas.xview)
    
    scrollable_frame = tk.Frame(canvas, bg="#eef2f7")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    v_scroll.pack(side="right", fill="y")
    #h_scroll.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    

    headers = ["Customer ID", "Name", "Contact Number", "Email", "Address"]
    for i, head in enumerate(headers):
        tk.Label(
            scrollable_frame, 
            text=head, 
            font=("Arial", 12, "bold"), 
            bg="#ffd735", 
            width=16, 
            relief="solid", 
            borderwidth=1
        ).grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

    def highlight_row(event,row_idx, color):
        for child in scrollable_frame.winfo_children():
            if isinstance(child, tk.Label) and child.grid_info().get('row') == row_idx: child.configure(bg=color)

    for i, order in enumerate(orders, start=1):
        row_data = [order['id'], order['rentee'], order['contact'], order['email'], order['address']]
        
        for col, val in enumerate(row_data):
            wrap_limit = 140 if col == 4 else None

            cell = tk.Label(
                scrollable_frame, 
                text=val, 
                bg="white", 
                font=("Arial", 11),
                width=20,
                relief="solid", 
                wraplength=wrap_limit,
                borderwidth=1,
                cursor="hand2"
            )
            cell.grid(row=i, column=col, sticky="nsew")
            
            cell.bind("<Button-1>", lambda e, o=order: customer_details(app, o))
            cell.bind("<Enter>", lambda e, r=i: highlight_row(e, r, "#f0f0f0"))
            cell.bind("<Leave>", lambda e, r=i: highlight_row(e, r, "white"))

        scrollable_frame.grid_rowconfigure(i, minsize=35)

    bottom = tk.Frame(main_frame, padx=40, pady=20, bg="#eef2f7")
    bottom.pack(fill="x", side="bottom")

    add_btn = tk.Button(
        bottom,
        text="Add Customer",
        font=("Arial", 17, "bold"),
        bg="#ffd735",
        command=lambda: app.set_active_page("add_rental")
    )
    add_btn.pack(side="right", padx=5)
    add_hover(add_btn, "#232624", "#ffd735", "#ffd735", "black")


def customer_details(app, order):
    frame = app.pages["customer_details"]
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
        text=f"Rentee Name: {order['rentee']}",
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

    back_btn = tk.Button(
        bottom_bar,
        text="Back",
        font=("Arial", 17, "bold"),
        bg="gray",
        cursor="hand2",
        command=lambda: app.pages["customers"].tkraise()
    )
    back_btn.pack(side="right", padx=5)
    add_hover(back_btn, "#232624", "gray", "white", "black")

    frame.tkraise()