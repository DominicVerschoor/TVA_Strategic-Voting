import tkinter as tk
from ui import start_screen

def main():
    root = tk.Tk()
    root.title("Voting System")
    root.geometry("800x600")
    start_screen(root)
    root.mainloop()

if __name__ == "__main__":
    main()