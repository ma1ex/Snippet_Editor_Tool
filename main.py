# Snippet Editor Tool for CudaText Editor

# Dependencies: base Python library (tkinter, os)

from tkinter import *
import os, base64

# ------------------------------------------------------------------------------

def main():
    root = Tk()
    root.title("Add/Edit Snippet - CudaText")
    
    # Insert spaces as tabulation
    TAB_WIDTH = 4
    
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
        #width=200,
        text='Snippets list: ', 
        font=('Verdana', 11),
        foreground='#FFD71C',
        background='#333842',
        padx=5, pady=5,
        relief=FLAT
    )
    # MIDDLE Side
    frame_middle = Frame(
        root,
        #width=300,
        background='#333842',
        padx=5, pady=5,
        relief=FLAT
    )
    # RIGHT Side
    frame_right = Frame(
        root,
        background='#333842',
        relief=FLAT
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
    listbox_snippet = Listbox(
        frame_left, 
        width=20,
        font=('Arial', 11),
        yscrollcommand=scrollbar_y.set, 
        xscrollcommand=scrollbar_x.set,
        foreground='#94D7F8',
        background='#16181D',
        relief=FLAT
    )
    listbox_snippet.pack(side=LEFT, fill=BOTH)
    
    # --- test data
    snippets = ['Item_#' + str(i) for i in range(1, 101)]
    for snippet in snippets:
        listbox_snippet.insert(END, 'Snippet_name_' + str(snippet))
    # Count snippets
    frame_left['text'] = frame_left['text'] + ' (' + str(len(snippets)) + ')'
    # /--- test data
    
    # Linking scrollbars for a Listbox
    scrollbar_y.config(command=listbox_snippet.yview)
    scrollbar_x.config(command=listbox_snippet.xview)
    
    # / MIDDLE ----------------------------------------------------------------/
    
    # Buttons
    btn_edit = Button(
        frame_middle, 
        text='Edit >>>', 
        width=10, 
        font=('Verdana', 11), 
        foreground='#E5E5E5', 
        background='#333842', 
        relief=GROOVE 
    )
    btn_edit.pack(side=TOP, pady=20)

    btn_help = Button(
        frame_middle, 
        text='Help?', 
        width=10, 
        font=('Verdana', 11), 
        foreground='#E5E5E5', 
        background='#333842', 
        relief=GROOVE 
    )
    btn_help.pack(side=BOTTOM, pady=5)
    
    # / RIGHT -----------------------------------------------------------------/

    left_top_frame = LabelFrame(
        frame_right,
        text='Snippet name: ', 
        font=('Verdana', 12),
        foreground='#FFD71C',
        background='#333842',
        padx=5, pady=5,
        relief=FLAT
    )
    left_top_frame.pack(side=TOP, fill=X)

    entry_snippet_name = Entry(
        left_top_frame,
        width=60,
        font=('Arial', 12),
        foreground='#FF79C6',
        background='#16181D',
        insertbackground='#FF79C6',
        relief=FLAT
    )
    entry_snippet_name.pack(fill=X)

    left_mid_frame = LabelFrame(
        frame_right,
        text='Snippet code: ', 
        font=('Arial', 12), 
        foreground='#FFD71C',
        background='#333842',
        padx=5, pady=5,
        relief=FLAT
    )
    left_mid_frame.pack(fill=X)

    text_area = Text(
        left_mid_frame,
        width=60,
        height=16,
        font=('Consolas', 12),
        foreground='#F8F8F2',
        background='#16181D',
        insertbackground='#F8F8F2',
        pady=5, padx=5,
        wrap=WORD,
        relief=FLAT
    )
    text_area.pack()
    text_area.bind('<Tab>', lambda event: do_tab(event, widget=text_area, tab_width=TAB_WIDTH))

    left_bottom_frame = Frame(
        frame_right,
        background='#333842', 
        padx=5, pady=5,
        relief=FLAT
    )
    left_bottom_frame.pack(fill=X)

    btn_new = Button(
        left_bottom_frame, 
        text='New', 
        width=15, 
        font=('Verdana', 11), 
        foreground='#F1FA8C', 
        background='#333842', 
        relief=GROOVE 
    )
    btn_new.pack(side=LEFT)

    btn_save = Button(
        left_bottom_frame, 
        text='Save', 
        width=15, 
        font=('Verdana', 11), 
        foreground='#3BDB84', 
        background='#333842', 
        relief=GROOVE 
    )
    btn_save.pack(side=RIGHT)

    # -------------------------------------------------------------------------/
    root.mainloop()

# / FUNCTIONS -----------------------------------------------------------------/

def do_tab(event=None, widget=None, tab_width=4):
    """Replacing tab chars with spaces"""
    widget.insert("insert", " " * tab_width)
    # return 'break' so that the default behavior doesn't happen
    return 'break'



if __name__ == "__main__":
    main()