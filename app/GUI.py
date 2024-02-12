import ctypes
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from utyl import claim_loop
import atexit

# Specify application is a Windows application
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


class EditPopup:
    def __init__(self, parent, current_values, save_callback):
        self.parent = parent
        self.current_values = current_values
        self.save_callback = save_callback

        self.popup = tk.Toplevel(parent)
        self.popup.title("Edit Entry")

        # Calculate x and y position for the window to be centered
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - 200
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - 100

        self.popup.geometry(f"300x200+{x}+{y}")

        self.email_label = tk.Label(self.popup, text="Email:")
        self.email_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Entry field for email
        self.email_entry = tk.Entry(self.popup, width=50)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.email_entry.insert(0, current_values[0])

        self.password_label = tk.Label(self.popup, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Entry field for password
        self.password_entry = tk.Entry(self.popup, show="*", width=50)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.password_entry.insert(0, current_values[1])

        # Save button
        self.save_button = tk.Button(self.popup, text="Save", command=self.save, width=40)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def save(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            self.save_callback((email, password))
            self.popup.destroy()


class UserPasswordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Yo Beans Claimer")
        self.root.geometry("640x480")

        # Create label widget
        self.label = tk.Label(root, text="")

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate x and y position for the window to be centered
        x = (screen_width - 640) // 2
        y = (screen_height - 480) // 2

        # Set window position
        self.root.geometry("640x480+{}+{}".format(x, y))

        self.select_button = tk.Button(root, text="Select a text file", command=self.select_file, width=40)
        self.select_button.pack(pady=5)

        self.run_button = tk.Button(root, text="Run", command=self.run_program, width=40)
        self.run_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_program, width=40)
        self.stop_button.pack(pady=5)
        self.stop_button.configure(state='disabled')  # Initially disabled

        self.file_path = None
        self.is_running = False
        self.stop_event = None

        # Create a Treeview widget to display email and password data
        self.tree = ttk.Treeview(root, columns=("Email", "Password"), show="headings")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Password", text="Password")
        self.tree.pack(expand=True, fill="both")

        # Entry fields for adding new data
        self.email_entry = tk.Entry(root, width=70)
        self.email_entry.pack()
        self.password_entry = tk.Entry(root, show="*", width=70)
        self.password_entry.pack()

        # Button to add new row
        self.add_button = tk.Button(root, text="Add", command=self.add_row, width=40)
        self.add_button.pack()

        # Button to remove row
        self.remove_button = tk.Button(root, text="Remove", command=self.remove_row, state="disabled", width=40)
        self.remove_button.pack()

        # Button to edit row
        self.edit_button = tk.Button(root, text="Edit", command=self.edit_row, state="disabled", width=40)
        self.edit_button.pack()

        # Bind selection event to enable/disable remove and edit buttons
        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)

        # Initialize data_list attribute
        self.data_list = []

        # Register save_data_on_exit function to be called when the program exits
        atexit.register(self.save_data_on_exit)

    def on_item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.remove_button.configure(state="normal")
            self.edit_button.configure(state="normal")
        else:
            self.remove_button.configure(state="disabled")
            self.edit_button.configure(state="disabled")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path  # Update file path attribute
            self.label.config(text="Selected file: " + file_path)
            self.populate_list_from_file(file_path)  # Add this line to populate the list

    def populate_list_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                for i in range(0, len(lines), 3):
                    email = lines[i].strip()
                    password = lines[i + 1].strip()
                    self.tree.insert("", "end", values=(email, password))
                    self.data_list.append((email, password))  # Add the new entry to data_list
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_program(self):
        if not self.is_running:
            try:
                if self.data_list:
                    self.is_running = True
                    self.stop_button.configure(state='normal')  # Enable stop button

                    # Start the claim_loop function in a separate thread
                    self.stop_event = threading.Event()
                    self.process_thread = threading.Thread(
                        target=claim_loop, args=(self.data_list, self.stop_event)
                    )
                    self.process_thread.start()
                else:
                    messagebox.showerror("Error", "No data available. Please add data before running.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.stop_program()

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
            self.data_list.append((email, password))  # Add the new entry to data_list
            self.tree.insert("", "end", values=(email, password))
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def remove_row(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            # Get the values of the selected item
            values = self.tree.item(item, "values")
            if values:
                # Find the corresponding entry in self.data_list
                for entry in self.data_list:
                    if entry[0] == values[0] and entry[1] == values[1]:
                        # Remove the entry from self.data_list
                        self.data_list.remove(entry)
                        break  # Exit loop once the entry is found and removed
            # Delete the selected item from the treeview
            self.tree.delete(item)

    def edit_row(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            current_values = self.tree.item(item, "values")
            if current_values:
                # Find the corresponding entry in self.data_list
                for i, entry in enumerate(self.data_list):
                    if entry[0] == current_values[0] and entry[1] == current_values[1]:
                        # Open the edit popup with the current values and update function
                        popup = EditPopup(self.root, current_values, lambda new_values: self.update_row(new_values, item, i))
                        break  # Exit loop once the entry is found

    def update_row(self, new_values, item, index):
        # Update the entry in self.data_list with the new values
        self.data_list[index] = new_values
        # Update the treeview with the new values
        self.tree.item(item, values=new_values)

    def save_data_on_exit(self):
        # Save the data list to a text file before the program exits
        file_path = "data.txt"
        try:
            fp = open('data.txt', 'w')
            fp.close()
            with open(file_path, "r+") as file:
                file.truncate(0)  # Clear the file contents
                for email, password in self.data_list:
                    file.write(f"{email}\n{password}\n\n")
        except Exception as e:
            print(f"Error saving data: {e}")
