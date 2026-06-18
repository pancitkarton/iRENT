import tkinter as tk
from PIL import Image, ImageTk
from db.view_rentals_logic import ( 
    get_connection, 
    get_rentals_by_status, 
    search_rentals, 
    get_rental_details, 
    mark_rental_as_completed
)

import os


orders = [  #temporary only, will delete when create rental exists
        {"id": "001", "rentee": "Daniel Padilla", "status": "Ongoing"},
        {"id": "002", "rentee": "Hughie Campbell", "status": "Overdue"},
        {"id": "003", "rentee": "Hev Abi", "status": "Completed"},
    ]

device_data = {
        "DeviceID": "D-999",
        "Model": "Asus Vivobook",
        "Serial Number": "123456789",
        "Appearance": "Slight Scratches",
        "Brand": "ASUS",
        "Device Type": "Laptop"
    }
        

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


#example receipt
#turn into completed status when done
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


    base_fee = 1000.00 
    is_overdue = (order['status'] == "Overdue")
    penalty = 300.00 if is_overdue else 0.00
    total = base_fee + penalty


    items = [
        ("Rental ID:", order['id']),
        ("Rentee:", order['rentee']),
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


    # SEARCH RENTALS BY NAME/ID FUNCTION
    # To be checked/revised by Garcia or Quitollo
    def search_rentals():
        search_term = search.get().strip()
        if search_term == "" or search_term == "Search...":
            return
        
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Match by numeric id or by name (partial match)
            try:
                # if search_term is numeric, search by id
                int_term = int(search_term)
                cursor.execute("SELECT * FROM rentals WHERE id = ?", (int_term,))
            except ValueError:
                like_term = f"%{search_term}%"
                cursor.execute("SELECT * FROM rentals WHERE name LIKE ?", (like_term,))
            result = cursor.fetchone()

        except Exception as e:
            print(f"Search error: {e}")
            return []
        finally:
            if conn:
                conn.close()
 
        


    def filter_menu(event): # To be checked/revised by Garcia or Quitollo
        # added simple handler to apply a status filter
        def filter_status(status):
            try:
                # call the db helper if available, otherwise no-op
                try:
                    results = get_rentals_by_status(status)
                except TypeError:
                    # fallback if imported function signature differs
                    results = None

            except Exception:
                pass

        menu = tk.Menu(main_frame, tearoff=0)
        menu.add_command(label="Show Active", command=lambda: filter_status("Ongoing"))
        menu.add_command(label="Show Overdue", command=lambda: filter_status("Overdue"))
        menu.add_command(label="Show Completed", command=lambda: filter_status("Completed"))
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


    # FILTER RENTAL BY STATUS FUNCTION
    # To be checked/revised by Garcia or Quitollo
    def get_rentals_by_status():
        try:
            filter_status = filter.get()
        except Exception:
            return None

        if not filter_status:
            return None

        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM rentals WHERE status = ?", (filter_status,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result

        except Exception:
            return None




    container = tk.Frame(main_frame, bg="#eef2f7", highlightthickness=0)
    container.pack(fill="both", expand=True, padx=20)

    for order in orders:
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
            cursor="hand2", command=lambda o=order: show_details(app, o)
        )
        btn.pack(side="left", padx=10)
        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")

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


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_path = os.path.join(BASE_DIR, "assets", "history.png")
    history_icon = ImageTk.PhotoImage(Image.open(history_path).resize((30, 30)))

    history = tk.Button(
        bottom,
        text="Previous Rentals",
        image=history_icon,
        compound="left",
        font=("Arial", 17, "bold"),
        bg="#eef2f7",
        fg="#ffd735",
        cursor="hand2",
        command=lambda:app.set_active_page("history"),
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    history.image = history_icon
    history.pack(side="left", padx=5)


    add_hover(history, "#eef2f7", "#eef2f7", "black", "#e6b800")
    add_hover(add_btn, "#232624", "#ffd735", "#ffd735", "black")


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
        
    # SHOW RENTAL DETAILS FUNCTION
    # To be checked/revised by Garcia or Quitollo
    def get_rentals_details():
        # Fetch rental details from the database
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, rentee, contact, email, region, city, barangay, postal, street, device, rental_month, rental_day, rental_year, return_month, return_day, return_year, total_fee, status FROM rentals WHERE id = ?", (order.get('id'),))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "rentee": row[1],
                "contact": row[2],
                "email": row[3],
                "region": row[4],
                "city": row[5],
                "barangay": row[6],
                "postal": row[7],
                "street": row[8],
                "device": row[9],
                "rental_month": row[10],
                "rental_day": row[11],
                "rental_year": row[12],
                "return_month": row[13],
                "return_day": row[14],
                "return_year": row[15],
                "total_fee": row[16],
                "status": row[17]
            }
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()




    #bottom
    bottom_bar = tk.Frame(
        frame,
        padx=40,
        pady=20,
        bg="#eef2f7"
    )
    bottom_bar.pack(fill="x", side="bottom")

    scolor = status_colors.get(order['status'], "black")

    tk.Label(
        bottom_bar,
        text=f"Rental Status: {order['status']}",
        font=("Arial", 20, "italic", "bold"),
        fg=scolor,
        bg="#eef2f7"
    ).pack(side="left")


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
        complete_btn = tk.Button(
            bottom_bar,
            text="COMPLETE RENTAL",
            font=("Arial", 17, "bold"),
            bg="#ffd735",
            cursor="hand2",
            command=lambda: [mark_rental_as_completed(get_connection(), order['id']), open_receipt(order), app.pages["rentals"].tkraise()]
        )
        complete_btn.pack(side="right", padx=5)
        add_hover(complete_btn, "#232624", "#ffd735", "#ffd735", "black")

    # MARK RENTAL AS COMPLETE FUNCTION
    # To be checked/revised by Garcia or Quitollo
    def mark_rental_as_completed(conn, rental_id):
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE rentals SET status = ? WHERE id = ?", ("Completed", rental_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error marking rental as completed:", e)
            return False
        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass




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
        text="RENTEE INFO", 
        font=("Arial", 20, "bold"), 
        bg="#eef2f7"
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    tk.Label(
        container,
        text=f"Rental ID: {order['id']}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=1, column=0, sticky="w", pady=10)

    tk.Label(
        container,
        text=f"Rentee Name: {order['rentee']}",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=1, column=1, sticky="w", pady=10)

    tk.Label(
        container,
        text="Contact Number: 123456789",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=2, column=0, sticky="w", pady=10)

    tk.Label(
        container,
        text="Email Address: testcase@gmail.com",
        font=("Arial", 12, "bold"),
        bg="#eef2f7"
    ).grid(row=2, column=1, sticky="w", pady=10)

    tk.Frame(
        container,
        height=2,
        bg="black"
    ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)

    #for showing the dummy device info lng
    tk.Label(
        container, 
        text="DEVICE INFORMATION", 
        font=("Arial", 20, "bold"), 
        bg="#eef2f7"
    ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))

    for i, (key, value) in enumerate(device_data.items()):
            row_idx = 5 + (i // 2) + 1
            col_idx = i % 2

            tk.Label(
                container, 
                text=f"{key}: {value}", 
                font=("Arial", 12, "bold"), 
                bg="#eef2f7"
            ).grid(row=row_idx, column=col_idx, sticky="w", padx=5, pady=5)
        
    next_row = 5 + (len(device_data) // 2) + 1

    tk.Frame(
        container, 
        height=2, 
        bg="black"
    ).grid(row=next_row, column=0, columnspan=2, sticky="ew", pady=20)
    
    tk.Label(
        container, 
        text="Rental Date: 06/11/2026", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=next_row + 1, column=0, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Must Return By: 06/12/2026", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=next_row + 1, column=1, sticky="w", pady=10)

    tk.Label(
        container, 
        text="Rental Total: 0.00 PHP", 
        font=("Arial", 14, "bold"), 
        bg="#eef2f7"
    ).grid(row=next_row + 2, column=0, sticky="w", pady=20)

    frame.tkraise()