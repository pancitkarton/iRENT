from db.database import get_connection

conn = get_connection()
cursor = conn.cursor()


def get_all_rentals(conn):
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
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
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
        WHERE r.RentalStatus = ?
        ORDER BY r.RentalID DESC
    ''', (status,))

    return cursor.fetchall()


def search_rentals(conn, search_term):
    cursor = conn.cursor()
    search_pattern = f"%{search_term}%"

    cursor.execute('''
        SELECT r.RentalID,
               c.FirstName || ' ' || c.LastName AS CustomerName,
               c.ContactNumber,
               r.RentalStatus,
               r.TotalRentalFee
        FROM Rental r
        JOIN Customer c 
            ON r.CustomerID = c.CustomerID
        WHERE CAST(r.RentalID AS TEXT) LIKE ?
           OR c.FirstName LIKE ?
           OR c.LastName LIKE ?
           OR (c.FirstName || ' ' || c.LastName) LIKE ?
        ORDER BY r.RentalID DESC
    ''', (search_pattern,) * 4)

    return cursor.fetchall()


def get_rental_details(conn, rental_id):
    cursor = conn.cursor()
    cursor.execute('''
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
    ''', (rental_id,))
    
    return cursor.fetchall()


def mark_rental_as_completed(conn, rental_id):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Rental
        SET RentalStatus = 'Completed'
        WHERE RentalID = ?
    ''', (rental_id,))
    
    conn.commit()
    
    return cursor.rowcount > 0