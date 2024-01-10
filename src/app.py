import tkinter as tk
from gui import MainWindow
#python -m PyInstaller --onefile src/app.py
# gonna need to make sure contributor notifications are turned off when downloading and harvesting
def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()