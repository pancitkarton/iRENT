import sqlite3

users = {}  #call this function in order to create a database and a table for login credentials

conn = sqlite3.connect("iRENT.db")
cursor = conn.cursor()

# Create table; VARCHAR is used for no maximum length of characters
cursor.execute("""
CREATE TABLE IF NOT EXISTS Staff (
        StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName VARCHAR NOT NULL,
        MiddleName VARCHAR,
        LastName VARCHAR NOT NULL,
        Suffix VARCHAR,
        ContactNo VARCHAR NOT NULL UNIQUE,
        EmailAdd VARCHAR NOT NULL UNIQUE,
        StaffRole VARCHAR NOT NULL,
        Username VARCHAR NOT NULL UNIQUE,
        Password VARCHAR NOT NULL
)
""")
conn.commit()


def signup():
    first_name = input("Enter First Name: ")
    middle_name = input("Enter Middle Name (Optional): ")
    last_name = input("Enter Last Name: ")
    suffix = input("Enter Suffix (Optional): ")
    contact_no = input("Enter Contact Number: ")
    email_add = input("Enter Email Address: ")
    staff_role = input("Enter Staff Role: ")

    username = input("Create Username: ")

    # Check if username already exists in database
    cursor.execute("SELECT * FROM Staff WHERE Username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists!")

    else:
        password = input("Create Password: ")
        confirm_password = input("Confirm Password: ")

        if confirm_password == password:

            # Insert user into database
            cursor.execute("""
            INSERT INTO Staff
            (FirstName, MiddleName, LastName, Suffix, ContactNo, EmailAdd, StaffRole, Username, Password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                first_name,
                middle_name,
                last_name,
                suffix,
                contact_no,
                email_add,
                staff_role,
                username,
                password
            ))

            conn.commit()
            print("Sign-up successful!")

        else:
            print("Passwords do not match. Try Again!")


def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor.execute("""
    SELECT * FROM Staff
    WHERE Username = ? AND Password = ?
    """, (username, password))

    result = cursor.fetchone()

    # Check if username and password match
    if result:
        print("Login successful. Welcome!")
    else:
        print("Invalid username or password. Try Again!")


def show_users():
    cursor.execute("""
    SELECT FirstName, MiddleName, LastName, Suffix, ContactNo, EmailAdd, StaffRole, Username, Password
    FROM Staff
    """)

    users = cursor.fetchall()

    print("\nRegistered Users:")

    for user in users:
        print("-----------------------------------")
        print("First Name:", user[0])
        print("Middle Name:", user[1])
        print("Last Name:", user[2])
        print("Suffix:", user[3])
        print("Contact No:", user[4])
        print("Email Address:", user[5])
        print("Staff Role:", user[6])
        print("Username:", user[7])
        print("Password:", user[8])


# Main Menu
while True:

    choice = input("""
1. Sign Up
2. Login
3. Show All Users
4. Exit

Choose an option: """)

    if choice == "1":
        signup()

    elif choice == "2":
        login()

    elif choice == "3":
        show_users()

    elif choice == "4":
        print("Program Closed.")
        break

    else:
        print("Invalid choice. Try Again!")

# Close database connection
conn.close() 