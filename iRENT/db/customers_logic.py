import sqlite3
from db.database import get_connection

def get_all_customers(status='Active'):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customer WHERE Status = ?", (status,))
    rows = cursor.fetchall()
    
    colnames = [description[0] for description in cursor.description]
    customers = [dict(zip(colnames, row)) for row in rows]
    
    conn.close()
    return customers

def customer_rentals(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT D.Model, R.RentalDate, R.ReturnDate, R.RentalStatus 
        FROM Rental R
        JOIN Device D ON R.DeviceID = D.DeviceID
        WHERE R.CustomerID = ?
    """
    cursor.execute(query, (customer_id,))
    rows = cursor.fetchall()

    rentals = [
        {"name": row[0], "rented_date": row[1], "due_date": row[2], "status": row[3]} 
        for row in rows
    ]
    
    conn.close()
    return rentals


def update_customer(customer_id, data_dict):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:

        data_dict['CustomerID'] = customer_id

        query = """UPDATE Customer SET 
                   FirstName=:FirstName, MiddleName=:MiddleName, LastName=:LastName, 
                   Suffix=:Suffix, Birthday=:Birthday, ContactNumber=:ContactNumber, 
                   EmailAddress=:EmailAddress, Region=:Region, City=:City, 
                   Barangay=:Barangay, Postal=:Postal, Street=:Street 
                   WHERE CustomerID=:CustomerID"""
        
        cursor.execute(query, data_dict)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating customer: {e}")
        return False
    finally:
        conn.close()

def has_active_rentals(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM Rental
        WHERE CustomerID = ? AND RentalStatus IN ('Ongoing', 'Overdue')
    """, (customer_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def archive_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Customer SET Status = 'Archived' WHERE CustomerID = ?", (customer_id,))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def unarchive_customer(customer_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Customer SET Status = 'Active' WHERE CustomerID = ?", (customer_id,))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()