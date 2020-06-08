import json
import os
import re
import tkinter as tk
from tkinter import ttk
import SnippetEditor
from IconsBase64 import Icons


class App:

    def __init__(self):

        # App config
        # self.__config = self.load_config()

        self.root = tk.Tk()
        self.root.title('Add/Edit Snippet - CudaText')
        self.icons = Icons()
        # App icon
        self.app_ico = self.icons.snippet_orange
        self.root.call('wm', 'iconphoto', self.root._w, self.app_ico)

        win_width = 800
        win_heght = 475
        x = int((self.root.winfo_screenwidth() - win_width) / 2)
        y = int((self.root.winfo_screenheight() - win_heght) / 2)
        self.root.wm_geometry(f'800x450+{x}+{y}')
        # self.root.resizable(False, False)
        self.root.minsize(width=win_width, height=win_heght)
        self.root.maxsize(width=1200, height=700)

        # Theme Styling --------------------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # TreeFileManager ------------------------------------------------------
        self.tree = SnippetEditor.TreeFileManager(self.root)
        self.tree.width_tree = 250
        self.tree.path = os.path.join(os.getcwd(), 'test_data')

        self.tree.folder_icon = self.icons.folder_orange
        self.tree.file_icon = self.icons.file_blue
        self.tree.folder_style = {'foreground': '#321900', 'font': ('Verdana', 12)}
        self.tree.file_style = {'foreground': '#18313F', 'font': ('Verdana', 11)}

        self.tree.show_toolbar = True
        self.tree.pack(side='left', fill='both')
        self.tree.create()

        # ----------------------------------------------------------------------

        self.cancel_icon = self.icons.cancel
        self.save_icon = self.icons.save
        self.new_icon = self.icons.add
        # self.file_icon = self.icons.file_blue
        self.help_icon = self.icons.help_blue

        # Notebook -------------------------------------------------------------
        self.notebook = ttk.Notebook(self.root, padding=5)
        self.notebook.pack(fill='both', expand='yes')

        self.tab1_frame = tk.Frame(self.root)
        self.tab2_frame = tk.Frame(self.root)

        frame_label_snippet = tk.LabelFrame(
            self.tab1_frame,
            padx=5, pady=8,
            text='[Snippet name:]',
            font=('Verdana', 12),
            fg='#BD500C')
        frame_label_snippet.pack(side=tk.TOP, fill=tk.X, padx=2, pady=8)

        frame_label_code = tk.LabelFrame(
            self.tab1_frame,
            fg='#BD500C',
            text='[Snippet code:]',
            padx=5, pady=5,
            font=('Verdana', 12))
        frame_label_code.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, padx=2, pady=2)

        self.entry_snippet_name = tk.Entry(
            frame_label_snippet,
            fg='navy',
            bg='#FAFAFA',
            width=60,
            font=('Arial', 12),
            relief=tk.RAISED
        )
        self.entry_snippet_name.pack(fill='x')
        self.tree.target_caption_field_edit = self.entry_snippet_name

        # Textarea
        self.txt = tk.Text(
            frame_label_code,
            width=20, height=14,
            font=('Consolas', 12),
            fg='#F8F8F2', bg='#3C3F41',
            insertbackground='#F8F8F2',
            pady=5, padx=5,
            wrap=tk.WORD,
            relief=tk.RAISED)
        self.txt.pack(fill='both', expand='yes', pady=5)
        self.tree.target_textarea_field_edit = self.txt

        # Buttons panel
        frame_buttons = tk.Frame(self.tab1_frame)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

        btn_save = ttk.Button(
            frame_buttons,
            text='Save',
            image=self.save_icon, compound='left')
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_new = ttk.Button(
            frame_buttons,
            text='New',
            image=self.new_icon, compound='left')
        btn_new.pack(side=tk.LEFT, padx=5)

        btn_cancel = ttk.Button(
            frame_buttons,
            text='Cancel',
            image=self.cancel_icon, compound='left',
            command=lambda: self.root.destroy())
        btn_cancel.pack(side=tk.RIGHT, padx=5)

        self.txt_help = tk.Text(bg='lightgray', pady=5, padx=5)
        self.txt_help.insert(tk.INSERT, "Help comming soon.....")
        self.txt_help.configure(state='disabled')

        self.notebook.add(self.tab1_frame, text='Snippet', image=self.icons.file_blue,
                          compound='left')
        self.notebook.add(self.txt_help, text='Syntax Help', image=self.help_icon,
                          compound='left')

        self.root.mainloop()

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
            # Default settings
            return {
                "path_snippets": ".",
                "tab_width": 4
            }

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


if __name__ == '__main__':
    app = App()
