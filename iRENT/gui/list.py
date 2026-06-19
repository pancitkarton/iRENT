import tkinter as tk
from tkinter import messagebox
from gui.add_rental import add_rental_page

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


def create_list(main_frame, app):
    # Ensure database columns are up to date on load
    try:
        _ensure_specs_column(get_connection())
    except Exception as e:
        print("DB Check Error:", e)

    for widget in main_frame.winfo_children():
        widget.destroy()

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=10)
    main_frame.grid_columnconfigure(0, weight=1)

    title = tk.Label(
        main_frame,
        text="LIST OF DEVICES",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.grid(row=0, column=0, pady=20)

    # container for all device cards
    container = tk.Frame(main_frame)
    container.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

    # config container grid
    container.grid_rowconfigure(0, weight=1)
    for i in range(2):
        container.grid_columnconfigure(i, weight=1, uniform="col")

    # Fetch categories from database
    devices = get_categories()

    rows = (len(devices) + 1) // 2

    for i in range(rows):
        container.grid_rowconfigure(i, weight=1)

    for i, device in enumerate(devices):
        row = i // 2
        col = i % 2

        btn = tk.Button(
            container,
            text=device,
            font=("Arial", 20, "bold"),
            bg="#ffd735",
            fg="black",
            relief="ridge",
            command=lambda d=device: open_brands(app, d)
        )
        btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")


def open_brands(app, device):
    show_device_brands(app, device)
    app.pages["brand_devices"].tkraise()


def show_device_brands(app, device):
    frame = app.pages["brand_devices"]

    for w in frame.winfo_children():
        w.destroy()

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    container = tk.Frame(frame, bg="#eef2f7")
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    container.grid_columnconfigure(0, weight=1)

    # Fetch brands from database
    brands = get_brands(device)
    num_brands = len(brands)

    # set number of columns
    num_columns = 3

    # calcu number of rows needed
    num_rows = (num_brands + num_columns - 1) // num_columns if num_brands > 0 else 1

    # title - centered (sticky = "ew" - stretches it left n right)
    title_frame = tk.Frame(container, bg="#eef2f7")
    title_frame.grid(row=0, column=0, sticky="ew", pady=20)
    title_frame.grid_columnconfigure(0, weight=1)

    tk.Label(
        title_frame,
        text=f"{device} BRANDS",
        font=("Arial", 24, "bold"),
        bg="#eef2f7"
    ).grid(row=0, column=0)

    # frame for the brand grid (rows and columns)
    brands_container = tk.Frame(container, bg="#eef2f7")
    brands_container.grid(row=1, column=0, sticky="nsew", pady=20)

    # configure grid columns for brands_container (equal width)
    for col in range(num_columns):
        brands_container.grid_columnconfigure(col, weight=1, uniform="brand_col")

    # config rows for brands_container (equal height)
    for row in range(num_rows):
        brands_container.grid_rowconfigure(row, weight=1)

    if not brands:
        tk.Label(brands_container, text="No brands found for this category.", bg="#eef2f7", font=("Arial", 14)).grid(row=0, column=0, columnspan=3)

    # create brand cards in grid layout
    for i, brand in enumerate(brands):
        row = i // num_columns
        col = i % num_columns

        # create card frame
        brand_frame = tk.Frame(
            brands_container,
            bg="white",
            highlightthickness=1,
            borderwidth=5,
            relief="solid"
        )
        brand_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        brand_frame.grid_rowconfigure(0, weight=1)  # Top spacer
        brand_frame.grid_rowconfigure(2, weight=1)  # Bottom spacer
        brand_frame.grid_columnconfigure(0, weight=1)

        # content frame to center content
        content_frame = tk.Frame(brand_frame, bg="white")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)

        # brand name
        tk.Label(
            content_frame,
            text=brand,
            bg="white",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=(30, 100))

        # button
        btn = tk.Button(
            content_frame,
            text="See More",
            bg="#ffd735",
            font=("Arial", 12, "bold"),
            command=lambda d=device, b=brand: show_brand_details(app, d, b)
        )
        btn.grid(row=1, column=0, pady=(0, 40))
        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")  # Use global

    # back
    back_btn_frame = tk.Frame(container, bg="#eef2f7")
    back_btn_frame.grid(row=2, column=0, sticky="e", pady=20)  # Changed from num_brands+1 to 2

    back_btn = tk.Button(
        back_btn_frame,
        text="←",
        font=("Arial", 16, "bold"),
        bg="#ffd735", fg="black", relief="flat",
        command=lambda: app.pages["devices"].tkraise()
    )
    back_btn.pack(pady=100)
    add_hover(back_btn, "#232624", "#ffd735", "#ffd735", "black")
    app.pages["brand_devices"].tkraise()


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
    """Open the edit details page for a specific model"""

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
    entries['id'] = create_entry(form_container, "ID:", current_details['id'], row)
    row += 1

    # Serial Number (editable)
    entries['serial_number'] = create_entry(
        form_container,
        "Serial Number:",
        current_details.get('serial_num', 'N/A'),
        row
    )
    row += 1

    # Functionality (editable - dropdown)
    func_frame = tk.Frame(form_container, bg="#eef2f7")
    func_frame.grid(row=row, column=0, sticky="ew", pady=8)
    func_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        func_frame,
        text="Functionality:",
        font=("Arial", 12, "bold"),
        bg="#eef2f7",
        width=18,
        anchor="w"
    ).grid(row=0, column=0, sticky="w")

    from tkinter import ttk
    func_var = tk.StringVar(value=current_details['functionality'])
    func_combo = ttk.Combobox(
        func_frame,
        textvariable=func_var,
        values=["Excellent", "Good", "Fair"],
        font=("Arial", 12),
        state="readonly"
    )
    func_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0))
    entries['functionality'] = func_var
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

    specs_text = "\n".join(current_details['specs'])
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
    entries['price'] = create_entry(form_container, "Price (₱):", current_details['price'], row)
    row += 1

    # Available (editable)
    entries['available'] = create_entry(form_container, "Available:", current_details['available'], row)
    row += 1

    # buttons -----------------
    button_frame = tk.Frame(frame, bg="#eef2f7")
    button_frame.grid(row=4, column=0, sticky="ew", pady=30, padx=40)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    def save_changes():
        """Save all changes and update DATA"""
        try:
            # Get values from entries
            new_id = entries['id'].get().strip()
            new_serial = entries['serial_number'].get().strip()
            new_functionality = entries['functionality'].get()
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
                new_functionality=new_functionality,
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


def show_brand_details(app, device, brand):
    frame = app.pages["brand_details"]

    for widget in frame.winfo_children():
        widget.destroy()

    # config grid main
    frame.grid_rowconfigure(0, weight=0)  # title - fixed
    frame.grid_rowconfigure(1, weight=1)  # content - expand
    frame.grid_columnconfigure(0, weight=1) # "       "

    # title
    title = tk.Label(
        frame,
        text=f"{brand} - {device} MODELS",
        font=("Arial", 24, "bold"),
        fg="black"
    )
    title.grid(row=0, column=0, pady=20)

    # container used for cards
    container = tk.Frame(frame)
    container.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

    # 3 columns for grid layout
    for i in range(3):
        container.grid_columnconfigure(i, weight=1, uniform="col")

    # gets models
    models_data = get_models(device, brand)

    # finds model with most specs listed (used for equal height cards)
    max_specs = max([len(m['specs']) for m in models_data], default=0)

    # calculates rows needed for 3 columns
    num_columns = 3
    num_rows = (len(models_data) + num_columns - 1) // num_columns if models_data else 1

    # creates cards
    if not models_data:
        tk.Label(container, text="No models found in inventory.", font=("Arial", 14)).grid(row=0, column=0, columnspan=3)
    for i, details in enumerate(models_data):
        row = i // 3
        col = i % 3
        model = details['model_name']
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
        card.grid_rowconfigure(3, weight=0)  # functionality: fixed
        card.grid_rowconfigure(4, weight=0)  # specs: fixed
        card.grid_rowconfigure(5, weight=1)  # specs list (stretches)
        card.grid_rowconfigure(6, weight=0)  # price: fixed
        card.grid_rowconfigure(7, weight=0)  # stock: fixed
        card.grid_rowconfigure(8, weight=0)  # buttons: fixed
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
            text=f"ID: {details['id']}",
            bg="white",
            font=("Arial", 10)
        ).grid(row=1, column=0, pady=(0, 10), sticky="ew")

        # serial number
        tk.Label(
            card,
            text=f"Serial: {details.get('serial_num', 'N/A')}",
            bg="white",
            font=("Arial", 10)
        ).grid(row=2, column=0, pady=(0, 10), sticky="ew")

        # functionality / condition
        func = details['functionality']
        if func == "Excellent":
            func_color = "green"
        elif func == "Good":
            func_color = "orange"
        else:  # Fair
            func_color = "red"

        tk.Label(
            card,
            text=f"Condition: {func}",
            bg="white",
            fg=func_color,
            font=("Arial", 10, "bold")
        ).grid(row=3, column=0, sticky="w", padx=10, pady=(0, 10))

        tk.Label(
            card,
            text="Specs:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=4, column=0, sticky="w", padx=10, pady=(5, 0))

        # specs list frame
        specs_frame = tk.Frame(card, bg="white")
        specs_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
        specs_frame.grid_columnconfigure(0, weight=1)

        # list specs
        for j, spec in enumerate(details['specs']):
            tk.Label(
                specs_frame,
                text=f"• {spec}",
                bg="white",
                font=("Arial", 9),
                wraplength=200,
                justify="left"
            ).grid(row=i, column=0, sticky="w", pady=2)

        # add empty rows to match tallest card (keeps all cards same height)
        for empty_row in range(len(details['specs']), max_specs):
            tk.Label(
                specs_frame,
                text="",
                bg="white",
                font=("Arial", 9)
            ).grid(row=empty_row, column=0, pady=2)

        tk.Label(
            card,
            text=f"Price: ₱{details['price']:,}",
            font=("Arial", 11, "bold"),
            fg="green",
            bg="white"
        ).grid(row=6, column=0, pady=(10, 5), sticky="ew")

        stock_color = "red" if details['available'] == 0 else "darkgreen"
        tk.Label(
            card,
            text=f"Stock: {details['available']}",
            fg=stock_color,
            bg="white",
            font=("Arial", 10, "bold")
        ).grid(row=7, column=0, pady=(0, 10), sticky="ew")

        button_row = tk.Frame(card, bg="white")
        button_row.grid(row=8, column=0, pady=(0, 15), sticky="ew")
        button_row.grid_columnconfigure(0, weight=1)  # Left side
        button_row.grid_columnconfigure(1, weight=1)  # Right side

        rent_btn = tk.Button(
            button_row,
            text="Rent Me",
            bg="#ffd735",
            fg = "black",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=lambda: app.set_active_page("add_rental")
        )
        rent_btn.grid(row=0, column=0, padx=10, sticky="w")
        add_hover(rent_btn, "#232624", "#ffd735", "#ffd735", "black")

        # disable if out of stock
        if details['available'] == 0:
            rent_btn.config(state="disabled", bg="gray", text="OUT OF STOCK")

        # menu button (⋯) - RIGHT SIDE
        menu_btn = tk.Button(
            button_row,
            text="☰",
            font=("Arial", 16, "bold"),
            bg="#ffd735",
            fg="black",
            cursor="hand2",
            width=3,
            relief="raised"
        )
        menu_btn.grid(row=0, column=1, padx=10, sticky="e")
        add_hover(menu_btn, "#d0d0d0", "#e0e0e0", "black", "black")

         # create dropdown menu for this specific card
        menu = tk.Menu(menu_btn, tearoff=0)
        menu.add_command(
            label="✏️ Edit Details",
            command=lambda d=device, b=brand, m=model: open_edit_details(app, d, b, m)
        )
        menu.add_separator()
        menu.add_command(
            label="🗑️ Delete Model",
            command=lambda d=device, b=brand, m=model: delete_model(app, d, b, m)
        )

        # Bind the menu to appear when clicking the button
        def show_menu(event, menu=menu, btn=menu_btn):
            try:
                menu.post(btn.winfo_rootx(), btn.winfo_rooty() + btn.winfo_height())
            except:
                pass

        menu_btn.bind("<Button-1>", show_menu)


    # config row weights for even distribution
    for r in range(num_rows):
        container.grid_rowconfigure(r, weight=1)


    # frame for buttons at the bottom (add, back)
    btm_btn_frame = tk.Frame(frame)
    btm_btn_frame.grid(row=2, column=0, sticky="ew", pady=20)
    btm_btn_frame.grid_columnconfigure(0, weight=1)  # Left side
    btm_btn_frame.grid_columnconfigure(1, weight=1)  # Right side

    # add device - left (sticky = "w")
    add_btn = tk.Button(
        btm_btn_frame,
        text="+ Add Another Device",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        cursor="hand2",
        relief="raised",
        command=lambda d=device, b=brand: add_device(app, device, brand)
    )
    add_btn.grid(row=0, column=0, sticky="w", padx=40)
    add_hover(add_btn, "#45a049", "#4CAF50", "white", "white")

    # back button - RIGHT (sticky = "e")
    back_btn = tk.Button(
        btm_btn_frame,
        text="←",
        font=("Arial", 14, "bold"),
        bg="#ffd735",
        fg="black",
        cursor="hand2",
        command=lambda: app.pages["brand_devices"].tkraise()
    )
    back_btn.grid(row=0, column=1, sticky="e", padx=40)
    add_hover(back_btn, "#232624", "#ffd735", "#ffd735", "black")

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

    # row 3: functionality (NEW - dropdown)
    tk.Label(form, text="Functionality:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    from tkinter import ttk
    func_var = tk.StringVar(value="Excellent")  # Default value
    func_combo = ttk.Combobox(
        form,
        textvariable=func_var,
        values=["Excellent", "Good", "Fair"],
        font=("Arial", 12),
        state="readonly",
        width=33
    )
    func_combo.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # row 4: price
    tk.Label(form, text="Price (₱):", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    price_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    price_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # row 5: stock
    tk.Label(form, text="Stock:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))

    stock_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    stock_entry.grid(row=row, column=1, sticky="ew", pady=10)
    row += 1

    # row 6: specs
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
        functionality = func_var.get()
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
            functionality=functionality,
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

    tk.Button(
        btn_frame,
        text="Add Model",
        font=("Arial", 14, "bold"),
        bg="#ffd735",
        cursor="hand2",
        command=save
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Cancel",
        font=("Arial", 14, "bold"),
        bg="#cccccc",
        cursor="hand2",
        command=lambda: app.pages["brand_details"].tkraise()
    ).pack(side="left", padx=10)

    # Show the page
    app.pages["add_device"].tkraise()