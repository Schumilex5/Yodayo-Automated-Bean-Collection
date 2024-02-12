import tkinter as tk
from GUI import UserPasswordGUI


def main_loop():
    root = tk.Tk()  # Define 'root' here
    app = UserPasswordGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main_loop()
