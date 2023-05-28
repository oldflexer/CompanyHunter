import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
import logging
import customtkinter as ctk


class Table(ctk.CTkFrame):
    def __init__(self, master=None, headings=tuple(), rows=tuple(), **kwargs):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
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
            self.menu.add_command(command=self.search_info_v2, label="Поиск по ИНН 2")
            self.menu.add_command(command=self.search_licenses, label="Поиск лицензий РПН")

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

            self.logger.info("init successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def popup_menu(self, event):
        try:
            self.logger.info("popup_menu started")
            self.cursor_x = event.x
            self.cursor_y = event.y
            self.menu.post(event.x_root, event.y_root)
            self.logger.info("popup_menu successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def copy_cell(self, event=None):
        try:
            self.logger.info("copy_cell started")
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

            self.logger.info("copy_cell successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def copy_rows(self):
        try:
            self.logger.info("copy_rows started")
            selection = self.table.selection()

            if not selection:
                return

            self.table.clipboard_clear()

            for _id in selection:
                row = self.table.item(_id)["values"]
                self.table.clipboard_append("; ".join(str(cell) for cell in row) + "\n\n")

            self.logger.info("copy_rows successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def search_info(self):
        try:
            self.logger.info("search_info started")
            selection = self.table.selection()

            if not selection:
                return

            for _id in selection:
                row = self.table.item(_id)["values"]
                webbrowser.open(f"https://www.list-org.com/search?type=inn&val={row[2]}", new=0)

            self.logger.info("search_info successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def search_info_v2(self):
        try:
            self.logger.info("search_info_v2 started")
            selection = self.table.selection()

            if not selection:
                return

            for _id in selection:
                row = self.table.item(_id)["values"]
                webbrowser.open(f"https://www.innproverka.ru/search?query={row[2]}", new=0)

            self.logger.info("search_info_v2 successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def search_licenses(self):
        try:
            self.logger.info("search_licenses started")
            selection = self.table.selection()

            if not selection:
                return

            for _id in selection:
                row = self.table.item(_id)["values"]
                webbrowser.open(f"https://license.rpn.gov.ru/rpn/license-registry?pcurrent_page=1&pper_page=20&plast_page=1&finn={row[2]}&oissuer_order_at=desc", new=0)

            self.logger.info("search_licenses successfully completed")

        except Exception as exception:
            self.logger.exception(exception)
