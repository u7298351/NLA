import tkinter as tk
from tkinter import messagebox

# pyinstaller app.py--onefile --name harvestAutomater

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

        # create entry field
        self.iteration_entry = tk.Entry(self)
        iteration_label = tk.Label(self, text="Enter Max Iterations:")

        # organise items
        scraper_header.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        html_harvester.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        iteration_label.grid(row=2, column=0, sticky="w", padx=10)
        self.iteration_entry.grid(row=2, column=1, sticky="w")
        start_button.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    def activate_html_harvester(self):
        # Placeholder for HTML Harvester activation code
        pass

    def start_scraping(self):
        try:
            max_iterations = int(self.iteration_entry.get())
            if max_iterations <= 0:
                raise ValueError("The number of iterations should be greater than 0.")
            # Call scraper_main here with max_iterations
            # scraper_main(max_iterations)
            messagebox.showinfo("Success", "Scraping started with {} iterations.".format(max_iterations))
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input for max iterations: {}".format(e))

# Example usage
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
