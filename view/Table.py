import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk


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

        self.table.bind("<Button-3>", self.popup_menu)
        self.table.bind("<Control-Key-c>", self.copy_cell)

        self.scrollbar_y = ctk.CTkScrollbar(master=self, orientation=tk.constants.VERTICAL, command=self.table.yview)
        self.scrollbar_x = ctk.CTkScrollbar(master=self, orientation=tk.constants.HORIZONTAL, command=self.table.xview)

        self.table.configure(yscrollcommand=self.scrollbar_y.set)
        self.table.configure(xscrollcommand=self.scrollbar_x.set)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=0)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=0)

        self.scrollbar_y.grid(row=0, column=1, sticky=ctk.NS)
        self.scrollbar_x.grid(row=1, column=0, sticky=ctk.EW)
        self.table.grid(row=0, column=0, sticky=ctk.NS)

    def popup_menu(self, event):
        self.cursor_x = event.x
        self.cursor_y = event.y
        self.menu.post(event.x_root, event.y_root)

    def copy_cell(self, event=None):
        selection = self.table.selection()
        if selection:
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

            print(self.table.clipboard_get())

    def copy_rows(self, event=None):
        selection = self.table.selection()
        row = None
        if selection:
            self.table.clipboard_clear()

            for _id in selection:
                row = self.table.item(_id)["values"]
                self.table.clipboard_append(str(row))

            print(self.table.clipboard_get())
