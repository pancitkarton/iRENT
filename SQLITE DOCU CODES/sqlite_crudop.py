#Database code only. All to be compiled by Quitollo and Frianeza for tkinter.
import sqlite3

def make_database():
    conn = sqlite3.connect('iRENT.db')
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
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
        #To reference profiling ID. Kayo nalang mag-ayos.
    
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
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE RESTRICT
        )
    ''')
    
    # Create Rental Item table (associative entity between Rental and Device)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RentalItem (
            RentalItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY (RentalID) REFERENCES Rental(RentalID),
            FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID),
            PriceAtRental DECIMAL (10, 2) NOT NULL,
            DRMonth INTEGER NOT NULL,
            DRDay INTEGER NOT NULL,
            DRYear INTEGER NOT NULL,
            PenaltyFee DECIMAL (10, 2) NOT NULL,
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
            FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID) ON DELETE CASCADE
        )
    ''')
        #Add more if there's any other specs needed. Nilagay ko muna yung mga common.
        #Revise niyo nalang yung mga variables, especially on NOT NULL ones

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
    
#The next set of codes is for CRUD operations for each table. All to be done by Garcia, Piamonte, Quitollo. 

# For Create/Insert/Add


# For Read, Search, and Display


# For Update/Alter/Change


# For Delete/Remove


#def main() to be created by Alonzo once all CRUD operations are done.