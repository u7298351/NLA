import tkinter as tk
from tkinter import filedialog, messagebox

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("NLA Automation Tools")
        self.geometry("800x600")
        self.resizable(width=True, height=True)

        # create headers
        scraper_header = tk.Label(self, text="Scraper Tools", font=("Arial", 12, "bold"))

        # create buttons
        html_harvester = tk.Button(self, text="HTML Harvester", command=self.activate_html_harvester)
        start_button = tk.Button(self, text="Start Scraping", command=self.start_scraping)
        self.select_file_button = tk.Button(self, text="Select CSV File", command=self.select_csv_file)

        # create entry field
        self.iteration_entry = tk.Entry(self)
        iteration_label = tk.Label(self, text="Enter Max Iterations:")

        # organize items
        scraper_header.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        html_harvester.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        iteration_label.grid(row=2, column=0, sticky="w", padx=10)
        self.iteration_entry.grid(row=2, column=1, sticky="w")
        start_button.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.select_file_button.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Label to show selected file path
        self.selected_file_label = tk.Label(self, text="")
        self.selected_file_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Variable to store selected file path
        self.selected_file_path = ""

    def activate_html_harvester(self):
        # Placeholder for HTML Harvester activation code
        pass

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

            # Check if a file has been selected
            if not self.selected_file_path:
                messagebox.showerror("Error", "Please select a CSV file to proceed.")
                return

            # Call scraper_main here with max_iterations and the selected file path
            # scraper_main(max_iterations, self.selected_file_path)
            messagebox.showinfo("Success", f"Scraping started with {max_iterations} iterations on file: {self.selected_file_path}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for max iterations: {e}")

# Example usage
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
