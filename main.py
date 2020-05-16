import json
import os
import re
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
        root.geometry('800x450+500+200')
        root.resizable(False, False)

        # App config
        self.__config = self.load_config()

        # Widgets
        # --/--

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

        # / LEFT --------------------------------------------------------------/

        # Scrollbars for a Listbox
        scrollbar_y = tk.Scrollbar(frame_left, width=12)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(frame_left, orient=tk.HORIZONTAL, width=12)
        # scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Snippets list
        listbox_snippet = tk.Listbox(
            frame_left,
            width=20,
            font=('Arial', 11),
            selectbackground='#643200',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            foreground='#94D7F8',
            background='#16181D',
            relief=tk.FLAT
        )
        listbox_snippet.pack(side=tk.LEFT, fill=tk.BOTH)

        snippets = self.__scan_dir(self.__config.get('path_snippets'))
        for key, value in snippets.items():
            listbox_snippet.insert(tk.END, key.replace('.synw-snippet', ''))

        # Count snippets
        frame_left['text'] = frame_left['text'] + ' (' + str(len(snippets)) + ')'

        # Linking scrollbars for a Listbox
        scrollbar_y.config(command=listbox_snippet.yview)
        scrollbar_x.config(command=listbox_snippet.xview)

        # / MIDDLE ------------------------------------------------------------/

        # Buttons
        btn_edit = tk.Button(
            frame_middle,
            text='Edit >>>',
            width=10,
            font=('Verdana', 11),
            foreground='#E5E5E5',
            background='#333842',
            relief=tk.GROOVE,
            command=lambda: self.__edit_snippet(widget=listbox_snippet,
                                                dict_snippets=snippets,
                                                entry_widget=entry_snippet_name,
                                                text_widget=text_area)
        )
        btn_edit.pack(side=tk.TOP, pady=20)

        # Editing selected snippet on double-click
        listbox_snippet.bind('<Double-Button-1>', lambda event: self.__edit_snippet(
            event, widget=listbox_snippet, dict_snippets=snippets,
            entry_widget=entry_snippet_name, text_widget=text_area))

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

        # / RIGHT -------------------------------------------------------------/

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
        text_area.bind('<Tab>', lambda event: self.__do_tab(event, widget=text_area,
                                                            tab_width=self.__config.get('tab_width')))

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
            relief=tk.GROOVE,
            command=lambda: self.__new_snippet(widget_name=entry_snippet_name,
                                               widget_text=text_area)
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

    def __edit_snippet(self, *args, **kwargs):
        """
        Edit snippet

        :param args: event=None
        :param kwargs: widget=None, dict_snippets=None, entry_widget=None, text_widget=None
        :return:
        """

        # Индекс выделенного пункта в Listbox - первое значение кортежа
        index = kwargs['widget'].curselection()[0]

        # Значение выделенного пункта в Listbox
        name = kwargs['widget'].get(index)

        # Поиск ключа в словаре, где значение - путь к файлу сниппета; None - если нету
        snippet = kwargs['dict_snippets'].get(name + '.synw-snippet')

        # Вставка имени редактируемого сниппета
        kwargs['entry_widget'].delete(0, tk.END)
        kwargs['entry_widget'].insert(0, name)
        # Если файл существует, открываем на редактирование
        if os.path.exists(snippet) and os.path.isfile(snippet):
            f = open(snippet, 'r')
            f_read = f.read()
            kwargs['text_widget'].delete(1.0, tk.END)
            kwargs['text_widget'].insert(1.0, f_read)
            f.close()

    def __new_snippet(self, widget_name=None, widget_text=None):
        # start_data = widget_name.get()
        # print(start_data)
        widget_name.delete(0, tk.END)
        widget_text.delete(1.0, tk.END)
        widget_name.focus_set()

    def __do_tab(self, *args, **kwargs):
        """
        Replacing tab chars with spaces

        :param args: event=None
        :param kwargs: widget=None, tab_width=4
        :return:
        """

        kwargs['widget'].insert("insert", " " * kwargs['tab_width'])
        # return 'break' so that the default behavior doesn't happen
        return 'break'

    def __open_help(self):
        Child(app_icon=self.app_ico_base64)

    def load_config(self, file='config.json'):
        """
        Open and Read JSON App Config
        :param file:
        :return:
        """

        if os.path.exists(file) and os.path.isfile(file):
            f = open(file, 'r', encoding='utf-8')
            raw = f.read()
            f.close()
            parsed = re.sub(r'\n^\s*//.+$', '', raw, flags=re.MULTILINE)
            # print(parsed)
            return json.loads(parsed)

            # with open(file, 'r', encoding='utf-8') as read_file:
            # parsed = re.sub(r'\n^\s*//.+$', '', read_file, flags=re.MULTILINE)
            # return json.load(read_file)
        else:
            # Defaul settings
            return {
                "path_snippets": ".",
                "tab_width": 4
            }


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
    app = MainFrame(root)
    app.pack()
    root.mainloop()
