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
            "start_date": f"{row[5]}/{row[6]}/{row[7]}",
            "expected_return": f"{row[8]}/{row[9]}/{row[10]}"
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
        "start_date": f"{row[11]}/{row[12]}/{row[13]}",
        "expected_return": f"{row[14]}/{row[15]}/{row[16]}",
        "total_fee": row[17],
        "status": row[18]
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