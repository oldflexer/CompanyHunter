import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk

import view.ScrollableFrame


class Table(view.ScrollableFrame.ScrollableFrame):
    def __init__(self, master, headings=tuple(), rows=tuple(), **kwargs):
        super().__init__(master, **kwargs)

        self.label_font = ctk.CTkFont(family="Calibri", size=18)
        self.entry_font = ctk.CTkFont(family="Calibri", size=14)

        ttk.Style().theme_use("default")
        ttk.Style().configure("Treeview", background="#555555", foreground="White", fieldbackground="#333333")
        ttk.Style().map("Treeview",
                        background=[("selected", "#66CC88")])

        ttk.Style().configure("Treeview.Heading", background="#444444", font=self.label_font)
        ttk.Style().configure("Treeview", background="#555555", font=self.entry_font)

        self.table = ttk.Treeview(self, show="headings", selectmode="extended")
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings

        for head in headings:
            self.table.heading(head, text=head, anchor=ctk.CENTER)
            self.table.column(head, anchor=ctk.CENTER)

        for row in rows:
            self.table.insert("", ctk.END, values=tuple(row))

        self.table.pack(expand=ctk.YES, fill=ctk.BOTH)

