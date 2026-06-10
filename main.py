import tkinter as tk
from ui.gui import App

def main():
    root = tk.Tk()
    root.title("CATIA Drawing Comparator")

    app = App(root)

    root.mainloop()

if __name__ == "__main__":
    main()