import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "iRENT.db")

def get_connection():
    return sqlite3.connect(db_path)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Brand (
        BrandID INTEGER PRIMARY KEY AUTOINCREMENT,
        BrandName TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DeviceType (
        DeviceTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        TypeName TEXT NOT NULL
    )
    """)

#stafffffffff
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
        StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        MiddleName TEXT,
        LastName TEXT NOT NULL,
        Suffix TEXT,
        ContactNo TEXT NOT NULL UNIQUE,
        EmailAdd TEXT NOT NULL UNIQUE,
        Username TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL
    )
    """)


    #customer/rentee
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        MiddleName TEXT,
        LastName TEXT NOT NULL,
        Suffix TEXT,
        Birthday TEXT,
        ContactNumber TEXT NOT NULL UNIQUE,
        EmailAddress TEXT NOT NULL UNIQUE,
        Region TEXT,
        Province TEXT,
        City TEXT,
        Barangay TEXT,
        Postal TEXT,
        Street TEXT,
        Status TEXT DEFAULT 'Active'
    )
    """)

    #dev (UPDATED WITH NEW COLUMNS  by Yuri)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Device (
        DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
        Model TEXT NOT NULL,
        ProductID TEXT,
        SerialNumber TEXT NOT NULL UNIQUE,
        RentalPrice REAL NOT NULL,
        SpecsText TEXT,
        AvailabilityStatus TEXT CHECK(AvailabilityStatus IN ('Available', 'Rented', 'Maintenance', 'Retired')),
        DeviceTypeID INTEGER,
        BrandID INTEGER,
        FOREIGN KEY(DeviceTypeID) REFERENCES DeviceType(DeviceTypeID),
        FOREIGN KEY(BrandID) REFERENCES Brand(BrandID)
    )
    """)

    #rental
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Rental (
        RentalID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INTEGER NOT NULL,
        StaffID INTEGER NOT NULL,
        DeviceID INTEGER NOT NULL,
        RentalDate TEXT NOT NULL,
        ReturnDate TEXT NOT NULL,
        RentalStatus TEXT NOT NULL DEFAULT 'Ongoing',
        PriceAtRental DECIMAL (10, 2) NOT NULL,
        DateReturned TEXT NOT NULL,
        PenaltyFee DECIMAL (10, 2) NOT NULL,
        TotalRentalFee REAL DEFAULT 0,
        CHECK(RentalStatus IN ('Ongoing', 'Completed', 'Overdue')),
        FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY(StaffID) REFERENCES Staff(StaffID) ON DELETE RESTRICT,
        FOREIGN KEY(DeviceID) REFERENCES Device(DeviceID) ON DELETE RESTRICT
    )
    """)

    #rental item

     #ilagay ung list of devices ni charmie (pakiupdate mamaya na!)
    cursor.execute("SELECT COUNT(*) FROM Device")
    if cursor.fetchone()[0] == 0:
        # Insert DeviceTypes and Brands from the DATA dict
        DATA = {
            "CAMERA": {
                "SONY": {
                    "SONY A7 IV": {"id": "CAM-001", "specs": ["33MP Full Frame", "4K 60fps", "IBIS Stabilization"], "price": 500, "available": 3},
                    "SONY FX3": {"id": "CAM-002", "specs": ["Cinema Camera", "4K 120fps", "Low Light Performance"], "price": 600, "available": 2},
                    "SONY ZV-E10 II": {"id": "CAM-003", "specs": ["APS-C Sensor", "4K Video", "Vlogging Focus"], "price": 450, "available": 4}
                },
                "CANON": {
                    "CANON EOS R5 II": {"id": "CAM-004", "specs": ["45MP", "8K Video", "Dual Pixel AF"], "price": 650, "available": 2},
                    "CANON EOS R6 III": {"id": "CAM-005", "specs": ["32.5MP Full-Frame", "7K 60p RAW", "4K 120p"], "price": 550, "available": 3},
                "INSTAX": {
                    "INSTAX MINI 12": {"id": "CAM-006", "specs": ["Instant Print", "Auto Exposure", "Compact"], "price": 200, "available": 10},
                    "INSTAX MINI EVO": {"id": "CAM-007", "specs": ["Hybrid Instant Camera", "Filters", "Bluetooth"], "price": 250, "available": 6}
                }
            },
            "CELLPHONE": {
                "IPHONE": {
                    "IPHONE 15 PRO MAX": {"id": "PHN-001", "specs": ["A17 Pro Chip", "48MP Camera", "Titanium Build"], "price": 800, "available": 5},
                    "IPHONE 16 PRO MAX": {"id": "PHN-002", "specs": ["Next Gen Chip", "Improved Battery", "Pro Camera System"], "price": 900, "available": 4}
                },
                "SAMSUNG": {
                    "GALAXY S24 ULTRA": {"id": "PHN-003", "specs": ["200MP Camera", "Snapdragon 8 Gen 3", "S-Pen"], "price": 750, "available": 6},
                    "GALAXY S25 ULTRA": {"id": "PHN-004", "specs": ["AI Camera", "Ultra Bright Display", "Long Battery"], "price": 850, "available": 5}
                },
                "XIAOMI": {
                    "XIAOMI 14T PRO": {"id": "PHN-005", "specs": ["Leica Camera", "Fast Charging", "AMOLED Display"], "price": 500, "available": 7}
                }
            },
            "CONSOLE": {
                "SONY": {"PLAYSTATION 5 SLIM": {"id": "CON-001", "specs": ["4K Gaming", "SSD Speed", "Ray Tracing"], "price": 600, "available": 4}},
                "MICROSOFT": {"XBOX SERIES X": {"id": "CON-002", "specs": ["4K 120fps", "Quick Resume", "1TB SSD"], "price": 620, "available": 3}},
                "NINTENDO": {"SWITCH OLED": {"id": "CON-003", "specs": ["Portable", "OLED Screen", "Handheld Mode"], "price": 400, "available": 8}}
            },
            "PORTABLE DVD PLAYER": {
                "SONY": {"DVP-FX980": {"id": "DVD-001", "specs": ["9-inch Screen", "Portable", "Rechargeable Battery"], "price": 150, "available": 5}},
                "PHILIPS": {"PD9012": {"id": "DVD-002", "specs": ["9-inch LCD", "USB Support", "Compact Design"], "price": 140, "available": 4}},
                "DBPOWER": {"MK101": {"id": "DVD-003", "specs": ["10.5-inch Screen", "Swivel Display", "Remote Control"], "price": 130, "available": 6}}
            },
            "LAPTOP": {
                "DELL": {"XPS 13": {"id": "LAP-001", "specs": ["i7", "16GB RAM", "512GB SSD"], "price": 700, "available": 5}},
                "HP": {"SPECTRE X360": {"id": "LAP-002", "specs": ["2-in-1", "Touchscreen", "i7 Processor"], "price": 750, "available": 4}},
                "LENOVO": {"THINKPAD X1 CARBON": {"id": "LAP-003", "specs": ["Business Laptop", "Lightweight", "i7 CPU"], "price": 800, "available": 3}}
            },
            "SOUND SYSTEM": {
                "JBL": {"PARTYBOX 110": {"id": "AUD-001", "specs": ["Bass Boost", "Portable", "LED Lights"], "price": 300, "available": 6}},
                "SAMSUNG": {"HW-Q990D": {"id": "AUD-002", "specs": ["Dolby Atmos", "11.1.4 Channel", "Wireless Subwoofer"], "price": 400, "available": 4}},
                "SVS": {"PRIME TOWER": {"id": "AUD-003", "specs": ["Hi-Fi Sound", "Home Theater", "Deep Bass"], "price": 500, "available": 3}}
            }
        }}

        # Insert categories and brands first
        for cat in DATA:
            cursor.execute("INSERT OR IGNORE INTO DeviceType (TypeName) VALUES (?)", (cat,))
        all_brands = set()
        for brands in DATA.values():
            all_brands.update(brands.keys())
        for brand in all_brands:
            cursor.execute("INSERT OR IGNORE INTO Brand (BrandName) VALUES (?)", (brand,))

        # Helper to get IDs
        def get_type_id(name):
            cursor.execute("SELECT DeviceTypeID FROM DeviceType WHERE TypeName=?", (name,))
            return cursor.fetchone()[0]
        def get_brand_id(name):
            cursor.execute("SELECT BrandID FROM Brand WHERE BrandName=?", (name,))
            return cursor.fetchone()[0]

        # Insert devices
        for category, brands in DATA.items():
            type_id = get_type_id(category)
            for brand, models in brands.items():
                brand_id = get_brand_id(brand)

                for model, details in models.items():
                    specs_text = "|".join(details["specs"])   # store as delimiter-separated string
                    for i in range(details["available"]):
                        serial = f"{details['id']}-{i+1:03d}"
                        cursor.execute("""
                            INSERT INTO Device
                            (Model, ProductID, SerialNumber, RentalPrice,
                            AvailabilityStatus, DeviceTypeID, BrandID, SpecsText)
                            VALUES (?, ?, ?, ?, ?, ?, ? ,?)
                        """, (model, details["id"], serial, details["price"], 
                              'Available', type_id, brand_id, specs_text))
        conn.commit()
    
    conn.close()