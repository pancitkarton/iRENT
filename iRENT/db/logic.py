#db and functions
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "iRENT.db")

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Staff (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    MiddleName TEXT,
    LastName TEXT NOT NULL,
    ContactNo TEXT NOT NULL UNIQUE,
    EmailAdd TEXT NOT NULL UNIQUE,
    StaffRole TEXT NOT NULL,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
)
""")
conn.commit()


#Log-in function
def login(username, password):
        if not username or not password:
            return "empty"
        
        cursor.execute("SELECT * FROM Staff WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

        if result:
             return "success"
        else:
             return "fail"


#Sign-up function
def signup(first_name, middle_name, last_name, contact_no, email_add, staff_role, username, password, confirm):

    if not username or not password:
        return "empty"

    # Check if password matches
    if password != confirm:
         return "mismatch"

    # Check if username exists
    cursor.execute(
        "SELECT * FROM Staff WHERE Username = ?",
        (username,)
    )
    if cursor.fetchone():
        return "exists"

    # Check if contact number already exists
    cursor.execute(
        "SELECT * FROM Staff WHERE ContactNo = ?",
        (contact_no,)
    )
    if cursor.fetchone():
        return "contact_exists"

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM Staff WHERE EmailAdd = ?",
        (email_add,)
    )
    if cursor.fetchone():
        return "email_exists"


# Inserts user into database
    cursor.execute("""
        INSERT INTO Staff
        (
            FirstName,
            MiddleName,
            LastName,
            ContactNo,
            EmailAdd,
            StaffRole,
            Username,
            Password
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        first_name, 
        middle_name, 
        last_name, 
        contact_no, 
        email_add, 
        staff_role, 
        username, 
        password
    ))

    conn.commit()

    return "success"
