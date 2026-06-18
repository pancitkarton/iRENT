from db.database import get_connection

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

    conn = get_connection()
    cursor = conn.cursor()

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
    customer_id = cursor.lastrowid
    conn.close()
    return customer_id


def get_devices():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DeviceID, Model
        FROM Device
        WHERE AvailabilityStatus = 'Available'
    """)
    results = cursor.fetchall()
    
    conn.close()
    return results


def create_rental(
        customer_id, 
        staff_id, 
        device_id,
        rental_date, 
        return_date
    ):

    conn = get_connection()
    cursor = conn.cursor()

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
    conn.close()

def get_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT CustomerID, FirstName, MiddleName, LastName, Suffix, ContactNumber, EmailAddress, Region, City, Barangay, Postal, Street
        FROM Customer
    """)

    results = cursor.fetchall()
    conn.close()
    return results

