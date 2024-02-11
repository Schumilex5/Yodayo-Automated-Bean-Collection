import ctypes
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from utyl import claim_loop
import threading

# Specify application is a Windows application
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)



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

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_program)
        self.stop_button.pack(pady=5)
        self.stop_button.configure(state='disabled')  # Initially disabled

        self.file_path = None
        self.is_running = False
        self.stop_event = None

        # Create a Treeview widget to display email and password data
        self.tree = tk.ttk.Treeview(root, columns=("Email", "Password"), show="headings")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Password", text="Password")
        self.tree.pack(expand=True, fill="both")

        # Entry fields for adding new data
        self.email_label = tk.Label(root, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Button to add new row
        self.add_button = tk.Button(root, text="Add", command=self.add_row, width=20)
        self.add_button.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path  # Update file path attribute
            self.label.config(text="Selected file: " + file_path)

    def run_program(self):
        if not self.is_running:
            try:
                credential_list = []
                if self.file_path:
                    with open(self.file_path, "r") as file:
                        lines = file.readlines()
                        total_lines = len(lines)

                        for i in range(0, total_lines, 3):
                            email = lines[i].strip()
                            password = lines[i+1].strip()
                            credential_list.append((email, password))
                else:
                    # Get credentials from Entry fields
                    email = self.email_entry.get()
                    password = self.password_entry.get()
                    if email and password:
                        credential_list.append((email, password))

                if credential_list:
                    self.is_running = True
                    self.stop_button.configure(state='normal')  # Enable stop button

                    # Display data in Treeview widget
                    for email, password in credential_list:
                        self.tree.insert("", "end", values=(email, password))

                    # Start the claim_loop function in a separate thread
                    self.stop_event = threading.Event()
                    self.process_thread = threading.Thread(
                        target=claim_loop, args=(credential_list, self.stop_event)
                    )
                    self.process_thread.start()
                else:
                    messagebox.showerror("Error", "Please provide credentials either by selecting a file or manually entering them.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def stop_program(self):
        if self.is_running and self.stop_event is not None:
            # Set the stop event to signal the claim_loop function to stop
            self.stop_event.set()
            # Wait for the thread to complete
            self.process_thread.join()
            self.is_running = False
            messagebox.showinfo("Program Stopped", "The program has been stopped.")
            self.stop_button.configure(state='disabled')  # Disable stop button

    def add_row(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            self.tree.insert("", "end", values=(email, password))
            # Clear entry fields after adding the row
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


