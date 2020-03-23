# Snippet Editor Tool for CudaText Editor

# Dependencies: base Python library (tkinter, os)

from tkinter import *
import os

# ------------------------------------------------------------------------------

def main():
    root = Tk()
    root.title("Add/Edit Snippet - CudaText")
    
    # App icon
    app_icon = os.path.join(os.path.dirname(__file__), 'res/app_ico.ico')
    root.iconbitmap(app_icon)
    
    # Window dimensions: Width х Height + X-pos + Y-pos
    w = root.winfo_screenwidth() # current screen width
    h = root.winfo_screenheight() # current screen height
    w = w // 2 # screen center
    h = h // 2 
    w = w - 300 # offset fron the center
    h = h - 300
    root.geometry('800x450+{}+{}'.format(w, h))
    root.resizable(False, False) # prevent window resizing


    # -------------------------------------------------------------------------/
    root.mainloop()


if __name__ == "__main__": main()