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

    cursor.execute("INSERT OR IGNORE INTO Brand (BrandID, BrandName) VALUES (1, 'Generic')")
    cursor.execute("INSERT OR IGNORE INTO DeviceType (DeviceTypeID, TypeName) VALUES (1, 'General')")

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
        City TEXT,
        Barangay TEXT,
        Postal TEXT,
        Street TEXT
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
        FunctionalStatus TEXT CHECK(FunctionalStatus IN ('Excellent', 'Good', 'Fair', 'Poor')),
        Functionality TEXT DEFAULT 'Excellent',
        SpecsText TEXT,
        Appearance TEXT CHECK(Appearance IN ('New', 'Good', 'Scratched', 'Damaged')),
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
        TotalRentalFee REAL DEFAULT 0,
        CHECK(RentalStatus IN ('Ongoing', 'Completed', 'Overdue')),
        FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY(StaffID) REFERENCES Staff(StaffID) ON DELETE RESTRICT,
        FOREIGN KEY(DeviceID) REFERENCES Device(DeviceID) ON DELETE RESTRICT
    )
    """)

    #rental item
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RentalItem (
        RentalItemID INTEGER PRIMARY KEY AUTOINCREMENT,
        PriceAtRental DECIMAL (10, 2) NOT NULL,
        DateReturned TEXT NOT NULL,
        PenaltyFee DECIMAL (10, 2) NOT NULL,
        RentalID INTEGER NOT NULL,
        DeviceID INTEGER NOT NULL,
        FOREIGN KEY (RentalID) REFERENCES Rental(RentalID) ON DELETE CASCADE,
        FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE RESTRICT
    )
    """)

    #ilagay ung list of devices ni charmie (UPDATED INITIAL SEEDING by Yuri)
    cursor.execute("SELECT COUNT(*) FROM Device")
    if cursor.fetchone()[0] == 0:
        initial_devices = [
            # Model, ProductID, SerialNumber, RentalPrice, FunctionalStatus, Functionality, SpecsText, Appearance, AvailabilityStatus, DeviceTypeID, BrandID
            ("Laptop", "LAP-01", "SN-1001", 500.00, "Excellent", "Excellent", "16GB RAM|512GB SSD", "New", "Available", 1, 1),
            ("Monitor", "MON-01", "SN-2002", 150.00, "Good", "Good", "1080p|60Hz", "Good", "Available", 1, 1)
        ]
        cursor.executemany("""
            INSERT INTO Device (Model, ProductID, SerialNumber, RentalPrice, FunctionalStatus, Functionality, SpecsText,
                                Appearance, AvailabilityStatus, DeviceTypeID, BrandID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_devices)
        conn.commit()

    conn.close()