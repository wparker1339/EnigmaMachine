"""Main routine to run the simplified Enigma Machine."""
import tkinter as tk

from enigma_ui.enigma_ui import EnigmaUI

def main():
    root = tk.Tk()
    _ = EnigmaUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
