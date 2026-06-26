from db.database import get_connection
import sqlite3

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
        SELECT DeviceID, Model, RentalPrice
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
        return_date,
        total_fee
    ):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Rental (
                CustomerID, 
                StaffID, 
                DeviceID,
                RentalDate, 
                ReturnDate,
                TotalRentalFee
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            staff_id,
            device_id,
            rental_date,
            return_date,
            total_fee
        ))

        cursor.execute("""
            UPDATE Device SET AvailabilityStatus = 'Rented'
            WHERE DeviceID = ?
        """, (device_id,))

        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
    finally:
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


def load_devices():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DT.TypeName, B.BrandName, D.Model, D.RentalPrice, D.DeviceID
        FROM Device D
        JOIN DeviceType DT ON D.DeviceTypeID = DT.DeviceTypeID
        JOIN Brand B ON D.BrandID = B.BrandID
        WHERE D.AvailabilityStatus = 'Available'
    """)
    rows = cursor.fetchall()
    conn.close()

    hierarchy = {}
    for device_id, dev_type, brand, model, price in rows:
        if dev_type not in hierarchy:
            hierarchy[dev_type] = {}
        if brand not in hierarchy[dev_type]:
            hierarchy[dev_type][brand] = {}
        
        hierarchy[dev_type][brand][model] = {
            "id": device_id,
            "price": price
        }
    
    return hierarchy

def all_avail_dev():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT D.DeviceID, DT.TypeName, B.BrandName, D.Model, D.RentalPrice
        FROM Device D
        JOIN DeviceType DT ON D.DeviceTypeID = DT.DeviceTypeID
        JOIN Brand B ON D.BrandID = B.BrandID
        WHERE D.AvailabilityStatus = 'Available'
    """)
    return [{"id": r[0], "type": r[1], "brand": r[2], "model": r[3], "price": r[4]} for r in cursor.fetchall()]