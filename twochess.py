import tkinter as tk
from twochess.menu import Menu

def main():
    root = tk.Tk()
    root.title("Chess")
    root.geometry("1300x800")
    root.resizable(False, False)

    menu = Menu(root)
    root.mainloop()

if __name__ == '__main__':
    main()