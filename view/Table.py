import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk


class Table(ctk.CTkFrame):
    def __init__(self, master=None, headings=tuple(), rows=tuple(), **kwargs):
        super().__init__(master, **kwargs)

        self.label_font = ctk.CTkFont(family="Calibri", size=14)
        self.entry_font = ctk.CTkFont(family="Calibri", size=14)

        ttk.Style().theme_use("default")
        ttk.Style().configure("Treeview", background="#555555", foreground="White", fieldbackground="#333333", font=self.entry_font)
        ttk.Style().configure("Treeview.Heading", background="#444444", font=self.label_font, foreground="White")
        ttk.Style().map("Treeview", background=[("selected", "#113322")])

        self.table = ttk.Treeview(self, show="headings", selectmode="extended")
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for head in headings:
            self.table.heading(head, text=head, anchor=ctk.CENTER)
            self.table.column(head, anchor=ctk.CENTER)

        for row in rows:
            self.table.insert("", ctk.END, values=tuple(row))

        self.scrollbar_y = ctk.CTkScrollbar(master=self, orientation=tk.constants.VERTICAL, command=self.table.yview)
        self.scrollbar_x = ctk.CTkScrollbar(master=self, orientation=tk.constants.HORIZONTAL, command=self.table.xview)

        self.table.configure(yscrollcommand=self.scrollbar_y.set)
        self.table.configure(xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(expand=ctk.YES, fill=ctk.Y, side=ctk.RIGHT)
        self.scrollbar_x.pack(expand=ctk.YES, fill=ctk.X, side=ctk.BOTTOM)
        self.table.pack(expand=ctk.YES, fill=ctk.Y)
