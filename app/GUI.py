import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from utyl import claim_loop


class UserPasswordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Yo Beans Claimer")
        self.root.geometry("640x480")

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate x and y position for the window to be centered
        x = (screen_width - 640) // 2
        y = (screen_height - 480) // 2

        # Set window position
        self.root.geometry("640x480+{}+{}".format(x, y))

        self.label = tk.Label(root, text="Select a text file:")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.run_button = tk.Button(root, text="Run", command=self.run_program)
        self.run_button.pack(pady=5)

        self.file_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path
            self.label.config(text="Selected file: " + file_path)

    def run_program(self):
        try:
            if self.file_path:
                credential_list = []
                with open(self.file_path, "r") as file:
                    lines = file.readlines()
                    total_lines = len(lines)

                    for i in range(0, total_lines, 3):
                        email = lines[i].strip()
                        password = lines[i+1].strip()
                        credential_list.append((email, password))

                        claim_loop(credential_list)

                    messagebox.showinfo("Program Executed", "Main loop executed successfully!")
            else:
                messagebox.showerror("Error", "Please select a file first.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
