from db.database import get_connection


# RENTAL LISTING FUNCTIONS

def get_all_rentals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
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
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee,
               r.StartRentalDate,
               r.ExpectedReturnDate
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
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
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
    cursor = conn.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute("""
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               r.RentalStatus
        FROM Rental r
        JOIN Customer c
            ON r.CustomerID = c.CustomerID
        WHERE CAST(r.RentalID AS TEXT) LIKE ?
           OR c.FirstName LIKE ?
           OR c.LastName LIKE ?
           OR (c.FirstName || ' ' || c.LastName) LIKE ?
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
    cursor = conn.cursor()

    cursor.execute("""
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
            r.StartRentalDate,
            r.ExpectedReturnDate,
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
    """, (rental_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": str(row[0]),
        "rentee": row[1],
        "contact number": row[2],
        "email address": row[3],
        "region": row[4],
        "city": row[5],
        "barangay": row[6],
        "postal": row[7],
        "street": row[8],
        "birthday": row[9],
        "device_model": row[10],
        "start_date": row[11],
        "expected_return": row[12],
        "total_fee": row[13],
        "status": row[14]
    }




# UPDATE RENTAL ORDER AS COMPLETE
def mark_rental_as_completed(rental_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Rental
        SET RentalStatus = 'Completed'
        WHERE RentalID = ?
    """, (rental_id,))

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated