import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "iRENT.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()



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


#dev
cursor.execute("""
CREATE TABLE IF NOT EXISTS Device (
    DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
    Model TEXT NOT NULL,
    SerialNumber TEXT NOT NULL UNIQUE,
    RentalPrice REAL NOT NULL,

    FunctionalStatus TEXT CHECK(FunctionalStatus IN ('Excellent', 'Good', 'Fair', 'Poor')),
    Appearance TEXT CHECK(Appearance IN ('New', 'Good', 'Scratched', 'Damaged')),
    AvailabilityStatus TEXT CHECK(AvailabilityStatus IN ('Available', 'Rented', 'Maintenance', 'Retired')),

    DeviceTypeID INTEGER,
    BrandID INTEGER
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

#device ganto muna ksi wala pa
cursor.execute("SELECT COUNT(*) FROM Device")

if cursor.fetchone()[0] == 0:
    cursor.execute("""
        INSERT INTO Device (
            Model, SerialNumber, RentalPrice,
            FunctionalStatus, Appearance, AvailabilityStatus,
            DeviceTypeID, BrandID
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "KUNWARE DEVICE",
        "DEVICE-001",
        0,
        "Good",
        "New",
        "Available",
        1,
        1
    ))

    conn.commit()




def getcreate_customer(
        first, 
        middle, 
        last, 
        suffix, 
        birthday,
        contact, 
        email,
        region,
        city,
        barangay,
        postal,
        street
    ):

    cursor.execute("""
        SELECT CustomerID FROM Customer
        WHERE ContactNumber = ? OR EmailAddress = ?
    """, (contact, email))

    row = cursor.fetchone()

    if row:
        return row[0]

    cursor.execute("""
    INSERT INTO Customer (
        FirstName, 
        MiddleName, 
        LastName, 
        Suffix,
        Birthday, 
        ContactNumber, 
        EmailAddress,
        Region,
        City,
        Barangay,
        Postal,
        Street
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    first, middle, last, suffix,
    birthday, contact, email,
    region, city, barangay, postal, street
))

    conn.commit()
    return cursor.lastrowid

def get_devices():
    cursor.execute("""
        SELECT DeviceID, Model
        FROM Device
        WHERE AvailabilityStatus = 'Available'
    """)
    return cursor.fetchall()

def create_rental(
        customer_id, 
        staff_id, 
        device_id,
        rental_date, 
        return_date
    ):



    cursor.execute("""
        INSERT INTO Rental (
            CustomerID, 
            StaffID, 
            DeviceID,
            RentalDate, 
            ReturnDate
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        customer_id,
        staff_id,
        device_id,
        rental_date,
        return_date
    ))

    conn.commit()

def get_customers():
    cursor.execute("""
        SELECT CustomerID, FirstName, MiddleName, LastName, Suffix, ContactNumber, EmailAddress, Region, City, Barangay, Postal, Street
        FROM Customer
    """)
    return cursor.fetchall()