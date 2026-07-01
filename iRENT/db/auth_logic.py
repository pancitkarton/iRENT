# db and functions for login
import sqlite3
import os
import bcrypt

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
    Suffix TEXT NOT NULL,
    ContactNo TEXT NOT NULL UNIQUE,
    EmailAdd TEXT NOT NULL UNIQUE,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
)
""")
conn.commit()

def hashed_pass(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


#Log-in function
def login(username, password):
        if not username or not password:
            return "empty"
        
        username_lower = username.lower()

        cursor.execute("SELECT StaffID, Password FROM Staff WHERE Username = ?", (username_lower,))
        result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

        if result and verify_password(password, result[1]):
            return {"status": "success", "staff_id": result[0]}
        
        else:
            return {"status": "fail"}


#Sign-up function
def signup(first_name, middle_name, last_name, suffix, contact_no, email_add, username, password, confirm):

    if not username or not password:
        return "empty"

    # Check if password matches
    if password != confirm:
         return "mismatch"
    
    username_lower = username.lower()

    # Check if username exists
    cursor.execute(
        "SELECT * FROM Staff WHERE Username = ?",
        (username_lower,)
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
    
    hashed_pw = hashed_pass(password)


# Inserts user into database
    cursor.execute("""
        INSERT INTO Staff
        (
            FirstName,
            MiddleName,
            LastName,
            Suffix,
            ContactNo,
            EmailAdd,
            Username,
            Password
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        first_name,
        middle_name,
        last_name,
        suffix,
        contact_no,
        email_add,
        username_lower,
        hashed_pw
    ))

    conn.commit()

    return "success"