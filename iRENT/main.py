import tkinter as tk
from gui.auth import AuthApp
from db.database import initialize_db

def main():
    initialize_db()

    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()