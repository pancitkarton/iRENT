# db functions for remaining needs
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, 'iRENT.db')

def get_connection():
    """Helper function to return a connection with foreign keys enabled."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def make_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Get Staff table from profiling
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Staff (
            StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR NOT NULL,
            MiddleName VARCHAR,
            LastName VARCHAR NOT NULL,
            Suffix VARCHAR,
            ContactNo VARCHAR NOT NULL UNIQUE,
            EmailAdd VARCHAR NOT NULL UNIQUE,
            Username VARCHAR NOT NULL UNIQUE,
            Password VARCHAR NOT NULL
        )
    ''')

    # Create Customer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            MiddleName TEXT,
            LastName TEXT NOT NULL,
            Suffix TEXT,
            ContactNumber TEXT NOT NULL UNIQUE,
            EmailAddress TEXT NOT NULL UNIQUE,
            Street TEXT NOT NULL,
            Barangay TEXT NOT NULL,
            City TEXT NOT NULL,
            Province TEXT NOT NULL,
            ZIPCode TEXT NOT NULL
        )
    ''')

    # Create Rental table
    cursor.execute('''
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
    ''')

    # Create Rental Item table (associative entity between Rental and Device)
    cursor.execute('''
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
    ''')

    # Create Device table
    cursor.execute('''
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
    ''')

    # Create table for multivalued attribute DeviceSpecs (under Device)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeviceSpecs (
            SpecsID INTEGER PRIMARY KEY AUTOINCREMENT,
            Processor TEXT NOT NULL,
            RAM TEXT NOT NULL,
            Storage TEXT NOT NULL,
            OS TEXT NOT NULL,
            ScreenSize TEXT NOT NULL,
            BatteryLife TEXT NOT NULL,
            DeviceID INTEGER NOT NULL,
            FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE CASCADE
        )
    ''')

    # Create Device Type table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeviceType (
            DeviceTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            TypeName TEXT NOT NULL UNIQUE
        )
    ''')

    # Create Brand table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Brand (
            BrandID INTEGER PRIMARY KEY AUTOINCREMENT,
            BrandName TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()


# CRUD Operations (Backend Code for GUIs).
# Only add more if necessary

# CREATE, ADD FUNCTION
def add_customer(conn, first_name, middle_name, last_name, suffix, contact, email, street, barangay, city, province, zipcode):
    """Registers a new customer into the system."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Customer (FirstName, MiddleName, LastName, Suffix, ContactNumber, EmailAddress, Street, Barangay, City, Province, ZIPCode)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, middle_name, last_name, suffix, contact, email, street, barangay, city, province, zipcode))
    conn.commit()
    return cursor.lastrowid

def add_device(conn, model, serial_number, price, func_status, appearance, avail_status, type_id, brand_id):
    """Adds a new electronic device to the inventory."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Device (Model, SerialNumber, RentalPrice, FunctionalStatus, Appearance, AvailabilityStatus, DeviceTypeID, BrandID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (model, serial_number, price, func_status, appearance, avail_status, type_id, brand_id))
    conn.commit()
    return cursor.lastrowid

def create_rental_transaction(conn, s_month, s_day, s_year, ex_month, ex_day, ex_year, status, fee, customer_id, staff_id):
    """Creates a new rental record."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Rental (SRentalMonth, SRentalDay, SRentalYear, ExReturnMonth, ExReturnDay, ExReturnYear, RentalStatus, TotalRentalFee, CustomerID, StaffID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (s_month, s_day, s_year, ex_month, ex_day, ex_year, status, fee, customer_id, staff_id))
    conn.commit()
    return cursor.lastrowid


# READ, DISPLAY FUNCTION
def get_all_available_devices(conn):
    """Fetches all devices currently marked as 'Available'."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.DeviceID, d.Model, d.SerialNumber, d.RentalPrice, t.TypeName, b.BrandName
        FROM Device d
        LEFT JOIN DeviceType t ON d.DeviceTypeID = t.DeviceTypeID
        LEFT JOIN Brand b ON d.BrandID = b.BrandID
        WHERE d.AvailabilityStatus = 'Available'
    ''')
    return cursor.fetchall()

def get_customer_rental_history(conn, customer_id):
    """Sample Query 2: Shows all rental transactions for a specific customer."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.RentalID, r.RentalStatus, r.TotalRentalFee, r.SRentalMonth, r.SRentalDay, r.SRentalYear
        FROM Rental r
        WHERE r.CustomerID = ?
    ''', (customer_id,))
    return cursor.fetchall()

def get_overdue_rentals(conn, current_year, current_month, current_day):
    """Sample Query 4: Displays overdue rentals and the responsible customers."""
    cursor = conn.cursor()
    # Logic checks if the expected return date is older than the current date provided
    cursor.execute('''
        SELECT r.RentalID, c.FirstName, c.LastName, c.ContactNumber, r.ExReturnMonth, r.ExReturnDay, r.ExReturnYear
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        WHERE r.RentalStatus = 'Ongoing'
            AND (r.ExReturnYear < ?
                OR (r.ExReturnYear = ? AND r.ExReturnMonth < ?)
                OR (r.ExReturnYear = ? AND r.ExReturnMonth = ? AND r.ExReturnDay   < ?))
    ''', (current_year, current_year, current_month, current_year, current_month, current_day))
    return cursor.fetchall()

def get_rentals_by_status(conn, status):
    """Allows staff to filter status (Ongoing, Overdue, Completed)."""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               r.RentalStatus,
               r.TotalRentalFee,
               r.SRentalMonth, r.SRentalDay, r.SRentalYear,
               r.ExReturnMonth, r.ExReturnDay, r.ExReturnYear
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        WHERE r.RentalStatus = ?
        ORDER BY r.RentalID DESC
    ''', (status,))

    return cursor.fetchall()

def search_rentals(conn, search_term):
    """Search rentals by RentalID or Customer name."""
    cursor = conn.cursor()

    # finds matching character at any position
    search_pattern = f"%{search_term}%"

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        WHERE CAST(r.RentalID AS TEXT) LIKE ?
           OR c.FirstName LIKE ?
           OR c.LastName LIKE ?
           OR (c.FirstName || ' ' || c.LastName) LIKE ?
        ORDER BY r.RentalID DESC
    ''', (search_pattern, search_pattern, search_pattern, search_pattern))

    return cursor.fetchall()

def search_device_by_model(conn, search_term):
    """Allows staff to search devices by model string."""
    cursor = conn.cursor()
    search_pattern = f"%{search_term}%"
    cursor.execute("SELECT * FROM Device WHERE Model LIKE ?", (search_pattern,))
    return cursor.fetchall()

def get_rental_details(conn, rental_id):
    """Returns full rental breakdown including customer, address, device, dates, and fee."""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            r.RentalID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            c.ContactNumber,
            c.EmailAddress,
            c.Street,
            c.Barangay,
            c.City,
            c.Province,
            c.ZIPCode,
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


# UPDATE FUNCTION
def update_device_availability(conn, device_id, new_status):
    """Updates device status (e.g., changing 'Available' to 'Rented' or 'Maintenance')."""
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Device
        SET AvailabilityStatus = ?
        WHERE DeviceID = ?
    ''', (new_status, device_id))
    conn.commit()

def mark_rental_as_completed(conn, rental_id):
    """Updates a rental record when equipment is successfully returned."""
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Rental
        SET RentalStatus = 'Completed'
        WHERE RentalID = ?
    ''', (rental_id,))
    conn.commit()
    return cursor.rowcount > 0  # Tells user if the row is updated after marking that row or rental as complete


# DELETE FUNCTION
def remove_retired_device(conn, device_id):
    """Removes damaged or retired equipment from the database entirely."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Device WHERE DeviceID = ?", (device_id,))
    conn.commit()
    print(f"Device {device_id} removed from system.")

def remove_customer(conn, customer_id):
    """Deletes a customer profile (Warning: cascades to delete their rentals if ON DELETE CASCADE is set properly)."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customer WHERE CustomerID = ?", (customer_id,))
    conn.commit()


# Initializes this database once when module is imported or explicitly called in GUI
make_database()

def init_db():
    conn = get_connection()
    return conn