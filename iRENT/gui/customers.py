import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from db.customers_logic import get_all_customers, update_customer_db
from db.validation import validate_input
import re


def display_table(app, table_wrapper, customer_list, refresh_callback=None):
    for widget in table_wrapper.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(table_wrapper, bg="#eef2f7", highlightthickness=0)
    v_scroll = tk.Scrollbar(table_wrapper, orient="vertical", command=canvas.yview)
    h_scroll = tk.Scrollbar(table_wrapper, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, bg="#eef2f7")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    def highlight_row(event, row_idx, color):
        for child in scrollable_frame.winfo_children():
            if isinstance(child, tk.Label) and child.grid_info().get('row') == row_idx:
                child.configure(bg=color)

    headers = ["ID", "First Name", "Middle Name", "Last Name", "Suffix", 
               "Birthday", "Contact", "Email", "Region", "City", 
               "Barangay", "ZIP", "Street"]
    
    for i, head in enumerate(headers):
        tk.Label(scrollable_frame, text=head, font=("Arial", 10, "bold"), 
                 bg="#ffd735", width=12, relief="solid", bd=1).grid(row=0, column=i)

    for i, customer in enumerate (customer_list, start=1):

        display_data = {
                'Customer ID': customer['CustomerID'],
                'First Name': customer['FirstName'],
                'Middle Name': customer['MiddleName'],
                'Last Name': customer['LastName'],
                'Suffix': customer['Suffix'],
                'Contact Number': customer['ContactNumber'],
                'Email': customer['EmailAddress'],
                'Birthday': customer['Birthday'],
                'Street/Bldg': customer['Street'],
                'Barangay': customer['Barangay'],
                'City': customer['City'],
                'Region': customer['Region'],
                'ZIP/Postal': customer['Postal']
            }
            
        row_data = [
                customer['CustomerID'], customer['FirstName'], customer['MiddleName'],
                customer['LastName'], customer['Suffix'], customer['Birthday'],
                customer['ContactNumber'], customer['EmailAddress'], customer['Region'],
                customer['City'], customer['Barangay'], customer['Postal'], customer['Street']
            ]
            
        for col, val in enumerate(row_data):
                cell = tk.Label(
                    scrollable_frame, 
                    text=val, 
                    bg="white", 
                    width=12, 
                    relief="solid",
                    bd=1,
                    cursor="hand2"
                )
                cell.grid(row=i, column=col, sticky="nsew")
                
                cell.bind("<Button-1>", lambda e, c=display_data: customer_details(app, c, refresh_callback))
                cell.bind("<Enter>", lambda e, r=i: highlight_row(e, r, "#f0f0f0"))
                cell.bind("<Leave>", lambda e, r=i: highlight_row(e, r, "white"))

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

def edit_details(order, refresh_callback):
    edit_win = tk.Toplevel()
    edit_win.title("Edit Customer Details")
    edit_win.configure(bg="#eef2f7")

    vcmd_num = (edit_win.register(lambda P: validate_input(P, "numbers", length=11)), '%P')
    vcmd_alpha = (edit_win.register(lambda P: validate_input(P, "alpha")), '%P')
    vcmd_suffix = (edit_win.register(lambda P: validate_input(P, "suffix", length=5)), '%P')
    vcmd_email = (edit_win.register(lambda P: validate_input(P, "email")), '%P')
    
    entries = {}

    tk.Label(
        edit_win,
        text="EDIT CUSTOMER DETAILS",
        font=("Arial", 15, "bold", "italic"),
        bg="#eef2f7"
    ).grid(row=0, column=0, columnspan=2, pady=15, padx=10)
    
    for i, (key, value) in enumerate(order.items()):
        row_idx = i + 1 
        tk.Label(edit_win, text=key, font=("Arial", 10, "bold"), bg="#eef2f7").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        ent = tk.Entry(edit_win, width=30)
        ent.insert(0, str(value))
        ent.grid(row=row_idx, column=1, padx=10, pady=5)
        entries[key] = ent

        if key in ["First Name", "Middle Name", "Last Name"]:
            ent.config(validate="key", validatecommand=vcmd_alpha)
        elif key == "Suffix":
            ent.config(validate="key", validatecommand=vcmd_suffix)
        elif key == "Contact Number":
            ent.config(validate="key", validatecommand=vcmd_num)
        elif key == "Email":
            ent.config(validate="key", validatecommand=vcmd_email)

    def save_changes():
        email = entries['Email'].get()
        contact = entries['Contact Number'].get()

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email address.")
            return
        
        if len(contact) < 11:
            messagebox.showerror("Error", "Contact number must be 11 digits.")
            return
        

        confirmed = messagebox.askyesno("Confirm", "Are you sure you want to save changes?")

        if not confirmed:
            return
        
        field_map = {
            'Customer ID': 'CustomerID', 
            'First Name': 'FirstName', 
            'Last Name': 'LastName', 
            'Suffix': 'Suffix',
            'Contact Number': 'ContactNumber',
            'Email': 'EmailAddress', 
            'Birthday': 'Birthday',
            'Street/Bldg': 'Street', 
            'Barangay': 'Barangay',
            'City': 'City', 
            'Region': 'Region', 
            'ZIP/Postal': 'Postal'
        }
        
        updated_data = {field_map.get(key, key): ent.get() for key, ent in entries.items()}

        customer_id = order['Customer ID']

        updated_data['MiddleName'] = order.get('MiddleName', '')
        updated_data['Suffix'] = order.get('Suffix', '')
        
        if update_customer_db(order['Customer ID'], updated_data):
            messagebox.showinfo("Success", "Yay! Customer details updated successfully.")
            edit_win.destroy()
            refresh_callback()
        else:
            tk.messagebox.showerror("Error", "Could not save to database.")

    save_btn = tk.Button(
        edit_win, 
        text="Save Changes", 
        font=("Arial", 12, "bold"), 
        bg="#ffd735", 
        command=save_changes
    )
    save_btn.grid(row=len(order)+1, columnspan=2, pady=20)
    add_hover(save_btn, "#232624", "#ffd735", "#ffd735", "black")

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



def customers_page(main_frame, app, refresh_callback):
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


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sort_path = os.path.join(BASE_DIR, "assets", "sort.png")
    sort_icon = ImageTk.PhotoImage(Image.open(sort_path).resize((25, 25)))

    sort_label = tk.Label(
        searchfilter, 
        text="Sort", 
        image=sort_icon, 
        compound="left", 
        justify="center",
        font=("Arial", 12, "bold"), 
        bg="#eef2f7", 
        fg="#e6b800", 
        cursor="hand2", 
        padx=5
    )
    sort_label.image = sort_icon
    sort_label.pack(side="right", padx=10)

    add_hover(sort_label, "#eef2f7", "#eef2f7", "black", "#e6b800")



    def load_table(data=None):
        if data is None:
            data = get_all_customers()
        display_table(app, table_wrapper, data, refresh)

    def refresh():
        load_table()

    #search and sort 
    def sort_data(key):
        all_cust = get_all_customers()
        if key == "alphabet":
            sorted_customer = sorted(all_cust, key=lambda x: (x.get('LastName', '').lower(), x.get('FirstName', '').lower()))
        else:
            sorted_customer = sorted(all_cust, key=lambda x: int(x.get('CustomerID', 0)))
        
        load_table(sorted_customer)

    def sort_menu(event):
        menu = tk.Menu(main_frame, tearoff=0)
        menu.add_command(label="Sort by Alphabet", command=lambda: sort_data("alphabet"))
        menu.add_command(label="Sort by ID", command=lambda: sort_data("id"))
        menu.post(event.x_root, event.y_root)

    def on_search(event=None):
        query = search.get().lower()
        if query == "search..." or query == "":
            load_table()
        else:
            all_cust = get_all_customers()
            filtered = [
                c for c in all_cust 
                if query in c['FirstName'].lower() or 
                    query in c['LastName'].lower()
            ]
            load_table(filtered)

        
    table_wrapper = tk.Frame(main_frame, bg="#eef2f7")
    table_wrapper.pack(fill="both", expand=True, padx=20, pady=10)

    
    sort_label.bind("<Button-1>", sort_menu)
    search.bind("<KeyRelease>", on_search)

    load_table()



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



def customer_details(app, order, refresh_callback):
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

    tk.Label(
        container,
        text="CUSTOMER INFO",
        font=("Arial", 30, "bold"),
        bg="#eef2f7"
    ).grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="w")

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=1, column=0, columnspan=2, sticky="ew", pady=20)

    container.grid_columnconfigure(0, weight=1, minsize=300)
    container.grid_columnconfigure(1, weight=1)

    tk.Label(
        container,
        text=f"Customer ID: {order['Customer ID']}",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=2, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text=f"Full Name: {order['First Name']} {order['Last Name']}", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=2, column=1, sticky="w", pady=10)

    tk.Label(
        container, 
        text=f"Contact: {order['Contact Number']}", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=3, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text=f"Email: {order['Email']}", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=3, column=1, sticky="w", pady=10)

    tk.Label(
        container, 
        text=f"Birthday: {order['Birthday']}", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=4, column=0, sticky="w", pady=10)

    address_text = f"{order['Street/Bldg']}, {order['Barangay']}, {order['City']}, {order['Region']}, {order['ZIP/Postal']}"
    
    tk.Label(
        container, 
        text=f"Address: {address_text}",
        font=("Arial", 14, "bold"), 
        bg="#eef2f7",
        justify="left"
    ).grid(row=4, column=1, sticky="w", pady=10)

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=20)


    tk.Label(
        container,
        text="Total Devices Rented: 3",
        font=("Arial", 14, "bold"),
        bg="#eef2f7"
    ).grid(row=6, column=0, columnspan=2, sticky="w", pady=10)

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=20)



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

    add_btn = tk.Button(
        bottom_bar,
        text="Edit Details",
        font=("Arial", 17, "bold"),
        bg="#ffd735",
        command=lambda: edit_details(order, refresh_callback)    
    )
    add_btn.pack(side="right", padx=5)
    add_hover(add_btn, "#232624", "#ffd735", "#ffd735", "black")


    frame.tkraise()