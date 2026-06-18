import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "iRENT.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# For customers
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

# For rents
cursor.execute("""
CREATE TABLE IF NOT EXISTS Rental (
    RentalID INTEGER PRIMARY KEY AUTOINCREMENT,
    SRentalMonth INTEGER NOT NULL,
    SRentalDay INTEGER NOT NULL,
    SRentalYear INTEGER NOT NULL,
    ExReturnMonth INTEGER NOT NULL,
    ExReturnDay INTEGER NOT NULL,
    ExReturnYear INTEGER NOT NULL,
    RentalStatus TEXT NOT NULL,
    TotalRentalFee DECIMAL (10, 2) NOT NULL,
    CustomerID INTEGER NOT NULL,
    StaffID INTEGER NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE RESTRICT
)
""")

# For rent item
cursor.execute("""
CREATE TABLE IF NOT EXISTS RentalItem (
    RentalItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    PriceAtRental DECIMAL (10, 2) NOT NULL,
    DRMonth INTEGER NOT NULL,
    DRDay INTEGER NOT NULL,
    DRYear INTEGER NOT NULL,
    PenaltyFee DECIMAL (10, 2) NOT NULL,
    RentalID INTEGER NOT NULL,
    DeviceID INTEGER NOT NULL,
    FOREIGN KEY (RentalID) REFERENCES Rental(RentalID) ON DELETE CASCADE,
    FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE RESTRICT
)
""")

# For device
cursor.execute("""
CREATE TABLE IF NOT EXISTS Device (
    DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
    Model TEXT NOT NULL,
    SerialNumber TEXT NOT NULL UNIQUE,
    RentalPrice DECIMAL (10, 2) NOT NULL,
    FunctionalStatus TEXT CHECK(FunctionalStatus IN ('Excellent', 'Good', 'Fair', 'Poor')),
    Appearance TEXT CHECK(Appearance IN ('New', 'Good', 'Scratched', 'Damaged')),
    AvailabilityStatus TEXT CHECK(AvailabilityStatus IN ('Available', 'Rented', 'Maintenance', 'Retired')),
    DeviceTypeID INTEGER NOT NULL,
    BrandID INTEGER NOT NULL,
    FOREIGN KEY (DeviceTypeID) REFERENCES DeviceType(DeviceTypeID) ON DELETE SET NULL,
    FOREIGN KEY (BrandID) REFERENCES Brand(BrandID) ON DELETE SET NULL
)
""")

# Get all rentals
def get_all_rentals(conn):
    """Fetches all rentals joined with the customer's full name."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               r.RentalStatus,
               r.TotalRentalFee,
               r.SRentalMonth || '/' || r.SRentalDay || '/' || r.SRentalYear AS StartDate,
               r.ExReturnMonth || '/' || r.ExReturnDay || '/' || r.ExReturnYear AS ExpectedReturn
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        ORDER BY r.RentalID DESC
    ''')
    return cursor.fetchall()

# Display rentals based on status
def display_rentals(conn):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee,
               r.SRentalMonth,
               r.SRentalDay,
               r.SRentalYear,
               r.ExReturnMonth,
               r.ExReturnDay,
               r.ExReturnYear
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        ORDER BY r.RentalID DESC
    ''')

    return cursor.fetchall()

# Filter rental's status
def get_rentals_by_status(conn, status):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               r.RentalStatus,
               r.TotalRentalFee,
               r.SRentalMonth, 
               r.SRentalDay, 
               r.SRentalYear,
               r.ExReturnMonth, 
               r.ExReturnDay, 
               r.ExReturnYear
        FROM Rental r
        JOIN Customer c 
            ON r.CustomerID = c.CustomerID
        WHERE r.RentalStatus = ?
        ORDER BY r.RentalID DESC
    ''', (status,))

    return cursor.fetchall()

# Search rental by customer name or ID
def search_rentals(conn, search_term):
    cursor = conn.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee
        FROM Rental r
        JOIN Customer c 
            ON r.CustomerID = c.CustomerID
        WHERE CAST(r.RentalID AS TEXT) LIKE ?
           OR c.FirstName LIKE ?
           OR c.LastName LIKE ?
           OR (c.FirstName || ' ' || c.LastName) LIKE ?
        ORDER BY r.RentalID DESC
    ''', (search_pattern,) * 4)

    return cursor.fetchall()

# See more details of a rental
def get_rental_details(conn, rental_id):
    """Returns full rental breakdown including customer, address, device, dates, and fee."""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            r.RentalID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            c.ContactNumber,
            c.EmailAddress,
            c.Region,
            c.City,
            c.Barangay,
            c.Postal,
            c.Street,
            c.Birthday,
            d.Model,
            r.SRentalMonth,
            r.SRentalDay,
            r.SRentalYear,
            r.ExReturnMonth,
            r.ExReturnDay,
            r.ExReturnYear,
            r.TotalRentalFee,
            r.RentalStatus

        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        JOIN RentalItem ri
            ON r.RentalID = ri.RentalID
        JOIN Device d
            ON ri.DeviceID = d.DeviceID

        WHERE r.RentalID = ?
    ''', (rental_id,))

    return cursor.fetchone()

# Mark rental order complete
def mark_rental_as_completed(conn, rental_id):
    """Updates a rental record when equipment is successfully returned."""
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE Rental
        SET RentalStatus = 'Completed'
        WHERE RentalID = ?
    ''', (rental_id,))
    
    conn.commit()
    
    return cursor.rowcount > 0