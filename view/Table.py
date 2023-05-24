import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
import webbrowser


class Table(ctk.CTkFrame):
    def __init__(self, master=None, headings=tuple(), rows=tuple(), **kwargs):
        super().__init__(master, **kwargs)

        self.label_font = ctk.CTkFont(family="Calibri", size=14)
        self.entry_font = ctk.CTkFont(family="Calibri", size=14)

        # table things
        ttk.Style().theme_use("default")
        ttk.Style().configure("Treeview", background="#555555", foreground="White", fieldbackground="#333333",
                              font=self.entry_font)
        ttk.Style().configure("Treeview.Heading", background="#444444", font=self.label_font, foreground="White")
        ttk.Style().map("Treeview", background=[("selected", "#353535")])

        self.table = ttk.Treeview(self, show="headings", selectmode="extended")
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for head in headings:
            self.table.heading(head, text=head, anchor=ctk.CENTER)
            self.table.column(head, anchor=ctk.CENTER)

        for row in rows:
            self.table.insert("", ctk.END, values=tuple(row))

        # adding popup menu
        self.cursor_x = 0
        self.cursor_y = 0

        self.menu = tk.Menu(self.table, tearoff=0)
        self.menu.add_command(command=self.copy_cell, label="Копировать ячейку")
        self.menu.add_command(command=self.copy_rows, label="Копировать строки")
        self.menu.add_command(command=self.search_info, label="Поиск по ИНН")

        self.table.bind("<Button-3>", self.popup_menu)
        self.table.bind("<Control-Key-c>", self.copy_cell)

        self.scrollbar_y = ctk.CTkScrollbar(master=self, orientation=tk.constants.VERTICAL, command=self.table.yview, width=16)
        self.scrollbar_x = ctk.CTkScrollbar(master=self, orientation=tk.constants.HORIZONTAL, command=self.table.xview, height=16)

        self.table.configure(yscrollcommand=self.scrollbar_y.set)
        self.table.configure(xscrollcommand=self.scrollbar_x.set)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=0)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=0)

        self.scrollbar_x.pack(side=ctk.BOTTOM, expand=False, fill=ctk.BOTH)
        self.scrollbar_y.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH)
        self.table.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH)
        # self.scrollbar_y.grid(row=0, column=1, sticky=ctk.NS)
        # self.scrollbar_x.grid(row=1, column=0, sticky=ctk.EW)
        # self.table.grid(row=0, column=0, sticky=ctk.NS)

    def popup_menu(self, event):
        self.cursor_x = event.x
        self.cursor_y = event.y
        self.menu.post(event.x_root, event.y_root)

    def copy_cell(self, event=None):
        selection = self.table.selection()

        if not selection:
            return

        row = self.table.item(selection[0])["values"]

        match event:
            case None:
                column = self.table.identify_column(self.cursor_x)
            case _:
                column = self.table.identify_column(event.x)

        column_number = int(column.lstrip("#")) - 1
        cell = row[column_number]

        self.table.clipboard_clear()
        self.table.clipboard_append(str(cell))

        # print(self.table.clipboard_get())

    def copy_rows(self):
        selection = self.table.selection()

        if not selection:
            return

        self.table.clipboard_clear()

        for _id in selection:
            row = self.table.item(_id)["values"]
            self.table.clipboard_append("; ".join(str(cell) for cell in row) + "\n\n")

        # print(self.table.clipboard_get())

    def search_info(self):
        selection = self.table.selection()

        if not selection:
            return

        for _id in selection:
            row = self.table.item(_id)["values"]
            webbrowser.open(f"https://www.list-org.com/search?type=inn&val={row[2]}", new=0)
