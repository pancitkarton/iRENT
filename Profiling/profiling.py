# Task 1.1 - Profiling Logic with Database
import sqlite3

users = {}  #call this function in order to create a database and a table for login credentials

conn = sqlite3.connect("iRENT.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Login (
    Login_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT(20) NOT NULL UNIQUE,
    Password TEXT(20) NOT NULL
)
''')
conn.commit()

#Start - Merged code from Garcia and Piamonte
def signup():
  username = input("\nCreate Username: ")
  if username in users:
    print("Username already exists!")
  else:
    password = input("Create Password: ")
    users[username] = password
    confirmpassword = input("Confirm Password: ")

    if confirmpassword == password:
      cursor.execute("INSERT INTO Login (Username, Password) VALUES (?, ?)", (username, password)) #stores the username and password into the database
      conn.commit()
      print("Sign-up successful!")
    else:
      print("Invalid password. Try Again!")

def login():
  username = input("\nEnter Username: ")
  password = input("Enter Password: ")

  cursor.execute("SELECT * FROM Login WHERE Username = ? AND Password = ?", (username, password))
  result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

  if result:
    print("Login successful. Welcome!")
  else:
    print("Invalid username or password. Try Again!")
#End - Merged code from Garcia and Piamonte

def show_users():
  cursor.execute("SELECT Username, Password FROM Login")
  users = cursor.fetchall()

  print("\nRegistered Users:")
  for user in users:
    print("Username:", user[0], "| Password:", user[1]) #displays only stored username, and password

while True:
  choice = input("""
1. Sign Up
2. Login
3. Show all users
4. Exit
Choose an option: """)

  if choice == "1":
    signup()
  elif choice == "2":
    login()
  elif choice == "3":
    show_users()
  elif choice == "4":
    break

  else:
    print("Invalid choice. Try Again!")

conn.close()


# Task 1.1 - Profiling Logic with Tkinter
