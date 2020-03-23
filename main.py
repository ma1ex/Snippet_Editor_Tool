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
    
    # LEFT Side
    frame_left = LabelFrame(
        root,
        width=200,
        text='Snippets:', 
        font=('Verdana', 11),
        padx=5, pady=5
    )
    # MIDDLE Side
    frame_middle = Frame(
        root,
        width=300,
        padx=5, pady=5
    )
    # RIGHT Side
    frame_right = Frame(
        root
    )

    frame_left.pack(side=LEFT, fill=Y)
    frame_middle.pack(side=LEFT, fill=Y)
    frame_right.pack(side=LEFT, fill=BOTH)
    
    # / LEFT ------------------------------------------------------------------/

    # Snippets list
    list_snippet = Listbox(
        frame_left, 
        font=('Arial', 11),
        width=20
    )
    list_snippet.pack(side=LEFT, fill=BOTH)
    
    # / MIDDLE ----------------------------------------------------------------/
    
    # Buttons
    btn_edit = Button(
        frame_middle, 
        text='Edit', 
        width=10, 
        font=('Verdana', 11) 
    )
    btn_edit.pack(side=TOP, pady=20)

    btn_help = Button(
        frame_middle, 
        text='Help?', 
        width=10, 
        font=('Verdana', 11) 
    )
    btn_help.pack(side=BOTTOM, pady=5)
    
    # / RIGHT -----------------------------------------------------------------/

    l_top_frame = LabelFrame(
        frame_right,
        text='Name: ', 
        font=('Verdana', 12),
        padx=5, pady=5
    )
    l_top_frame.pack(side=TOP, fill=X)

    entry_snippet_name = Entry(
        l_top_frame,
        font=('Arial', 12),
        width=60
    )
    entry_snippet_name.pack(fill=X)

    l_mid_frame = LabelFrame(
        frame_right,
        text='Code: ', 
        font=('Arial', 12)
    )
    l_mid_frame.pack(fill=X)

    text_area = Text(
        l_mid_frame,
        width=60,
        height=17,
        font=('Consolas', 12)
    )
    text_area.pack()

    l_bottom_frame = Frame(
        frame_right,
        padx=5, pady=5
    )
    l_bottom_frame.pack(fill=X)

    btn_new = Button(
        l_bottom_frame, 
        text='New', 
        width=15, 
        font=('Verdana', 11) 
    )
    btn_new.pack(side=LEFT)

    btn_save = Button(
        l_bottom_frame, 
        text='Save', 
        width=15, 
        font=('Verdana', 11) 
    )
    btn_save.pack(side=RIGHT)

    # -------------------------------------------------------------------------/
    root.mainloop()


if __name__ == "__main__": main()