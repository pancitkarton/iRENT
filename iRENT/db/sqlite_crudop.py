# Database code only. All to be compiled by Quitollo and Frianeza for tkinter.
import sqlite3
import os

# Database path setup
# Gets the exact directory where this python file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Forces the database to be named iRENT.db inside that exact directory
DB_PATH = os.path.join(BASE_DIR, 'iRENT.db')

def get_connection():
    """Helper function to return a connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
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

    #To reference profiling ID. Paayos nalang, Quitollo.

    # Create Customer table
    # Added customer address (5 composite values)
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
    # Included CustomerID INTEGER NOT NULL, and StaffID INTEGER NOT NULL. They're foreign keys in this table.
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
    # Included DeviceTypeID INTEGER NOT NULL, and BrandID INTEGER NOT NULL. They are foreign keys to this table.
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
    # Included DeviceID INTEGER NOT NULL. It is a foreign key to the table
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
# Basis of GUIs. 
# Only add more if necessary


# For Create/Insert/Add
def add_customer(conn, first_name, middle_name, last_name, suffix, contact, email):
    """Registers a new customer into the system."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Customer (FirstName, MiddleName, LastName, Suffix, ContactNumber, EmailAddress)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, middle_name, last_name, suffix, contact, email))
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


# For Read, Search, and Display
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

# added def rentals status filter (aayusin pa)
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

# added def search rentals by name or id (aayusin pa)
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

# added def get rental details (aayusin pa)
def get_rental_details(conn, rental_id):
    """Returns full rental breakdown including customer + dates + fee."""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            r.RentalID,
            c.FirstName || ' ' || c.LastName AS CustomerName,
            c.ContactNumber,
            c.EmailAddress,

            r.SRentalMonth, r.SRentalDay, r.SRentalYear,
            r.ExReturnMonth, r.ExReturnDay, r.ExReturnYear,

            r.RentalStatus,
            r.TotalRentalFee,

            s.FirstName || ' ' || s.LastName AS StaffName
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        JOIN Staff s ON r.StaffID = s.StaffID
        WHERE r.RentalID = ?
    ''', (rental_id,))

    return cursor.fetchone()


# For Update/Alter/Change
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
    print(f"Rental {rental_id} successfully marked as Completed.")
    # Set rentalstatus to complete, for status change effectiveness


# For Delete/Remove
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



# The def main(). 
# Initial logic only. The main basis are the crudops above.

def main():
    print(" iRENT Database Management System ")

    # Create database and tables
    make_database()

    # Open connection
    conn = get_connection()

    try:
        while True:
            print("\n--- DATABASE TEST MENU ---")
            print("1. Show Available Devices")
            print("2. Search Device by Model")
            print("3. Add Customer")
            print("4. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                devices = get_all_available_devices(conn)

                if not devices:
                    print("No available devices found.")
                else:
                    for device in devices:
                        print(device)

            elif choice == "2":
                model = input("Enter model name: ")
                results = search_device_by_model(conn, model)

                if not results:
                    print("No matching devices found.")
                else:
                    for device in results:
                        print(device)

            elif choice == "3":
                first = input("First Name: ")
                middle = input("Middle Name: ")
                last = input("Last Name: ")
                suffix = input("Suffix: ")
                contact = input("Contact Number: ")
                email = input("Email Address: ")

                customer_id = add_customer(
                    conn,
                    first,
                    middle,
                    last,
                    suffix,
                    contact,
                    email
                )

                print(f"Customer added successfully! ID = {customer_id}")

            elif choice == "4":
                print("Exiting iRENT Database System...")
                break

            else:
                print("Invalid choice. Try again.")

    except sqlite3.Error as e:
        print(f"Database Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()



# Alternate version of def main, if it is to be connected to GUI Tkinter
# Just change the def main.

# def main():
#   make_database()

#   conn = get_connection()

#   try:
#       print("Database initialized successfully.")
#       print("Connection established.")

        # Connect to Tkinter code place here

#   except sqlite3.Error as e:
#       print(f"Database Error: {e}")

#   finally:
#       conn.close()

# if __name__ == "__main__":
#   main()