import tkinter as tk
from gui.add_rental import add_rental_page

DATA = {
    "CAMERA": {
        "SONY": {
            "SONY A7 IV": {
                "id": "CAM-001",
                "specs": ["33MP Full Frame", "4K 60fps", "IBIS Stabilization"],
                "price": 500,
                "available": 3
            },
            "SONY FX3": {
                "id": "CAM-002",
                "specs": ["Cinema Camera", "4K 120fps", "Low Light Performance"],
                "price": 600,
                "available": 2
            },
            "SONY ZV-E10 II": {
                "id": "CAM-003",
                "specs": ["APS-C Sensor", "4K Video", "Vlogging Focus"],
                "price": 450,
                "available": 4
            }
        },

        "CANON": {
            "CANON EOS R5 II": {
                "id": "CAM-004",
                "specs": ["45MP", "8K Video", "Dual Pixel AF"],
                "price": 650,
                "available": 2
            },
            "CANON EOS R6 III": {
                "id": "CAM-005",
                "specs": ["24MP", "4K 60fps", "Low Light Master"],
                "price": 550,
                "available": 3
            }
        },

        "INSTAX": {
            "INSTAX MINI 12": {
                "id": "CAM-006",
                "specs": ["Instant Print", "Auto Exposure", "Compact"],
                "price": 200,
                "available": 10
            },
            "INSTAX MINI EVO": {
                "id": "CAM-007",
                "specs": ["Hybrid Instant Camera", "Filters", "Bluetooth"],
                "price": 250,
                "available": 6
            }
        }
    },

    "CELLPHONE": {
        "IPHONE": {
            "IPHONE 15 PRO MAX": {
                "id": "PHN-001",
                "specs": ["A17 Pro Chip", "48MP Camera", "Titanium Build"],
                "price": 800,
                "available": 5
            },
            "IPHONE 16 PRO MAX": {
                "id": "PHN-002",
                "specs": ["Next Gen Chip", "Improved Battery", "Pro Camera System"],
                "price": 900,
                "available": 4
            }
        },

        "SAMSUNG": {
            "GALAXY S24 ULTRA": {
                "id": "PHN-003",
                "specs": ["200MP Camera", "Snapdragon 8 Gen 3", "S-Pen"],
                "price": 750,
                "available": 6
            },
            "GALAXY S25 ULTRA": {
                "id": "PHN-004",
                "specs": ["AI Camera", "Ultra Bright Display", "Long Battery"],
                "price": 850,
                "available": 5
            }
        },

        "XIAOMI": {
            "XIAOMI 14T PRO": {
                "id": "PHN-005",
                "specs": ["Leica Camera", "Fast Charging", "AMOLED Display"],
                "price": 500,
                "available": 7
            }
        }
    },

    "CONSOLE": {
        "SONY": {
            "PLAYSTATION 5 SLIM": {
                "id": "CON-001",
                "specs": ["4K Gaming", "SSD Speed", "Ray Tracing"],
                "price": 600,
                "available": 4
            }
        },

        "MICROSOFT": {
            "XBOX SERIES X": {
                "id": "CON-002",
                "specs": ["4K 120fps", "Quick Resume", "1TB SSD"],
                "price": 620,
                "available": 3
            }
        },

        "NINTENDO": {
            "SWITCH OLED": {
                "id": "CON-003",
                "specs": ["Portable", "OLED Screen", "Handheld Mode"],
                "price": 400,
                "available": 8
            }
        }
    },

    "PORTABLE DVD PLAYER": {
        "SONY": {
            "DVP-FX980": {
                "id": "DVD-001",
                "specs": ["9-inch Screen", "Portable", "Rechargeable Battery"],
                "price": 150,
                "available": 5
            }
        },

        "PHILIPS": {
            "PD9012": {
                "id": "DVD-002",
                "specs": ["10-inch Screen", "USB Support", "Compact Design"],
                "price": 140,
                "available": 4
            }
        },

        "DBPOWER": {
            "MK101": {
                "id": "DVD-003",
                "specs": ["12-inch Screen", "Swivel Display", "Remote Control"],
                "price": 130,
                "available": 6
            }
        }
    },

    "LAPTOP": {
        "DELL": {
            "XPS 13": {
                "id": "LAP-001",
                "specs": ["i7", "16GB RAM", "512GB SSD"],
                "price": 700,
                "available": 5
            }
        },

        "HP": {
            "SPECTRE X360": {
                "id": "LAP-002",
                "specs": ["2-in-1", "Touchscreen", "i7 Processor"],
                "price": 750,
                "available": 4
            }
        },

        "LENOVO": {
            "THINKPAD X1 CARBON": {
                "id": "LAP-003",
                "specs": ["Business Laptop", "Lightweight", "i7 CPU"],
                "price": 800,
                "available": 3
            }
        }
    },

    "SOUND SYSTEM": {
        "JBL": {
            "PARTYBOX 110": {
                "id": "AUD-001",
                "specs": ["Bass Boost", "Portable", "LED Lights"],
                "price": 300,
                "available": 6
            }
        },

        "SAMSUNG": {
            "HW-Q990D": {
                "id": "AUD-002",
                "specs": ["Dolby Atmos", "11.1.4 Channel", "Wireless Subwoofer"],
                "price": 400,
                "available": 4
            }
        },

        "SVS": {
            "PRIME TOWER": {
                "id": "AUD-003",
                "specs": ["Hi-Fi Sound", "Home Theater", "Deep Bass"],
                "price": 500,
                "available": 3
            }
        }
    }
}

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

    # viewing list of devices
    devices = [device for device in DATA.keys()]

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
        add_hover(btn, "#232624", "#ffd735", "#ffd735", "black")  # Use global


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
    
    # get brands
    brands = list(DATA[device].keys())
    num_brands = len(brands) 
    
    # set number of columns 
    num_columns = 3
    
    # calcu number of rows needed
    num_rows = (num_brands + num_columns - 1) // num_columns
    
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
        
        # config brand_frame for internal layout
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
    models = list(DATA[device][brand].keys())
    
    # finds model with most specs listed (used for equal height cards)
    max_specs = 0
    for model in models:
        details = DATA[device][brand][model]
        max_specs = max(max_specs, len(details['specs']))
    
    # calculates rows needed for 3 columns
    num_columns = 3
    num_rows = (len(models) + num_columns - 1) // num_columns
    
    # creates cards
    for i, model in enumerate(models):
        row = i // 3
        col = i % 3
        
        # card frame
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
        card.grid_rowconfigure(2, weight=0)  # specs: fixed
        card.grid_rowconfigure(3, weight=1)  # specs list (stretches)
        card.grid_rowconfigure(4, weight=0)  # price: fixed
        card.grid_rowconfigure(5, weight=0)  # stock: fixed
        card.grid_rowconfigure(6, weight=0)  # rentme: fixed 
        card.grid_columnconfigure(0, weight=1) # column stretches
        
        details = DATA[device][brand][model]
        
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
        
        tk.Label(
            card,
            text="Specs:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=(5, 0))
        
        # specs list frame
        specs_frame = tk.Frame(card, bg="white")
        specs_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        specs_frame.grid_columnconfigure(0, weight=1)
        
        # add specs
        for i, spec in enumerate(details['specs']):
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
        ).grid(row=4, column=0, pady=(10, 5), sticky="ew")
        
        stock_color = "red" if details['available'] == 0 else "darkgreen"
        tk.Label(
            card,
            text=f"Stock: {details['available']}",
            fg=stock_color,
            bg="white",
            font=("Arial", 10, "bold")
        ).grid(row=5, column=0, pady=(0, 10), sticky="ew")
        
        rent_btn = tk.Button(
            card,
            text="Rent Me",
            bg="#ffd735",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=lambda : app.set_active_page("add_rental") #calls add_rental_page
        )
        rent_btn.grid(row=6, column=0, pady=(0, 15))
        add_hover(rent_btn, "#232624", "#ffd735", "#ffd735", "black")
        
        # disables if out of stock: shows message
        if details['available'] == 0:
            rent_btn.config(state="disabled", bg="gray", text="OUT OF STOCK")
    
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
    
    # Make 2 columns in the form (labels on left, entries on right)
    form.grid_columnconfigure(0, weight=0)  # labels (id, price, stock, etc) FIXED 
    form.grid_columnconfigure(1, weight=1)  # entries (enter id, enter price, etc) EXPANDS
    
    # row 0: model name
    tk.Label(form, text="Model Name:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 20))
    
    model_entry = tk.Entry(form, font=("Arial", 12), width=35,  bd=1, relief="solid")
    model_entry.grid(row=0, column=1, sticky="ew", pady=10)
    
    # row 1 form: id
    tk.Label(form, text="ID:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 20))
    
    id_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    id_entry.grid(row=1, column=1, sticky="ew", pady=10)
    
    # row 2 form: price
    tk.Label(form, text="Price (₱):", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 20))
    
    price_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    price_entry.grid(row=2, column=1, sticky="ew", pady=10)
    
    # row 3 form: stock
    tk.Label(form, text="Stock:", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=3, column=0, sticky="w", pady=10, padx=(0, 20))
    
    stock_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    stock_entry.grid(row=3, column=1, sticky="ew", pady=10)
    
    # row 4 form: specs
    tk.Label(form, text="Specs (separate with commas):", font=("Arial", 12, "bold"), bg="white"
    ).grid(row=4, column=0, sticky="w", pady=10, padx=(0, 20))
    
    specs_entry = tk.Entry(form, font=("Arial", 12), width=35, bd=1, relief="solid")
    specs_entry.grid(row=4, column=1, sticky="ew", pady=10)
    
    #suggestion label, below specs entry box
    tk.Label(
        form, 
        text="Example: 33MP, 4K Video, IBIS Stabilization", 
        font=("Arial", 8), 
        fg="gray",
        bg="white"
    ).grid(row=5, column=1, sticky="w", pady=(0, 10))
    
    #starts empty and later used as message.config to display error messages differently
    message = tk.Label(frame, text="", font=("Arial", 11))
    message.grid(row=3, column=0, pady=10)
    
    #add, cancel
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=4, column=0, pady=20)
    
    def save():
        #gets what user typed
        name = model_entry.get().strip().upper()
        pid = id_entry.get().strip().upper()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()
        specs_text = specs_entry.get().strip()
        
        #validates every entry and shows warning 
        if not name:
            message.config(text="Enter model name!", fg="red")
            return
        if not pid:
            message.config(text="Enter ID!", fg="red")
            return
        if not price or not price.isdigit():
            message.config(text="Enter valid price!", fg="red")
            return
        if not stock or not stock.isdigit():
            message.config(text="Enter valid stock!", fg="red")
            return
        if not specs_text:
            message.config(text="Enter specs!", fg="red")
            return
        
        #checks if model exists
        if name in DATA[device][brand]:
            message.config(text=f"❌ {name} already exists!", fg="red")
            return
        
        #converts specs into list
        specs_list = [s.strip() for s in specs_text.split(",")]
        
        #saves to data (temp)
        DATA[device][brand][name] = {
            "id": pid,
            "specs": specs_list,
            "price": int(price),
            "available": int(stock)
        }
        #shows success text
        message.config(text=f"✅ {name} added!", fg="green")
        
        #automatically goes back to brand_details after saving. shows the added device during run
        frame.after(1000, lambda: app.pages["brand_details"].tkraise())
        frame.after(1000, lambda: show_brand_details(app, device, brand))

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