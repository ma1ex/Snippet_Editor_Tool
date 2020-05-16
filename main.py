
import os
import tkinter as tk


class MainFrame(tk.Frame):
    """
    Main Layout with Widgets
    """

    def __init__(self, root):
        super().__init__(root)

        # App icon
        self.app_ico_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAPklEQVR42mMYXODPAon/IEyGPEIBMZaQJkFYLUIQmY2O0eWp6wJsNmBiTHkUDrkxRpELhkMsUJ4SKc8LlAMAjSSh9Q+hN1gAAAAASUVORK5CYII="
        self.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=self.app_ico_base64))

        # Directory for scan snippets
        self.PATH_SNIPPETS = 'test_data/data/snippets/ma1ex.Html/'
        # Insert spaces as tabulation
        self.TAB_WIDTH = 4

        self.init_main()

    def init_main(self):
        # LEFT Side
        frame_left = tk.LabelFrame(
            text='Snippets list: ',
            font=('Verdana', 11),
            foreground='#FFD71C',
            background='#333842',
            padx=5, pady=5,
            relief=tk.FLAT
        )
        # MIDDLE Side
        frame_middle = tk.Frame(
            background='#333842',
            padx=5, pady=5,
            relief=tk.FLAT
        )
        # RIGHT Side
        frame_right = tk.Frame(
            background='#333842',
            relief=tk.FLAT
        )

        frame_left.pack(side=tk.LEFT, fill=tk.Y)
        frame_middle.pack(side=tk.LEFT, fill=tk.Y)
        frame_right.pack(side=tk.LEFT, fill=tk.BOTH)

        # / LEFT ------------------------------------------------------------------/

        # Scrollbars for a Listbox
        scrollbar_y = tk.Scrollbar(frame_left, width=12)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(frame_left, orient=tk.HORIZONTAL, width=12)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Snippets list
        listbox_snippet = tk.Listbox(
            frame_left,
            width=20,
            font=('Arial', 11),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            foreground='#94D7F8',
            background='#16181D',
            relief=tk.FLAT
        )
        listbox_snippet.pack(side=tk.LEFT, fill=tk.BOTH)

        snippets = self.__scan_dir(self.PATH_SNIPPETS)
        for key, value in snippets.items():
            listbox_snippet.insert(tk.END, key.replace('.synw-snippet', ''))

        # Count snippets
        frame_left['text'] = frame_left['text'] + ' (' + str(len(snippets)) + ')'

        # Linking scrollbars for a Listbox
        scrollbar_y.config(command=listbox_snippet.yview)
        scrollbar_x.config(command=listbox_snippet.xview)

        # / MIDDLE ----------------------------------------------------------------/

        # Buttons
        btn_edit = tk.Button(
            frame_middle,
            text='Edit >>>',
            width=10,
            font=('Verdana', 11),
            foreground='#E5E5E5',
            background='#333842',
            relief=tk.GROOVE
        )
        btn_edit.pack(side=tk.TOP, pady=20)

        btn_help = tk.Button(
            frame_middle,
            text='Help?',
            width=10,
            font=('Verdana', 11),
            foreground='#E5E5E5',
            background='#333842',
            relief=tk.GROOVE,
            command=self.__open_help
        )
        btn_help.pack(side=tk.BOTTOM, pady=5)

        # / RIGHT -----------------------------------------------------------------/

        left_top_frame = tk.LabelFrame(
            frame_right,
            text='Snippet name: ',
            font=('Verdana', 12),
            foreground='#FFD71C',
            background='#333842',
            padx=5, pady=5,
            relief=tk.FLAT
        )
        left_top_frame.pack(side=tk.TOP, fill=tk.X)

        entry_snippet_name = tk.Entry(
            left_top_frame,
            width=60,
            font=('Arial', 12),
            foreground='#FF79C6',
            background='#16181D',
            insertbackground='#FF79C6',
            relief=tk.FLAT
        )
        entry_snippet_name.pack(fill=tk.X)

        left_mid_frame = tk.LabelFrame(
            frame_right,
            text='Snippet code: ',
            font=('Arial', 12),
            foreground='#FFD71C',
            background='#333842',
            padx=5, pady=5,
            relief=tk.FLAT
        )
        left_mid_frame.pack(fill=tk.X)

        text_area = tk.Text(
            left_mid_frame,
            width=60,
            height=16,
            font=('Consolas', 12),
            foreground='#F8F8F2',
            background='#16181D',
            insertbackground='#F8F8F2',
            pady=5, padx=5,
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        text_area.pack()
        text_area.bind('<Tab>', lambda event: self.__do_tab(event, widget=text_area, tab_width=self.TAB_WIDTH))

        left_bottom_frame = tk.Frame(
            frame_right,
            background='#333842',
            padx=5, pady=5,
            relief=tk.FLAT
        )
        left_bottom_frame.pack(fill=tk.X)

        btn_new = tk.Button(
            left_bottom_frame,
            text='New',
            width=15,
            font=('Verdana', 11),
            foreground='#F1FA8C',
            background='#333842',
            relief=tk.GROOVE
        )
        btn_new.pack(side=tk.LEFT)

        btn_save = tk.Button(
            left_bottom_frame,
            text='Save',
            width=15,
            font=('Verdana', 11),
            foreground='#3BDB84',
            background='#333842',
            relief=tk.GROOVE
        )
        btn_save.pack(side=tk.RIGHT)

    def __scan_dir(self, path='data/snippets/'):
        """
        Scan snippets directory

        Default path - root app dir - 'data/snippets/'
        """

        folders = []  # List dirs, subdirs and files
        filtered = {}  # Snippet names without extension

        if os.path.exists(path) and os.path.isdir(path):
            for i in os.walk(path):
                folders.append(i)

            for files in folders[0][2]:
                if files.endswith('.synw-snippet'):
                    filtered[files] = folders[0][0] + '/' + files

        return filtered

    def __do_tab(self, event=None, widget=None, tab_width=4):
        """Replacing tab chars with spaces"""

        widget.insert("insert", " " * tab_width)
        # return 'break' so that the default behavior doesn't happen
        return 'break'

    def __open_help(self):
        Child(app_icon=self.app_ico_base64)


class Child(tk.Toplevel):
    """
    Child Window
    """

    def __init__(self, app_icon=None):
        super().__init__(root)
        if app_icon is not None:
            self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(data=app_icon))

        self.init_child()

    def init_child(self):
        self.title('Snippet Syntax Help')
        self.geometry('450x250+500+200')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()









if __name__ == '__main__':
    root = tk.Tk()
    root.title('Add/Edit Snippet - CudaText')
    root.geometry('800x450+500+200')
    root.resizable(False, False)
    app = MainFrame(root)
    app.pack()


    root.mainloop()