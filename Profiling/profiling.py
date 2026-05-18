users = {}

def signup():
  username = input("Create a username: ")
  if username in users:
    print("Username already exists!")
  else:
    password = input("Create a password: ")
    users[username] = password
    confirmpassword = input("Confirm password: ")
    if confirmpassword == password:
      print("Sign-up successful!")
    else:
      print("Wrong password!")

def login():
  username = input("Enter username: ")
  password = input("Enter password: ")

  if username in users and users[username] == password:
    print("Login successful! Welcome back.")

  else:
    print("Invalid username or password.")

while True:
  choice = input("\n1. Sign Up\n2. Login\n3. Show all users\n4. Exit\n Choose an option: ")
  if choice == "1":
    signup()
  elif choice == "2":
    login()
  elif choice == "3":
    print(users)
  elif choice == "4":
    break
  else:
    print("Invalid choice.")