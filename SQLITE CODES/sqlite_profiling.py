# Database for Profiling
import sqlite3

users = {}  #call this function in order to create a database and a table for login credentials

conn = sqlite3.connect("iRENT.db")
cursor = conn.cursor()

# Create table; VARCHAR is used for no maximum length of characters
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR NOT NULL UNIQUE,
        Password VARCHAR NOT NULL,
        FirstName VARCHAR NOT NULL,
        LastName VARCHAR NOT NULL,
        HomeAddress VARCHAR NOT NULL,
        ContactNumber VARCHAR NOT NULL UNIQUE
)
""")
conn.commit()


def signup():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    contact_no = input("Enter Contact Number: ")
    home_ad = input("Enter Home Address: ")

    username = input("Create Username: ")

    # Check if username already exists in database
    cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists!")

    else:
        password = input("Create Password: ")
        confirm_password = input("Confirm Password: ")

        if confirm_password == password:

            # Insert user into database
            cursor.execute("""
            INSERT INTO Users
            (Username, Password, FirstName, LastName, HomeAddress, ContactNumber)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username,
                password,
                first_name,
                last_name,
                contact_no,
                home_ad
            ))

            conn.commit()
            print("Sign-up successful!")

        else:
            print("Passwords do not match. Try Again!")


def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor.execute("""
    SELECT * FROM Users
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
    SELECT Username, Password, FirstName, LastName,
           ContactNumber, HomeAddress
    FROM Users
    """)

    users = cursor.fetchall()

    print("\nRegistered Users:")

    for user in users:
        print("-----------------------------------")
        print("First Name:", user[2])
        print("Last Name:", user[3])
        print("Contact No:", user[4])
        print("Home Address:", user[5])
        print("Username:", user[0])
        print("Password:", user[1])


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