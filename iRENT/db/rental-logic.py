import sqlite3

# Import all our database functions from the irent_db.py file
from sqlite_crudop import (
    make_database, get_connection, add_customer, add_device, create_rental_transaction, get_all_available_devices, get_customer_rental_history, get_overdue_rentals, search_device_by_model, mark_rental_as_returned, remove_retired_device
)

def make_database():
    """Ensure the database and required tables exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
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
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            MiddleName TEXT,
            LastName TEXT NOT NULL,
            Suffix TEXT,
            ContactNumber TEXT NOT NULL UNIQUE,
            EmailAddress TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeviceType (
            DeviceTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            TypeName TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Brand (
            BrandID INTEGER PRIMARY KEY AUTOINCREMENT,
            BrandName TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Device (
            DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
            Model TEXT NOT NULL,
            SerialNumber TEXT NOT NULL UNIQUE,
            RentalPrice DECIMAL(10, 2) NOT NULL,
            FunctionalStatus TEXT CHECK(FunctionalStatus IN ('Excellent', 'Good', 'Fair', 'Poor')),
            Appearance TEXT CHECK(Appearance IN ('New', 'Good', 'Scratched', 'Damaged')),
            AvailabilityStatus TEXT CHECK(AvailabilityStatus IN ('Available', 'Rented', 'Maintenance', 'Retired')),
            DeviceTypeID INTEGER,
            BrandID INTEGER,
            FOREIGN KEY (DeviceTypeID) REFERENCES DeviceType(DeviceTypeID) ON DELETE SET NULL,
            FOREIGN KEY (BrandID) REFERENCES Brand(BrandID) ON DELETE SET NULL
        )
    ''')

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
            TotalRentalFee DECIMAL(10, 2) NOT NULL,
            CustomerID INTEGER NOT NULL,
            StaffID INTEGER NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE RESTRICT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RentalItem (
            RentalItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            RentalID INTEGER NOT NULL,
            DeviceID INTEGER NOT NULL,
            PriceAtRental DECIMAL(10, 2) NOT NULL,
            DRMonth INTEGER NOT NULL,
            DRDay INTEGER NOT NULL,
            DRYear INTEGER NOT NULL,
            PenaltyFee DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (RentalID) REFERENCES Rental(RentalID) ON DELETE CASCADE,
            FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE RESTRICT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeviceSpecs (
            SpecsID INTEGER PRIMARY KEY AUTOINCREMENT,
            DeviceID INTEGER NOT NULL,
            Processor TEXT NOT NULL,
            RAM TEXT NOT NULL,
            Storage TEXT NOT NULL,
            OS TEXT NOT NULL,
            ScreenSize TEXT NOT NULL,
            BatteryLife TEXT NOT NULL,
            FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*45)
    print("      iRENT Electronic Rental System")
    print("="*45)
    print("1. Add a New Customer")
    print("2. Add a New Device")
    print("3. Create a Rental Transaction")
    print("4. View All Available Devices")
    print("5. View Customer Rental History")
    print("6. View Overdue Rentals")
    print("7. Search Device by Model")
    print("8. Mark Rental as Returned")
    print("9. Remove a Retired Device")
    print("0. Exit System")
    print("="*45)

def run_terminal_interface():
    """Main loop for the terminal UI."""
    # Ensure database and tables exist before starting
    make_database()

    # Enable foreign keys for this connection
    conn = get_connection()

    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ")

        try:
            if choice == '1':
                print("\n--- Add New Customer ---")
                fname = input("First Name: ")
                mname = input("Middle Name (leave blank if none): ")
                lname = input("Last Name: ")
                suffix = input("Suffix (leave blank if none): ")
                contact = input("Contact Number: ")
                email = input("Email Address: ")

                cust_id = add_customer(conn, fname, mname, lname, suffix, contact, email)
                print(f"Success! Customer added with ID: {cust_id}")

            elif choice == '2':
                print("\n--- Add New Device ---")
                model = input("Model Name: ")
                serial = input("Serial Number: ")
                price = float(input("Rental Price (e.g., 150.00): "))
                func = input("Functional Status (Excellent/Good/Fair/Poor): ").capitalize()
                appr = input("Appearance (New/Good/Scratched/Damaged): ").capitalize()
                avail = input("Availability (Available/Rented/Maintenance/Retired): ").capitalize()
                type_id = int(input("Device Type ID (integer): "))
                brand_id = int(input("Brand ID (integer): "))

                dev_id = add_device(conn, model, serial, price, func, appr, avail, type_id, brand_id)
                print(f"Success! Device added with ID: {dev_id}")

            elif choice == '3':
                print("\n--- Create Rental Transaction ---")
                cust_id = int(input("Customer ID: "))
                staff_id = int(input("Staff ID: "))
                s_month = int(input("Start Month (1-12): "))
                s_day = int(input("Start Day: "))
                s_year = int(input("Start Year: "))
                ex_month = int(input("Expected Return Month (1-12): "))
                ex_day = int(input("Expected Return Day: "))
                ex_year = int(input("Expected Return Year: "))
                fee = float(input("Total Rental Fee: "))

                rental_id = create_rental_transaction(conn, s_month, s_day, s_year, ex_month, ex_day, ex_year, 'Ongoing', fee, cust_id, staff_id)
                print(f"Success! Rental created with Transaction ID: {rental_id}")

            elif choice == '4':
                print("\n--- Available Devices ---")
                devices = get_all_available_devices(conn)
                if not devices:
                    print("No devices are currently available.")
                else:
                    print(f"{'ID':<5} | {'Model':<20} | {'Serial':<15} | {'Price':<10}")
                    print("-" * 60)
                    for d in devices:
                        print(f"{d[0]:<5} | {d[1]:<20} | {d[2]:<15} | ₱{d[3]:<10.2f}")

            elif choice == '5':
                print("\n--- Customer Rental History ---")
                cust_id = int(input("Enter Customer ID: "))
                history = get_customer_rental_history(conn, cust_id)
                if not history:
                    print("No rental history found for this customer.")
                else:
                    for r in history:
                        print(f"Rental ID: {r[0]} | Status: {r[1]} | Fee: ₱{r[2]} | Date: {r[3]}/{r[4]}/{r[5]}")

            elif choice == '6':
                print("\n--- Check Overdue Rentals ---")
                print("Enter today's date to check for overdue items.")
                c_month = int(input("Current Month (1-12): "))
                c_day = int(input("Current Day: "))
                c_year = int(input("Current Year: "))

                overdue = get_overdue_rentals(conn, c_year, c_month, c_day)
                if not overdue:
                    print("No overdue rentals right now.")
                else:
                    for o in overdue:
                        print(f"Rental ID: {o[0]} | Customer: {o[1]} {o[2]} | Contact: {o[3]} | Expected Return: {o[4]}/{o[5]}/{o[6]}")

            elif choice == '7':
                print("\n--- Search Device ---")
                term = input("Enter model name to search: ")
                results = search_device_by_model(conn, term)
                if not results:
                    print("No devices found matching that model.")
                else:
                    for res in results:
                        print(f"ID: {res[0]} | Model: {res[1]} | Status: {res[6]}")

            elif choice == '8':
                print("\n--- Mark Rental as Returned ---")
                rental_id = int(input("Enter Rental ID to mark as returned: "))
                mark_rental_as_returned(conn, rental_id)
                print(f"Rental {rental_id} successfully marked as Returned.")

            elif choice == '9':
                print("\n--- Remove Retired Device ---")
                dev_id = int(input("Enter Device ID to remove: "))
                confirm = input(f"Are you sure you want to delete Device ID {dev_id}? (y/n): ")
                if confirm.lower() == 'y':
                    remove_retired_device(conn, dev_id)
                    print(f"Device {dev_id} removed from system.")
                else:
                    print("Deletion cancelled.")

            elif choice == '0':
                print("\nExiting iRENT System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 0 and 9.")

        except ValueError:
            print("\nInput Error: Please enter the correct data type (e.g., numbers for IDs and prices).")
        except sqlite3.Error as e:
            print(f"\nDatabase Error: {e}")
            print("Note: Check if you are missing data in parent tables (Staff, DeviceType, Brand) for foreign keys.")

    # Close the connection when the loop exits
    conn.close()

if __name__ == "__main__":
    run_terminal_interface()