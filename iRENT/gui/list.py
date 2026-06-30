import tkinter as tk
from tkinter import messagebox
from gui.add_rental import add_rental_page
from PIL import Image, ImageTk
import os

# Import database connection and logic
from db.database import get_connection
from db.view_device_list_logic import (
    _ensure_specs_column,
    get_categories,
    get_brands,
    get_models,
    add_model as db_add_model,
    delete_model as db_delete_model,
    update_model as db_update_model
)

# global func to use anywhere in the code
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

def refresh_device_grid(container, devices, app):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    for i in range(2):
        container.grid_columnconfigure(i, weight=1, uniform="col")

    for i, device in enumerate(devices):
        row, col = i // 2, i % 2

        btn = tk.Button(
            container,
            text=device,
            font=("Arial", 20, "bold"),
            bg="#ffd735",
            fg="black",
            relief="ridge",
            height=3,
            command=lambda d=device: open_brands(app, d)
        )
        btn.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")

        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")


def create_list(main_frame, app):
    # Ensure database columns are up to date on load
    try:
        _ensure_specs_column(get_connection())
    except Exception as e:
        print("DB Check Error:", e)

    for widget in main_frame.winfo_children():
        widget.destroy()
    main_frame.config(bg="#eef2f7")

    app.main_frame = main_frame

    title = tk.Label(main_frame, text="LIST OF DEVICES", font=("Arial", 30, "bold"), fg="black", bg="#eef2f7")
    title.pack(pady=25)

    tk.Frame(main_frame, height=2, bg="black").pack(fill="x", padx=20, pady=5)

    searchfilter = tk.Frame(main_frame, bg="#eef2f7")
    searchfilter.pack(fill="x", padx=20, pady=10)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    swrap = tk.Frame(searchfilter, bg="#eef2f7")
    swrap.pack(side="right", padx=(10,0))

    search_path = os.path.join(BASE_DIR, "assets", "search.png")
    search_icon = ImageTk.PhotoImage(Image.open(search_path).resize((20, 20)))

    icon_label = tk.Label(swrap, image=search_icon, bg="#eef2f7")
    icon_label.image = search_icon
    icon_label.pack(side="right")

    search = tk.Entry(swrap, font=("Arial", 12), width=15)
    search.insert(0, "Search...")
    search.config(fg="gray")
    search.pack(side="right", padx=5)

    # FIXED: Pack Bottom Bar FIRST so the canvas doesn't overlap it
    bottom_bar = tk.Frame(main_frame, bg="#eef2f7")
    bottom_bar.pack(side="bottom", fill="x", padx=20, pady=20)

    add_btn = tk.Button(
        bottom_bar,
        text="+ Add Device Category",
        font=("Arial", 17, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        relief="raised",
        command=lambda: add_device_type(app)
    )
    add_btn.pack(side="right")
    add_hover(add_btn, "#142C14", "#4CAF50", "white", "white")

    canvas = tk.Canvas(main_frame, bg="#eef2f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

    container = tk.Frame(canvas, bg="#eef2f7")
    app.device_container = container

    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def perform_search(event=None):
        query = search.get().strip().lower()
        categories = get_categories()

        if query == "search..." or not query:
            refresh_device_grid(container, categories, app)
        else:
            matches = [c for c in categories if query in c.lower()]
            refresh_device_grid(container, matches, app)

    search.bind("<KeyRelease>", perform_search)
    search.bind("<FocusIn>", lambda e: (search.delete(0, "end"), search.config(fg="black")) if search.get()=="Search..." else None)
    search.bind("<FocusOut>", lambda e: (search.insert(0, "Search..."), search.config(fg="gray")) if not search.get() else None)

    refresh_device_grid(container, get_categories(), app)

def add_device_type(app):
    frame = app.pages["add_device_type"]

    for w in frame.winfo_children():
        w.destroy()

    frame.grid_rowconfigure(0, weight=0)     #title, fixed
    frame.grid_rowconfigure(1, weight=5)     #content, expands
    frame.grid_columnconfigure(0, weight=1)  #expands horizontally, shares extra width

    title = tk.Label(
        frame,
        text="ADD DEVICE CATEGORY",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.grid(row=0, column=0, pady=20)

    container = tk.LabelFrame(frame, text="CATEGORY", font=("Arial", 24, "bold"), bd=2, relief="solid")
    container.grid(row=1, column=0, sticky="n", pady=10)

    device_label = tk.Label(container, text="Category Name:", font=("Arial", 12, "bold"))
    device_label.grid(row=0, column=0, padx=10, pady=10)

    device_entry = tk.Entry(container, font=("Arial", 12), width=35, bd=1, relief="solid")
    device_entry.grid(row=0, column=1, padx=10, pady=10)

    message = tk.Label(container, text="", font=("Arial", 11), fg="red")
    message.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w", padx=20)

    def save_device_type():
        """Save all changes and update DATA"""
        # Get values from entries
        new_device = device_entry.get().strip().upper()

        if not new_device:
            message.config(text="Please fill in all text fields!")
            return

       # SAVES TO DB INSTEAD OF LOCAL LIST
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT 1 FROM DeviceType WHERE TypeName = ?", (new_device,))
            if cursor.fetchone():
                message.config(text="Category already exists!", fg="red")
                return

            cursor.execute("INSERT INTO DeviceType (TypeName) VALUES (?)", (new_device,))
            conn.commit()

            message.config(text=f"✅ Added: {new_device.upper()}", fg="green")
            frame.after(1000, lambda: app.pages["devices"].tkraise())
            frame.after(1000, lambda: create_list(app.main_frame, app))

        except Exception as e:
            message.config(text=f"❌ DB Error: {e}", fg="red")
        finally:
            conn.close()

    def cancel_changes():
        """Go back without saving"""
        app.pages["devices"].tkraise()

    btn_frame = tk.Frame(container)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    save_btn = tk.Button(
        btn_frame,
        text="Save Category",
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        padx=15,
        pady=5,
        bd=1,
        command=save_device_type
    )
    save_btn.pack(side="left", padx=10)
    add_hover(save_btn, "#45a049", "#4CAF50", "white", "white")

    cancel_btn = tk.Button(
        btn_frame,
        text="Cancel",
        font=("Arial", 10, "bold"),
        bg="#f44336",
        fg="white",
        cursor="hand2",
        padx=15,
        pady=5,
        bd=1,
        command=cancel_changes
    )
    cancel_btn.pack(side="left", padx=10)
    add_hover(cancel_btn, "#d32f2f", "#f44336", "white", "white")

    app.pages["add_device_type"].tkraise()

def open_brands(app, device):
    show_device_brands(app, device)
    app.pages["brand_devices"].tkraise()

def show_device_brands(app, device):
    frame = app.pages["brand_devices"]

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(
        frame,
        text=f"{device.upper()} BRANDS",
        font=("Arial", 30, "bold"),
        fg="black",
        bg ="#eef2f7"
    ).pack(pady=25)

    tk.Frame(
        frame,
        height=2,
        bg="black"
    ).pack(fill="x", padx=20, pady=5)

    searchfilter = tk.Frame(frame, bg="#eef2f7")
    searchfilter.pack(fill="x", padx=20, pady=10)

    swrap = tk.Frame(searchfilter, bg="#eef2f7")
    swrap.pack(side="right", padx=(10,0))

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    search_path = os.path.join(BASE_DIR, "assets", "search.png")
    search_icon = ImageTk.PhotoImage(Image.open(search_path).resize((20, 20)))

    icon_label = tk.Label(swrap, image=search_icon, bg="#eef2f7")
    icon_label.image = search_icon
    icon_label.pack(side="right")

    search = tk.Entry(swrap, font=("Arial", 12), width=15)
    search.insert(0, "Search...")
    search.config(fg="gray")
    search.pack(side="right", padx=5)

    # FIXED: PACK BOTTOM BAR FIRST TO PREVENT OVERLAP ON CANVAS CLICKS
    bottom = tk.Frame(frame, bg="#eef2f7")
    bottom.pack(side="bottom", fill="x", padx=20, pady=20)

    back_btn = tk.Button(
        bottom,
        text="Back",
        font=("Arial", 17, "bold"),
        bg="gray",
        fg="black",
        relief="raised",
        height=1,
        command=lambda: app.pages["devices"].tkraise())
    back_btn.pack(side="right")
    add_hover(back_btn, "#232624", "gray", "white", "black")

    add_btn = tk.Button(
        bottom,
        text="+ Add Device Brand",
        font=("Arial", 17, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        relief="raised",
        height=1, command=lambda: add_device_brand(app, device))
    add_btn.pack(side="left")
    add_hover(add_btn, "#142C14", "#4CAF50", "white", "white")

    content = tk.Frame(frame, bg="#eef2f7")
    content.pack(fill="both", expand=True)

    canvas = tk.Canvas(content, bg="#eef2f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    brands_container = tk.Frame(canvas, bg="#eef2f7")
    canvas_window = canvas.create_window((0, 0), window=brands_container, anchor="nw")

    canvas.bind("<Configure>", lambda e:canvas.itemconfig(canvas_window, width=e.width))
    brands_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    num_columns= 3

    def refresh_brand_grid(brand_list):
        for widget in brands_container.winfo_children():
            widget.destroy()

        for i in range(num_columns):
            brands_container.grid_columnconfigure(i, weight=1, uniform="brand_col")

        for i, brand in enumerate(brand_list):
            row = i // num_columns
            col = i % num_columns

            # Removed Fixed dimensions to avoid text-clipping overlaps inside frame
            brand_frame = tk.Frame(
                brands_container,
                bg="white",
                highlightthickness=1,
                borderwidth=3,
                relief="solid"
            )
            brand_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            tk.Label(
                brand_frame,
                text=brand,
                bg="white",
                font=("Arial", 20, "bold")
            ).pack(pady=(30, 20), anchor="center")

            btn = tk.Button(
                brand_frame,
                text="See More",
                bg="#ffd735",
                font=("Arial", 12, "bold"),
                command=lambda d=device, b=brand: show_brand_details(app, d, b)
            )
            btn.pack(pady=(0, 20)) # FIXED by Yuri: Changed from 40 to 20
            add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")

    def perform_search(event=None):
        query = search.get().lower().strip()
        brands = get_brands(device)

        if query == "Search..." or not query:
            refresh_brand_grid(brands)
        else:
            matches = [b for b in brands if query in b.lower()]
            refresh_brand_grid(matches)

    search.bind("<KeyRelease>", perform_search)
    search.bind("<FocusIn>", lambda e: (search.delete(0, "end"), search.config(fg="black")) if search.get()=="Search..." else None)
    search.bind("<FocusOut>", lambda e: (search.insert(0, "Search..."), search.config(fg="gray")) if not search.get() else None)

    refresh_brand_grid(get_brands(device))

    app.pages["brand_devices"].tkraise()

def add_device_brand(app, device):
    frame = app.pages["add_device_brand"]

    for w in frame.winfo_children():
        w.destroy()

    frame.grid_rowconfigure(0, weight=0)     #title, fixed
    frame.grid_rowconfigure(1, weight=5)     #content, expands
    frame.grid_columnconfigure(0, weight=1)  #expands horizontally, shares extra width

    title = tk.Label(
        frame,
        text="ADD DEVICE BRAND",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.grid(row=0, column=0, pady=20)

    # Main content container
    container = tk.LabelFrame(frame, text="DEVICE BRAND", font=("Arial", 20, "bold"), bd=2, relief="solid")
    container.grid(row=1, column=0, sticky="n", pady=10)

    device_label = tk.Label(container, text="Brand Name:", font=("Arial", 12, "bold"))
    device_label.grid(row=0, column=0, padx=10, pady=10)

    devicebrand_entry = tk.Entry(container, font=("Arial", 12), width=35, bd=1, relief="solid")
    devicebrand_entry.grid(row=0, column=1, padx=10, pady=10)

    message = tk.Label(container, text="", font=("Arial", 11), fg="red")
    message.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w", padx=20)

    def save_device_brand():
        """Save and update all changes"""
        # Get values from entries
        new_brand = devicebrand_entry.get().strip().upper()     #NEW

        if not new_brand:
            message.config(text="Please enter a brand name!", fg="red")
            return

        try:
            import os
            dummy_id = f"DUMMY-{os.urandom(2).hex()[:6].upper()}"

            success, msg = db_add_model(
                category_name=device,
                brand_name=new_brand,
                model_name="[NO MODELS YET]",
                product_id=dummy_id,
                price=0,
                stock_count=0,
                specs_list=["[PLACEHOLDER]"],
                serial_num=dummy_id
            )

            if success:
                message.config(text=f"✅ Added: {new_brand} for {device.upper()}", fg="green")
                # Go back to devices page after delay
                frame.after(1000, lambda: app.pages["brand_devices"].tkraise())
                frame.after(1000, lambda: show_device_brands(app, device))
            else:
                message.config(text=f"❌ DB Error: {msg}", fg="red")

        except Exception as e:
            # Displays the hidden backend crash on the UI
            message.config(text=f"❌ Error: {e}", fg="red")

    def cancel_changes():
        """Go back without saving"""
        app.pages["brand_devices"].tkraise()

    btn_frame = tk.Frame(container)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    save_btn = tk.Button(
        btn_frame,
        text="Save Brand",
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        padx=15,
        pady=5,
        bd=1,
        command=save_device_brand
    )
    save_btn.pack(side="left", padx=10)
    add_hover(save_btn, "#45a049", "#4CAF50", "white", "white")

    cancel_btn = tk.Button(
        btn_frame,
        text="Cancel",
        font=("Arial", 10, "bold"),
        bg="#f44336",
        fg="white",
        cursor="hand2",
        padx=15,
        pady=5,
        bd=1,
        command=cancel_changes
    )
    cancel_btn.pack(side="left", padx=10)
    add_hover(cancel_btn, "#d32f2f", "#f44336", "white", "white")

    app.pages["add_device_brand"].tkraise()

def delete_model(app, device, brand, model_name):
    """Delete a model from the Database"""
    # confirm deletion
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{model_name}' from {brand}?\n\nThis action cannot be undone!",
        icon="warning"
    )

    if confirm:
        # Call backend delete logic
        success, msg = db_delete_model(device, brand, model_name)

        if success:
            messagebox.showinfo("Success", msg)
            show_brand_details(app, device, brand)
        else:
            messagebox.showerror("Error", msg)


def open_edit_details(app, device, brand, model_name, current_details):
    frame = app.pages["edit_details"]

    # Clear existing widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Configure frame grid
    frame.grid_rowconfigure(0, weight=0)  # title row
    frame.grid_rowconfigure(1, weight=0)  # subtitle row
    frame.grid_rowconfigure(2, weight=0)  # separator row
    frame.grid_rowconfigure(3, weight=1)  # form row (expands)
    frame.grid_rowconfigure(4, weight=0)  # buttons row
    frame.grid_columnconfigure(0, weight=1)

    # title
    title = tk.Label(
        frame,
        text=f"{device} - {brand}",
        font=("Arial", 24, "bold"),
        fg="black",
        bg="#eef2f7"
    )
    title.grid(row=0, column=0, pady=(20, 5), sticky="ew")

    # subtitle (model name)
    subtitle = tk.Label(
        frame,
        text=model_name,
        font=("Arial", 18),
        fg="#555",
        bg="#eef2f7"
    )
    subtitle.grid(row=1, column=0, pady=(0, 20), sticky="ew")

    # separator
    separator = tk.Frame(frame, height=2, bg="#ccc")
    separator.grid(row=2, column=0, sticky="ew", padx=40, pady=(0, 20))

    # form container
    form_container = tk.Frame(frame, bg="#eef2f7")
    form_container.grid(row=3, column=0, sticky="nsew", padx=40)
    form_container.grid_columnconfigure(0, weight=1)

    # dictionary to store entry widgets
    entries = {}
    safe_id = current_details.get('id', current_details.get('product_id', ''))
    safe_serial = current_details.get('serial_num', current_details.get('serial_number', 'N/A'))
    safe_specs = current_details.get('specs', current_details.get('specs_list', []))
    safe_price = current_details.get('price', 0)
    safe_stock = current_details.get('available', current_details.get('stock_count', 0))

    # helper function to create labeled entry
    def create_entry(parent, label_text, default_value, row):
        """Create a labeled entry field"""
        entry_frame = tk.Frame(parent, bg="#eef2f7")
        entry_frame.grid(row=row, column=0, sticky="ew", pady=8)
        entry_frame.grid_columnconfigure(1, weight=1)

        # Label
        label = tk.Label(
            entry_frame,
            text=label_text,
            font=("Arial", 12, "bold"),
            bg="#eef2f7",
            width=18,
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w")

        # Entry
        entry = tk.Entry(
            entry_frame,
            font=("Arial", 12),
            bg="white",
            relief="solid",
            bd=1
        )
        entry.insert(0, str(default_value))
        entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        return entry

    # create form rows
    row = 0

    # model name (display only - not editable)
    name_frame = tk.Frame(form_container, bg="#eef2f7")
    name_frame.grid(row=row, column=0, sticky="ew", pady=8)
    name_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        name_frame,
        text="Model Name:",
        font=("Arial", 12, "bold"),
        bg="#eef2f7",
        width=18,
        anchor="w"
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        name_frame,
        text=model_name,
        font=("Arial", 12),
        bg="#eef2f7",
        fg="#555"
    ).grid(row=0, column=1, sticky="w", padx=(10, 0))
    row += 1

    # ID (editable)
    entries['id'] = create_entry(form_container, "ID:", safe_id, row)
    row += 1

    # Serial Number (editable)
    entries['serial_number'] = create_entry(
        form_container,
        "Serial Number:",
        safe_serial,
        row
    )
    row += 1


    # Specs (editable - text area)
    specs_frame = tk.Frame(form_container, bg="#eef2f7")
    specs_frame.grid(row=row, column=0, sticky="ew", pady=8)
    specs_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        specs_frame,
        text="Specs:",
        font=("Arial", 12, "bold"),
        bg="#eef2f7",
        width=18,
        anchor="nw"
    ).grid(row=0, column=0, sticky="nw", padx=(0, 10))

    specs_text = "\n".join(safe_specs)
    specs_entry = tk.Text(
        specs_frame,
        font=("Arial", 11),
        bg="white",
        relief="solid",
        bd=1,
        height=5,
        width=30
    )
    specs_entry.insert("1.0", specs_text)
    specs_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
    entries['specs'] = specs_entry
    row += 1

    # Price (editable)
    entries['price'] = create_entry(form_container, "Price (₱):", safe_price, row)
    row += 1

    # Available (editable)
    entries['available'] = create_entry(form_container, "Available:", safe_stock, row)
    row += 1

    # buttons -----------------
    button_frame = tk.Frame(frame, bg="#eef2f7")
    button_frame.grid(row=4, column=0, sticky="ew", pady=30, padx=40)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    def save_changes():
        try:
            # Get values from entries
            new_id = entries['id'].get().strip()
            new_serial = entries['serial_number'].get().strip()
            new_specs_text = entries['specs'].get("1.0", tk.END).strip()
            new_specs = [spec.strip() for spec in new_specs_text.split('\n') if spec.strip()]
            new_price = int(entries['price'].get().strip())

            # Validate
            if not new_id or not new_serial or not new_specs:
                messagebox.showerror("Error", "Fields cannot be empty!")
                return
            if new_price < 0:
                messagebox.showerror("Error", "Price cannot be negative!")
                return

            # Call backend update logic
            success, msg = db_update_model(
                category_name=device,
                brand_name=brand,
                model_name=model_name,
                new_model_name=model_name, # GUI doesn't allow changing model name currently
                new_id=new_id,
                new_serial=new_serial,
                new_specs=new_specs,
                new_price=new_price
            )

            if success:
                messagebox.showinfo("Success", msg)
                app.pages["brand_details"].tkraise()
                show_brand_details(app, device, brand)
            else:
                messagebox.showerror("Error", msg)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Price!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def cancel_changes():
        """Go back without saving"""
        app.pages["brand_details"].tkraise()

    # Save button (LEFT)
    save_btn = tk.Button(
        button_frame,
        text="💾 Save Changes",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        padx=30,
        pady=10,
        command=save_changes
    )
    save_btn.grid(row=0, column=0, sticky="e", padx=10)
    add_hover(save_btn, "#45a049", "#4CAF50", "white", "white")

    # Cancel button (RIGHT)
    cancel_btn = tk.Button(
        button_frame,
        text="❌ Cancel",
        font=("Arial", 12, "bold"),
        bg="#f44336",
        fg="white",
        cursor="hand2",
        padx=30,
        pady=10,
        command=cancel_changes
    )
    cancel_btn.grid(row=0, column=1, sticky="w", padx=10)
    add_hover(cancel_btn, "#d32f2f", "#f44336", "white", "white")

    # Raise the edit page
    app.pages["edit_details"].tkraise()

def refresh_models(container, canvas,models_data, app, device, brand):
    for widget in container.winfo_children():
        widget.destroy()

    data = [m for m in models_data if m.get('model_name', m.get('model', '')) != "[NO MODELS YET]"]

    if not data:
        tk.Label(container, text="No models found.", font=("Arial", 14)).grid(row=0, column=0, columnspan=3)
        return

    max_specs = max([len(m.get('specs', m.get('specs_list', []))) for m in data], default=0)

    for i, details in enumerate(models_data):
        row = i // 3
        col = i % 3
        model = details.get('model_name', details.get('model', 'Unknown'))
        d_id = details.get('id', details.get('product_id', 'N/A'))
        serial = details.get('serial_num', details.get('serial_number', 'N/A'))
        specs = details.get('specs', details.get('specs_list', []))
        price = details.get('price', 0)
        stock = details.get('available', details.get('stock_count', 0))
        card = tk.Frame(
            container,
            bg="white",
            relief="solid",
            highlightthickness=1,
            highlightbackground="black"
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # config card grid layout
        card.grid_rowconfigure(0, weight=0)  # model: fixed
        card.grid_rowconfigure(1, weight=0)  # id: fixed
        card.grid_rowconfigure(2, weight=0)  # serial number
        card.grid_rowconfigure(3, weight=0)  # specs: fixed
        card.grid_rowconfigure(4, weight=1)  # specs list (stretches)
        card.grid_rowconfigure(5, weight=0)  # price: fixed
        card.grid_rowconfigure(6, weight=0)  # stock: fixed
        card.grid_rowconfigure(7, weight=0)  # buttons: fixed
        card.grid_columnconfigure(0, weight=1)  # column stretches

        # model name
        tk.Label(
            card,
            text=model,
            font=("Arial", 18, "bold"),
            bg="white"
        ).grid(row=0, column=0, pady=(15, 5), sticky="ew")

        # ID
        tk.Label(
            card,
            text=f"ID: {d_id}",
            bg="white",
            font=("Arial", 10)
        ).grid(row=1, column=0, pady=(0, 10), sticky="ew")

        # serial number
        tk.Label(
            card,
            text=f"Serial: {serial}",
            bg="white",
            font=("Arial", 10)
        ).grid(row=2, column=0, pady=(0, 10), sticky="ew")


        tk.Label(
            card,
            text="Specs:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", padx=10, pady=(5, 0))

        # specs list frame
        specs_frame = tk.Frame(card, bg="white")
        specs_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        specs_frame.grid_columnconfigure(0, weight=1)

        # list specs
        for j, spec in enumerate(specs):
            tk.Label(
                specs_frame,
                text=f"• {spec}",
                bg="white",
                font=("Arial", 9),
                wraplength=200,
                justify="left"
            ).grid(row=j, column=0, sticky="w", pady=2) # FIXED by Yuri: Changed row=i to row=j

        # add empty rows to match tallest card (keeps all cards same height)
        for empty_row in range(len(specs), max_specs):
            tk.Label(
                specs_frame,
                text="",
                bg="white",
                font=("Arial", 9)
            ).grid(row=empty_row, column=0, pady=2)

        tk.Label(
            card,
            text=f"Price: ₱{price:,}",
            font=("Arial", 15, "bold"),
            fg="green",
            bg="white"
        ).grid(row=5, column=0, pady=(0, 5), sticky="ew")

        stock_color = "red" if stock == 0 else "gray"
        tk.Label(
            card,
            text=f"Stock: {stock}",
            fg=stock_color,
            bg="white",
            font=("Arial", 10, "bold", "italic")
        ).grid(row=6, column=0, pady=(0, 5), sticky="ew")

        button_row = tk.Frame(card, bg="white")
        button_row.grid(row=8, column=0, pady=(0, 15), sticky="ew")
        button_row.grid_columnconfigure(0, weight=1)  # Left side
        button_row.grid_columnconfigure(1, weight=1)  # Right side

        rent_btn = tk.Button(
            button_row,
            text="Rent Me",
            bg="#ffd735",
            fg = "black",
            font=("Arial", 15, "bold"),
            cursor="hand2",
            command=lambda det=details: [
                add_rental_page(app.pages["add_rental"], app, prefill_device=det),
                app.pages["add_rental"].tkraise()
            ]
        )
        rent_btn.grid(row=0, column=0, padx=10, sticky="w")
        add_hover(rent_btn, "#232624", "#ffd735", "#ffd735", "black")

        # disable if out of stock
        if stock == 0:
            rent_btn.config(state="disabled", bg="gray", text="OUT OF STOCK")

        # menu button (⋯) - RIGHT SIDE
        menu_btn = tk.Button(
            button_row,
            text="☰",
            font=("Arial", 15),
            bg="#ffd735",
            activebackground="#ffd735",
            activeforeground="black",
            fg="black",
            cursor="hand2",
            width=3
        )
        menu_btn.grid(row=0, column=1, padx=10, sticky="e")
        add_hover(menu_btn, "#232624", "#ffd735", "#ffd735", "black")

        # create dropdown menu for this specific card
        menu = tk.Menu(menu_btn, tearoff=0)
        menu.add_command(
            label="Edit Details",
            command=lambda d=device, b=brand, m=model, det=details: open_edit_details(app, d, b, m, det) #FIXED by Yuri: Fixed edit details not working
        )
        menu.add_separator()
        menu.add_command(
            label="Delete Model",
            command=lambda d=device, b=brand, m=model: delete_model(app, d, b, m)
        )

        # Bind the menu to appear when clicking the button
        def show_menu(event, menu=menu, btn=menu_btn):
            try:
                menu.post(btn.winfo_rootx(), btn.winfo_rooty() + btn.winfo_height())
            except:
                pass

        menu_btn.bind("<Button-1>", show_menu)

    container.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))




def show_brand_details(app, device, brand):
    frame = app.pages["brand_details"]

    for widget in frame.winfo_children():
        widget.destroy()

    frame.config(bg="#eef2f7")

    # title
    title = tk.Label(
        frame,
        text=f"{brand} - {device} MODELS",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.pack(pady=20)

    tk.Frame(
        frame,
        height=2,
        bg="black"
    ).pack(fill="x", padx=20, pady=5)

    searchfilter = tk.Frame(
        frame,
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

    search = tk.Entry(searchfilter, font=("Arial", 12), width=15, fg="gray")
    search.insert(0, "Search...")

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
    search.pack(side="right")

    filter_menu = tk.Menu(searchfilter, tearoff=0)

    def mfilter(category):
        all_models = get_models(device, brand)

        if category == "All":
            data = all_models
        elif category == "Available":
            data = [m for m in all_models if m.get('available', m.get('stock_count', 0)) > 0]
        elif category == "Out of Stock":
            data = [m for m in all_models if m.get('available', m.get('stock_count', 0)) == 0]

        refresh_models(container, canvas, data, app, device, brand)

    filter_menu.add_command(label="Show All", command=lambda: mfilter("All"))
    filter_menu.add_command(label="Show Available", command=lambda: mfilter("Available"))
    filter_menu.add_command(label="Show Out of Stock", command=lambda: mfilter("Out of Stock"))

    def mfilter_menu(event):
        filter_menu.post(event.x_root, event.y_root)

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
    filter_label.bind("<Button-1>", mfilter_menu)

    add_hover(filter_label, "#eef2f7", "#eef2f7", "black", "#e6b800")

    scroll_wrapper = tk.Frame(frame, bg="#eef2f7")
    scroll_wrapper.pack(fill="both", expand=True, padx=20)

    canvas = tk.Canvas(scroll_wrapper, bg="#eef2f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    container = tk.Frame(canvas, bg="#eef2f7")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def msearch(event=None):
        term = search.get().lower()
        all_models = get_models(device,brand)

        if term == "search..." or term == "":
            data = get_models(device, brand)
        else:
            data = []
            for m in all_models:
                name_match = term in m.get('model_name', '').lower()
                specs_match = any(term in s.lower() for s in m.get('specs', []))

                if name_match or specs_match:
                    data.append(m)

        refresh_models(container, canvas, data, app, device, brand)

    search.bind("<KeyRelease>", msearch)

    # Initial load
    initial_data = get_models(device, brand)
    refresh_models(container, canvas, initial_data, app, device, brand)

    # 3 columns for grid layout
    for i in range(3):
        container.grid_columnconfigure(i, weight=1, uniform="col")


    # frame for buttons at the bottom (add, back)
    bottom = tk.Frame(frame)
    bottom.pack(fill="x", padx=20, pady=(0,20))

    # add device - left (sticky = "w")
    add_btn = tk.Button(
        bottom,
        text="+ Add New Model",
        font=("Arial", 17, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        relief="raised",
        command=lambda d=device, b=brand: add_device(app, device, brand)
    )
    add_btn.pack(side="left", padx=10)
    add_hover(add_btn, "#45a049", "#4CAF50", "white", "white")

    back_btn = tk.Button(
        bottom,
        text="Back",
        font=("Arial", 17, "bold"),
        bg="gray",
        fg="black",
        relief="raised",
        height=1,
        command=lambda: app.pages["brand_devices"].tkraise())
    back_btn.pack(side="right")
    add_hover(back_btn, "#232624", "gray", "white", "black")

    app.pages["brand_details"].tkraise()


def add_device(app, device, brand):
    frame = app.pages["add_device"]

    for widget in frame.winfo_children():
        widget.destroy()

    # config grid for main frame (the frame)
    frame.grid_rowconfigure(0, weight=0)  # title
    frame.grid_rowconfigure(1, weight=1)  # form
    frame.grid_columnconfigure(0, weight=1)

    # title label
    tk.Label(
        frame,
        text=f"Add New {brand} Model",
        font=("Arial", 24, "bold")
    ).grid(row=0, column=0, pady=20)

    # shows what device - brand you are currently editing with
    tk.Label(
        frame,
        text=f"{device} - {brand}",
        font=("Arial", 14),
        fg="gray"
    ).grid(row=1, column=0)

    # used for everything below inside form
    form = tk.Frame(frame, bg="white", borderwidth=2, relief="solid", padx=30, pady=30)
    form.grid(row=2, column=0, sticky="nsew", padx=50, pady=20)

    # make 2 columns in the form (labels on left, entries on right)
    form.grid_columnconfigure(0, weight=0)  # labels (id, price, stock, etc) FIXED
    form.grid_columnconfigure(1, weight=1)  # entries (enter id, enter price, etc) EXPANDS

    # row counter
    row = 0

    # row 0: model name
    tk.Label(form, text="Model Name:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    model_entry = tk.Entry(form, font=("Arial", 12), width=35,  bd=1, relief="solid")
    model_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # row 1: id
    tk.Label(form, text="ID:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    id_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    id_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # row 2: serial number (NEW)
    tk.Label(form, text="Serial Number:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    serial_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    serial_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    tk.Label(form, text="Price (₱):", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    price_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    price_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    tk.Label(form, text="Stock:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    stock_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    stock_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    tk.Label(form, text="Specs (separate with commas):", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    specs_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    specs_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # suggestion label, below specs entry box
    tk.Label(
        form,
        text="Example: 33MP, 4K Video, IBIS Stabilization",
        font=("Arial", 8),
        fg="gray",
        bg="white"
    ).grid(row=row, column=1, sticky="w", pady=(0, 10))
    row += 1

    # starts empty and later used as message.config to display error messages differently
    message = tk.Label(frame, text="", font=("Arial", 11))
    message.grid(row=3, column=0, pady=10)

    # add, cancel
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=4, column=0, pady=20)

    def save():
        # gets what user typed
        name = model_entry.get().strip().upper()
        pid = id_entry.get().strip().upper()
        serial = serial_entry.get().strip()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()
        specs_text = specs_entry.get().strip()

        if not name or not pid or not serial or not specs_text:
            message.config(text="Please fill in all text fields!", fg="red")
            return
        if not price or not price.isdigit():
            message.config(text="Enter valid price!", fg="red")
            return
        if not stock or not stock.isdigit():
            message.config(text="Enter valid stock!", fg="red")
            return

        #converts specs into list
        specs_list = [s.strip() for s in specs_text.split(",")]

        # Send data to Database
        success, msg = db_add_model(
            category_name=device,
            brand_name=brand,
            model_name=name,
            product_id=pid,
            price=int(price),
            stock_count=int(stock),
            specs_list=specs_list,
            serial_num=serial
        )

        #shows success text
        if success:
            message.config(text=f"✅ {msg}", fg="green")

            #automatically goes back to brand_details after saving. shows the added device during run
            frame.after(1000, lambda: app.pages["brand_details"].tkraise())
            frame.after(1000, lambda: show_brand_details(app, device, brand))
        else:
            message.config(text=f"❌ {msg}", fg="red")

    add_btn = tk.Button(
        btn_frame,
        text="Add Model",
        font=("Arial", 14, "bold"),
        bg="#ffd735",
        cursor="hand2",
        command=save
    )
    add_btn.pack(side="left", padx=10)
    add_hover(add_btn, "#232624", "#ffd735", "#ffd735", "black")

    cancel_btn = tk.Button(
        btn_frame,
        text="Cancel",
        font=("Arial", 14, "bold"),
        bg="#cccccc",
        cursor="hand2",
        command=lambda: app.pages["brand_details"].tkraise()
    )
    cancel_btn.pack(side="left", padx=10)
    add_hover(cancel_btn, "#232624", "#ffd735", "#ffd735", "black")

    # Show the page
    app.pages["add_device"].tkraise()