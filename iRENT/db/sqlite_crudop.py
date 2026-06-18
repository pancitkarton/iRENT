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
            ZIPCode TEXT NOT NULL,
            BirthMonth TEXT NOT NULL,
            BirthDay TEXT NOT NULL,
            BirthYear TEXT NOT NULL
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
def add_customer(conn, first_name, middle_name, last_name, suffix, contact, email, street, barangay, city, province, zipcode, birthmonth, birthday, birthyear):
    """Registers a new customer into the system."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Customer (FirstName, MiddleName, LastName, Suffix, ContactNumber, EmailAddress, Street, Barangay, City, Province, ZIPCode, BirthMonth, BirthDay, BirthYear)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, middle_name, last_name, suffix, contact, email, street, barangay, city, province, zipcode, birthmonth, birthday, birthyear))
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

def add_device_specs(conn, device_id, processor, ram, storage, os, screen_size, battery_life):
    """Adds specifications for a device."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO DeviceSpecs (Processor, RAM, Storage, OS, ScreenSize, BatteryLife, DeviceID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (processor, ram, storage, os, screen_size, battery_life, device_id))
    conn.commit()
    return cursor.lastrowid

def add_device_type(conn, type_name):
    """Adds a new device type (e.g., CAMERA, CELLPHONE, CONSOLE)."""
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO DeviceType (TypeName)
            VALUES (?)
        ''', (type_name,))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Type already exists

def add_brand(conn, brand_name):
    """Adds a new brand (e.g., SONY, CANON, IPHONE)."""
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Brand (BrandName)
            VALUES (?)
        ''', (brand_name,))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Brand already exists

def create_rental_transaction(conn, s_month, s_day, s_year, ex_month, ex_day, ex_year, status, fee, customer_id, staff_id):
    """Creates a new rental record."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Rental (SRentalMonth, SRentalDay, SRentalYear, ExReturnMonth, ExReturnDay, ExReturnYear, RentalStatus, TotalRentalFee, CustomerID, StaffID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (s_month, s_day, s_year, ex_month, ex_day, ex_year, status, fee, customer_id, staff_id))
    conn.commit()
    return cursor.lastrowid

def add_rental_item(conn, rental_id, device_id, price_at_rental, dr_month, dr_day, dr_year, penalty_fee):
    """Adds a device to a rental transaction."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO RentalItem (RentalID, DeviceID, PriceAtRental, DRMonth, DRDay, DRYear, PenaltyFee)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (rental_id, device_id, price_at_rental, dr_month, dr_day, dr_year, penalty_fee))
    conn.commit()
    return cursor.lastrowid

# READ, DISPLAY FUNCTION
def get_all_device_types(conn):
    """Fetches all device types for the main device list page (e.g., CAMERA, CELLPHONE, CONSOLE)."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DeviceTypeID, TypeName
        FROM DeviceType
        ORDER BY TypeName ASC
    ''')
    return cursor.fetchall()

def get_brands_by_device_type(conn, device_type_id):
    """Fetches all brands for a specific device type."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT b.BrandID, b.BrandName
        FROM Brand b
        JOIN Device d ON b.BrandID = d.BrandID
        WHERE d.DeviceTypeID = ?
        ORDER BY b.BrandName ASC
    ''', (device_type_id,))
    return cursor.fetchall()

def get_brands_by_device_type_name(conn, device_type_name):
    """Fetches all brands for a specific device type by name."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT b.BrandID, b.BrandName
        FROM Brand b
        JOIN Device d ON b.BrandID = d.BrandID
        JOIN DeviceType dt ON d.DeviceTypeID = dt.DeviceTypeID
        WHERE dt.TypeName = ?
        ORDER BY b.BrandName ASC
    ''', (device_type_name,))
    return cursor.fetchall()

def get_device_type_id_by_name(conn, device_type_name):
    """Gets the DeviceTypeID from the device type name."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DeviceTypeID
        FROM DeviceType
        WHERE TypeName = ?
    ''', (device_type_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_brand_id_by_name(conn, brand_name):
    """Gets the BrandID from the brand name."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT BrandID
        FROM Brand
        WHERE BrandName = ?
    ''', (brand_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_models_by_brand_and_type(conn, device_type_id, brand_id):
    """Fetches all device models for a specific brand and device type."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.DeviceID, d.Model, d.RentalPrice, d.SerialNumber, 
               d.FunctionalStatus, d.Appearance, d.AvailabilityStatus
        FROM Device d
        WHERE d.DeviceTypeID = ? AND d.BrandID = ?
        ORDER BY d.Model ASC
    ''', (device_type_id, brand_id))
    return cursor.fetchall()

def get_models_by_brand_and_type_names(conn, device_type_name, brand_name):
    """Fetches all device models for a specific brand and device type using names."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.DeviceID, d.Model, d.RentalPrice, d.SerialNumber, 
               d.FunctionalStatus, d.Appearance, d.AvailabilityStatus
        FROM Device d
        JOIN DeviceType dt ON d.DeviceTypeID = dt.DeviceTypeID
        JOIN Brand b ON d.BrandID = b.BrandID
        WHERE dt.TypeName = ? AND b.BrandName = ?
        ORDER BY d.Model ASC
    ''', (device_type_name, brand_name))
    return cursor.fetchall()

def get_device_details(conn, device_id):
    """Fetches complete details of a single device including specs."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.DeviceID, d.Model, d.SerialNumber, d.RentalPrice,
               d.FunctionalStatus, d.Appearance, d.AvailabilityStatus,
               dt.TypeName, b.BrandName
        FROM Device d
        JOIN DeviceType dt ON d.DeviceTypeID = dt.DeviceTypeID
        JOIN Brand b ON d.BrandID = b.BrandID
        WHERE d.DeviceID = ?
    ''', (device_id,))
    return cursor.fetchone()

def get_device_specs(conn, device_id):
    """Fetches specifications for a specific device."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SpecsID, Processor, RAM, Storage, OS, ScreenSize, BatteryLife
        FROM DeviceSpecs
        WHERE DeviceID = ?
    ''', (device_id,))
    return cursor.fetchall()

def get_available_devices_count(conn):
    """Gets count of available devices by type and brand for inventory overview."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT dt.TypeName, b.BrandName, COUNT(d.DeviceID) as Count
        FROM Device d
        JOIN DeviceType dt ON d.DeviceTypeID = dt.DeviceTypeID
        JOIN Brand b ON d.BrandID = b.BrandID
        WHERE d.AvailabilityStatus = 'Available'
        GROUP BY dt.TypeName, b.BrandName
        ORDER BY dt.TypeName, b.BrandName
    ''')
    return cursor.fetchall()

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
            c.BirthMonth,
            c.BirthDay,
            c.BirthYear,
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

def update_device_details(conn, device_id, model=None, price=None, func_status=None, appearance=None):
    """Updates device information."""
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if model is not None:
        updates.append("Model = ?")
        params.append(model)
    if price is not None:
        updates.append("RentalPrice = ?")
        params.append(price)
    if func_status is not None:
        updates.append("FunctionalStatus = ?")
        params.append(func_status)
    if appearance is not None:
        updates.append("Appearance = ?")
        params.append(appearance)
    
    if not updates:
        return False
    
    params.append(device_id)
    query = f"UPDATE Device SET {', '.join(updates)} WHERE DeviceID = ?"
    
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount > 0

def update_device_specs(conn, device_id, processor=None, ram=None, storage=None, os=None, screen_size=None, battery_life=None):
    """Updates device specifications."""
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if processor is not None:
        updates.append("Processor = ?")
        params.append(processor)
    if ram is not None:
        updates.append("RAM = ?")
        params.append(ram)
    if storage is not None:
        updates.append("Storage = ?")
        params.append(storage)
    if os is not None:
        updates.append("OS = ?")
        params.append(os)
    if screen_size is not None:
        updates.append("ScreenSize = ?")
        params.append(screen_size)
    if battery_life is not None:
        updates.append("BatteryLife = ?")
        params.append(battery_life)
    
    if not updates:
        return False
    
    params.append(device_id)
    query = f"UPDATE DeviceSpecs SET {', '.join(updates)} WHERE DeviceID = ?"
    
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount > 0

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

def remove_device_specs(conn, device_id):
    """Removes specifications for a device."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DeviceSpecs WHERE DeviceID = ?", (device_id,))
    conn.commit()
    return cursor.rowcount > 0   

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