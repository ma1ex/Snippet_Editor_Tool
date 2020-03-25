# Snippet Editor Tool for CudaText Editor

# Dependencies: base Python library (tkinter, os)

from tkinter import *
import os, base64

# ------------------------------------------------------------------------------

def main():
    root = Tk()
    root.title("Add/Edit Snippet - CudaText")
    
    # App icon
    app_ico_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAPklEQVR42mMYXODPAon/IEyGPEIBMZaQJkFYLUIQmY2O0eWp6wJsNmBiTHkUDrkxRpELhkMsUJ4SKc8LlAMAjSSh9Q+hN1gAAAAASUVORK5CYII="
    # Прямое обращение к Tcl для нестандартной кастомизации виджета PhotoImage
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(data = app_ico_base64))
    
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

    # Scrollbars for a Listbox
    scrollbar_y = Scrollbar(frame_left, width=12)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x = Scrollbar(frame_left, orient=HORIZONTAL, width=12)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    
    # Snippets list
    list_snippet = Listbox(
        frame_left, 
        font=('Arial', 11),
        yscrollcommand = scrollbar_y.set, 
        xscrollcommand = scrollbar_x.set,
        width=20
    )
    list_snippet.pack(side=LEFT, fill=BOTH)
    
    # test data
    for snippet in range(0, 100):
        list_snippet.insert(END, 'Snippet_name_#' + str(snippet))
    
    # Linking scrollbars for a Listbox
    scrollbar_y.config(command = list_snippet.yview)
    scrollbar_x.config(command = list_snippet.xview)
    
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