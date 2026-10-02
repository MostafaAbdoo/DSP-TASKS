import tkinter as tk
from gui.main_window import DSPApp


def main():
    root = tk.Tk()
    app = DSPApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()