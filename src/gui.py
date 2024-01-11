import tkinter as tk
from tkinter import filedialog, messagebox
# Import your script here, replace 'your_script' with the actual file name
from functions import scraper_main 

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("NLA Automation Tools")
        self.geometry("800x600")
        self.resizable(width=True, height=True)

        # Create headers
        scraper_header = tk.Label(self, text="Scraper Tools", font=("Arial", 12, "bold"))

        # Create buttons
        self.select_file_button = tk.Button(self, text="Select CSV File", command=self.select_csv_file)
        start_button = tk.Button(self, text="Start Scraping", command=self.start_scraping)

        # Create entry field
        self.iteration_entry = tk.Entry(self)
        iteration_label = tk.Label(self, text="Enter Max Iterations:")

        # Output text area for messages
        self.output_text = tk.Text(self, height=10)
        self.output_text.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Organize items
        scraper_header.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        iteration_label.grid(row=2, column=0, sticky="w", padx=10)
        self.iteration_entry.grid(row=2, column=1, sticky="w")
        start_button.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.select_file_button.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Label to show selected file path
        self.selected_file_label = tk.Label(self, text="")
        self.selected_file_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Variable to store selected file path
        self.selected_file_path = ""


    def select_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_label.config(text=f"Selected File: {file_path}")

    def start_scraping(self):
        try:
            max_iterations = int(self.iteration_entry.get())
            if max_iterations <= 0:
                raise ValueError("The number of iterations should be greater than 0.")

            if not self.selected_file_path:
                messagebox.showerror("Error", "Please select a CSV file to proceed.")
                return

            # Call scraper_main only when this method is triggered
            scraper_main(max_iterations, self.selected_file_path, self.update_output)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for max iterations: {e}")

    def update_output(self, message):
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()