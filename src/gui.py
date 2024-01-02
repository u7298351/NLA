import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("NLA Automation Tools")
        self.geometry("800x600")
        self.resizable(width=True, height=True)

        # create buttons
        html_harvester = tk.button(self, text = "HTML Harvester", command = self.activate_html_harvester)

        # create headers
        scraper_header = tk.Label(self, text = "Scraper Tools", font=("Arial", 12, "bold"))

        # organise items
        scraper_header.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 5)
        html_harvester.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 5)

    def activate_html_harvester(self):
        pass