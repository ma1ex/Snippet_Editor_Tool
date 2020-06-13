import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from IconsBase64 import Icons
from Tooltip import ToolTip


class TreeFileManager(tk.Frame):
    """
    Tree File Manager
    """

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        # self.main_frame = self

        # self.__tree_struct_dict = {} # shadow copy

        # Treeview width
        self.width_tree = 200
        # Filesystem path
        self.path = os.getcwd()

        # Filesystem buffer
        self.__tree_struct_dict = {}
        # Treeview iid node name
        self.tree_root_node = 'root_node'
        # Main column title
        self.header_title = 'Tree FileManager'
        # Tree root icon
        self.icons = Icons()
        # Tree folders icon
        self.folder_icon = self.icons.folder_blue
        # Tree files icon
        self.file_icon = self.icons.file_orange
        self.home_style = {'foreground': '#9C9C9C', 'font': ('Verdana', 10)}
        self.folder_style = {'foreground': '#002E48', 'font': ('Verdana', 12)}
        self.file_style = {'foreground': '#BD9662', 'font': ('Verdana', 11)}

        self.scrollbars = {'vertical': True, 'horizontal': True}
        self.show_toolbar = False
        self.show_context_menu = True
        self.target_caption_field_edit = None
        self.target_textarea_field_edit = None
        # ----------------------------------------------------------------------
        self.collapse_icon = self.icons.collapse
        self.expand_icon = self.icons.expand

        self.new_file_icon = self.icons.file_add
        self.del_file_icon = self.icons.file_remove
        self.new_folder_icon = self.icons.folder_add2
        self.del_folder_icon = self.icons.folder_remove
        self.edit_icon = self.icons.edit_green_pen
        self.update_icon = self.icons.refresh_blue

        # Widgets
        # self.menu = tk.Menu()
        self.style = ttk.Style()
        self.tree = ttk.Treeview()

        # self.style.configure('Treeview', foreground='yellow',
        #                      background='#16181D',
        #                      fieldbackground='#16181D',
        #                      selectbackground='red', rowheight=28)

        # ----------------------------------------------------------------------

    def create(self):
        """

        :return:
        """

        # PROPOSAL -------------------------------------------------------------
        # toggle = itertools.cycle([600, self.width_tree])
        # self.tree.heading('#0', text=self.header_title, command=lambda: self.tree.column('#0', width=next(toggle)))
        # self.tree.column('#0', width=230, minwidth=220, stretch=tk.NO)
        # ----------------------------------------------------------------------

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        self.tree = ttk.Treeview(frame, selectmode='browse')
        self.tree.heading('#0', text=self.header_title)
        self.tree.column('#0', width=self.width_tree)

        # Style Treeview -------------------------------------------------------
        self.style.map('Treeview', foreground=self._fixed_map('foreground'),
                       background=self._fixed_map('background'))
        self.style.configure('Treeview', rowheight=28)
        self.tree.tag_configure('Home', **self.home_style)
        self.tree.tag_configure('Dirs', **self.folder_style)
        self.tree.tag_configure('Files', **self.file_style)
        self.tree.pack(side=tk.LEFT, fill=tk.Y)
        self._tree_create()
        self.tree.bind('<<TreeviewSelect>>', self.__select)
        self.tree.bind('<Double-Button-1>', lambda event: self._edit(event))

        self.get_scrollbar(wrapper=frame, **self.scrollbars)
        self.get_context_menu(show=self.show_context_menu)
        self.get_toolbar(show=self.show_toolbar)

    def __select(self, *event):

        item = self.tree.selection()
        print('item:', item)

        item_text = self.tree.item(item)['text']
        print('item_text:', item_text)
        item_values = ''.join(self.tree.item(item)['values'])
        print(item_text, item_values)
        parent_id = self.tree.parent(item)
        parent_name = self.tree.item(parent_id)['text']

        if os.path.isfile(item_values):
            print('True - this file!')

        # print('Child: ', self.tree.get_children(item[0]))
        print('Parent id: ', parent_id)
        print('Parent name: ', parent_name)

        return {'name': item_text, 'path': item_values, 'parent_id': parent_id,
                'parent_name': parent_name}

    def _path_scandir(self, path, parent):
        """
        os.scandir is much faster because it uses iterator, caching, and
        low-level calling of OS functions
        """

        with os.scandir(path) as p:
            for entry in p:
                abspath = os.path.join(path, entry)
                if entry.is_dir():
                    # name = f'[{entry.name}]'
                    # parent_element = self.tree.insert(parent, 'end', text=name,
                    name = '|' + entry.name + '|'
                    parent_element = self.tree.insert(parent, 'end', iid=name, text=name,
                                                      open=False, values=abspath.split(','), image=self.folder_icon,
                                                      tags='Dirs')
                    # self.__tree_struct_dict[parent_element] = self.tree.item(parent_element)['text']
                else:
                    parent_element = self.tree.insert(parent, 'end', iid=entry.name, text=entry.name, open=False,
                                                      values=abspath.split(','), image=self.file_icon, tags='Files')
                    # self.__tree_struct_dict[parent_element] = self.tree.item(parent_element)['text']
                if entry.is_dir():
                    self._path_scandir(abspath, parent_element)

    def _tree_create(self):
        dirs = self.tree.insert('', 'end', text=self.path, iid=self.tree_root_node,
                                open=True, tags='Home', image=self.icons.home)
        self._path_scandir(self.path, dirs)

    def tree_update(self):
        self._tree_del()
        self._tree_create()

    def _tree_del(self):
        """Retrieving rows from Treeview and deleting them to avoid repetitive content"""

        [self.tree.delete(i) for i in self.tree.get_children()]

    def _add_new_folder(self, path):

        if not (path and os.path.isdir(path)):
            mb.showerror(title='Error!', message='Choosed item is not a '
                                                 'folder!\n\nSelect folder item and try again.')
            return

        add_folder_dlg = ModalDialog(self.master, title='Add new folder',
                                     icon=self.icons.folder_orange)

        frame = tk.Frame(add_folder_dlg)
        frame.pack(expand='yes', padx=5, pady=5)

        label_path_info = tk.Label(frame, text='Path: ', anchor=tk.W, font='bold')
        label_path_info.grid(row=0, column=0, sticky=tk.E)

        label_path = tk.Label(frame, text=f'...{path[40:]}', width=50, anchor=tk.W, fg='blue', bg='#DDDDDD')
        label_path.grid(row=0, column=1)

        label_name = tk.Label(frame, text='Name:', anchor=tk.W, font='bold')
        label_name.grid(row=1, column=0, sticky=tk.E)

        entry_new = tk.Entry(frame)
        entry_new.focus_set()
        entry_new.grid(row=1, column=1, pady=5, sticky=tk.W + tk.E)

        def __save():
            new_folder_name = entry_new.get()

            if not new_folder_name:
                return

            try:
                os.mkdir(os.path.join(path, new_folder_name))
                self.tree_update()
                # mb.showinfo(title='Success!', message='Ok!')
                item = f'|{new_folder_name}|'
                self._open_parent(item)
                self.tree.focus(item)
                self.tree.selection_set(item)

                # item = f'[{new_folder_name}]'

                # for key, value in self.__tree_struct_dict.items():
                #     if value == item:
                #         print(f'Найдено! - {key}: {value} - ', self.tree.item(key))
                #         self._open_parent(key)
                #         self.tree.focus(key)
                #         self.tree.selection_set(key)

            except FileExistsError:
                mb.showerror('Error!', f'Folder "{new_folder_name}" is exists!')
                entry_new.selection_range(0, tk.END)
                entry_new.focus_set()
                return

            add_folder_dlg.destroy()

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)

        btn_save = ttk.Button(btn_frame, text='Save', image=self.icons.save,
                              compound='left', command=__save)
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_cancel = ttk.Button(btn_frame, text='Cancel', image=self.icons.cancel,
                              compound='left', command=add_folder_dlg.destroy)
        btn_cancel.pack(side=tk.LEFT)

        # add_folder_dlg.show()

    def _del_folder(self, path, item):
        if not (path and os.path.isdir(path)):
            mb.showerror(title='Error!', message='Choosed item is not a '
                                                 'folder!\n\nSelect folder item and try again.')
            return

        # print('Parent name: ', self.tree.item(parent))
        parent = self.tree.parent(item)
        print('Parent name--:', self.tree.parent(item))

        dir_name = os.path.basename(path)
        question = mb.askokcancel(f'DELETE folder "{dir_name}"', 'Are you sure want to delete '
                                                 f'"{dir_name}" folder and all its content?', icon=mb.WARNING)
        print(question)

        if question:
            try:
                os.rmdir(path)

            except OSError as e:
                print(f'Error! {path} : {e.strerror}')

            self.tree.delete(item)
            mb.showinfo(title='Complete!', message='Deleted successfully!')
            self.tree.focus(parent)
            self.tree.selection_set(parent)


    def _edit(self, *event):

        if not (isinstance(self.target_caption_field_edit, tk.Entry) and
                isinstance(self.target_textarea_field_edit, tk.Text)):
            mb.showerror(title='Error!', message='Fields for editing are not specified!')
            return

        # if not os.path.isfile(self.__select()['path']):
        #     mb.showerror(title='Error!', message='Select file for edit!')
        #     return

        print(self.__select()['path'], self.__select()['name'])
        print(type(self.__select()['path']), type(self.__select()['name']))

        file_path = self.__select()['path']
        file_name = self.__select()['name']

        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Вставка имени редактируемого файла
            self.target_caption_field_edit.delete(0, tk.END)
            self.target_caption_field_edit.insert(0, file_name)

            f = open(file_path, 'r')
            f_read = f.read()
            self.target_textarea_field_edit.delete(1.0, tk.END)
            self.target_textarea_field_edit.insert(1.0, f_read)
            f.close()

    def _open_parent(self, item):
        parent = self.tree.parent(item)

        if parent:
            self.tree.item(parent, open=True)
            self._open_parent(parent)

    def __toggle_open_nodes(self, open=True):

        def execute(item):
            self.tree.item(item, open=open)
            for child in self.tree.get_children(item):
                execute(child)

        execute(self.tree.get_children(self.tree_root_node))

    def collapse_all(self):
        self.__toggle_open_nodes(False)

    def expand_all(self):
        self.__toggle_open_nodes(True)

    def get_scrollbar(self, wrapper, vertical=False, horizontal=False):

        if vertical:
            scrollbar_y = ttk.Scrollbar(wrapper, command=self.tree.yview)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.config(yscrollcommand=scrollbar_y.set)
        if horizontal:
            scrollbar_x = ttk.Scrollbar(wrapper, orient=tk.HORIZONTAL, command=self.tree.xview)
            scrollbar_x.place(x=0, rely=1, width=self.width_tree, anchor=tk.SW)
            self.tree.configure(xscrollcommand=scrollbar_x.set)

    def get_context_menu(self, show=True):
        if show:
            menu = tk.Menu(self.tree, tearoff=0)
            menu.add_command(label='Edit snippet', image=self.edit_icon,
                             compound='left', command=self._edit)
            menu.add_separator()
            menu.add_command(label='New snippet', image=self.new_file_icon,
                             compound='left')
            menu.add_command(label='Delete snippet', image=self.del_file_icon,
                             compound='left')
            menu.add_separator()
            menu.add_command(label='New folder', image=self.new_folder_icon,
                             compound='left', command=lambda: self._add_new_folder(self.__select()['path']))
            menu.add_command(label='Delete folder', image=self.del_folder_icon,
                             compound='left', command=lambda: self._del_folder(self.__select()['path'],
                                                                               self.tree.selection()[0]))
            menu.add_separator()
            menu.add_command(label='Update', image=self.update_icon,
                             compound='left', command=self.tree_update)
            # self.menu.add_command(label='Delete Tree', command=self._tree_del)
            self.tree.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))

    def get_toolbar(self, show=False):
        if show:
            # Selecting the buttons background depending on the Theme used
            btn_background = '#EEEEEE'
            this_style = self.style.theme_use()
            if this_style == 'vista':
                btn_background = '#F7F8FA'
            elif this_style == 'clam':
                btn_background = '#DCDAD5'

            btn_toolbar_collapse = tk.Button(self.tree, bg=btn_background,
                                             image=self.collapse_icon, relief=tk.FLAT,
                                             command=self.collapse_all)
            btn_toolbar_collapse.place(x=5, y=3)

            btn_toolbar_expand = tk.Button(self.tree, bg=btn_background,
                                           image=self.expand_icon, relief=tk.FLAT,
                                           command=self.expand_all)
            btn_toolbar_expand.place(x=30, y=3)

            ToolTip(btn_toolbar_collapse, 'Collapse all!')
            ToolTip(btn_toolbar_expand, 'Expand all')

    def _fixed_map(self, option):
        """
        Bug fix Treeview styling
        """

        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.

        style = ttk.Style()

        return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]


class ModalDialog(tk.Toplevel):
    """
    Modal Dialog
    """

    def __init__(self, parent, title='Dialog', icon=None):
        super().__init__(parent)

        self.parent = parent
        x = int((self.parent.winfo_screenwidth() - self.winfo_reqwidth()) / 2)
        y = int((self.parent.winfo_screenheight() - self.winfo_reqheight()) / 2)
        self.wm_geometry("+%d+%d" % (x, y))
        self.resizable(False, False)
        self.transient(parent)

        if icon:
            self.tk.call('wm', 'iconphoto', self._w, icon)
        else:
            self.attributes('-toolwindow', True)

        self.title(title)

        self.grab_set()
        self.focus_set()
