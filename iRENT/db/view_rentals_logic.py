from db.database import get_connection
import sqlite3
from datetime import datetime

def check_overdue_rentals(conn):
    """Automatically updates the RentalStatus to 'Overdue' if the ReturnDate has passed."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT RentalID, ReturnDate FROM Rental WHERE RentalStatus = 'Ongoing'")
        ongoing_rentals = cursor.fetchall()
        
        today = datetime.today().date()
        for rental_id, return_date_str in ongoing_rentals:
            try:
                # Parse the mm-dd-yyyy date format
                return_date = datetime.strptime(return_date_str, "%m-%d-%Y").date()
                if today > return_date:
                    # Date has passed! Mark as Overdue
                    cursor.execute("UPDATE Rental SET RentalStatus = 'Overdue' WHERE RentalID = ?", (rental_id,))
            except ValueError:
                continue 
                
        conn.commit()
    except sqlite3.Error:
        pass


# RENTAL LISTING FUNCTIONS

def get_all_rentals():
    conn = get_connection()
    check_overdue_rentals(conn) # <-- Triggers dynamic date check
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || 
               CASE WHEN c.MiddleName IS NOT NULL AND c.MiddleName != '' THEN ' ' || c.MiddleName ELSE '' END || 
               ' ' || c.LastName || 
               CASE WHEN c.Suffix IS NOT NULL AND c.Suffix != '' THEN ' ' || c.Suffix ELSE '' END AS CustomerName,
               r.RentalStatus
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        ORDER BY r.RentalID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": str(row[0]),
            "rentee": row[1],
            "status": row[2]
        }
        for row in rows
    ]


def display_rentals():
    conn = get_connection()
    check_overdue_rentals(conn)
    cursor = conn.cursor()

    # FIXED: Replaced outdated SRentalMonth columns with the new RentalDate column
    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || 
               CASE WHEN c.MiddleName IS NOT NULL AND c.MiddleName != '' THEN ' ' || c.MiddleName ELSE '' END || 
               ' ' || c.LastName || 
               CASE WHEN c.Suffix IS NOT NULL AND c.Suffix != '' THEN ' ' || c.Suffix ELSE '' END AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee,
               r.RentalDate,
               r.ReturnDate
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        ORDER BY r.RentalID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": str(row[0]),
            "rentee": row[1],
            "contact": row[2],
            "status": row[3],
            "total_fee": row[4],
            "start_date": row[5],
            "expected_return": row[6]
        }
        for row in rows
    ]

def get_rentals_by_status(status):
    conn = get_connection()
    check_overdue_rentals(conn)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || 
               CASE WHEN c.MiddleName IS NOT NULL AND c.MiddleName != '' THEN ' ' || c.MiddleName ELSE '' END || 
               ' ' || c.LastName || 
               CASE WHEN c.Suffix IS NOT NULL AND c.Suffix != '' THEN ' ' || c.Suffix ELSE '' END AS CustomerName,
               r.RentalStatus
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        WHERE r.RentalStatus = ?
        ORDER BY r.RentalID DESC
    """, (status,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": str(row[0]),
            "rentee": row[1],
            "status": row[2]
        }
        for row in rows
    ]


def search_rentals(search_term):
    conn = get_connection()
    check_overdue_rentals(conn)
    cursor = conn.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || 
               CASE WHEN c.MiddleName IS NOT NULL AND c.MiddleName != '' THEN ' ' || c.MiddleName ELSE '' END || 
               ' ' || c.LastName || 
               CASE WHEN c.Suffix IS NOT NULL AND c.Suffix != '' THEN ' ' || c.Suffix ELSE '' END AS CustomerName,
               r.RentalStatus
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        WHERE CAST(r.RentalID AS TEXT) LIKE ?
           OR c.FirstName LIKE ?
           OR c.LastName LIKE ?
           OR (c.FirstName || ' ' || IFNULL(c.MiddleName, '') || ' ' || c.LastName || ' ' || IFNULL(c.Suffix, '')) LIKE ?
        ORDER BY r.RentalID DESC
    """, (search_pattern,) * 4)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": str(row[0]),
            "rentee": row[1],
            "status": row[2]
        }
        for row in rows
    ]

def get_rental_details(rental_id):
    conn = get_connection()
    check_overdue_rentals(conn)
    cursor = conn.cursor()

    # FIXED: Added d.RentalPrice to the SELECT query so the Daily Rate shows up in the GUI
    cursor.execute("""
        SELECT
            r.RentalID,
            c.CustomerID,
            CASE 
                WHEN c.FirstName IS NULL THEN 'Unknown'
                ELSE c.FirstName || 
                     CASE WHEN c.MiddleName IS NOT NULL AND c.MiddleName != '' THEN ' ' || c.MiddleName ELSE '' END || 
                     ' ' || c.LastName || 
                     CASE WHEN c.Suffix IS NOT NULL AND c.Suffix != '' THEN ' ' || c.Suffix ELSE '' END
            END AS CustomerName,
            c.ContactNumber,
            c.EmailAddress,
            d.DeviceID,
            b.BrandName,
            d.Model,
            d.SerialNumber,
            r.RentalDate,
            r.ReturnDate,
            r.TotalRentalFee,
            r.RentalStatus,
            d.RentalPrice
        FROM Rental r
        LEFT JOIN Customer c ON r.CustomerID = c.CustomerID
        LEFT JOIN Device d ON r.DeviceID = d.DeviceID
        LEFT JOIN Brand b ON d.BrandID = b.BrandID
        WHERE r.RentalID = ?
    """, (rental_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": str(row[0]),
        "customer_id": row[1],
        "rentee": row[2],
        "contact number": row[3],
        "email address": row[4],
        "device_id": row[5],
        "brand": row[6],
        "model": row[7],
        "serial_number": row[8],
        "start_date": row[9],
        "expected_return": row[10],
        "total_fee": row[11],
        "status": row[12],
        "device_price": row[13]
    }


# UPDATE RENTAL ORDER AS COMPLETE
def mark_rental_as_completed(rental_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Rental
            SET RentalStatus = 'Completed'
            WHERE RentalID = ?
        """, (rental_id,))

        # FIXED: Pulled from the correct 'Rental' table instead of a non-existent 'RentalDevice' table
        cursor.execute("""
                UPDATE Device
                SET AvailabilityStatus = 'Available'
                WHERE DeviceID = (
                    SELECT DeviceID
                    FROM Rental
                    WHERE RentalID = ?
                )
            """, (rental_id,))
        
        conn.commit()
        updated = cursor.rowcount > 0
        return updated
    
    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()