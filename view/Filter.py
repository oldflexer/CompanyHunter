import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk


class Filter(ctk.CTkScrollableFrame):
    def __init__(self, label_font, entry_font, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label_font = label_font
        self.entry_font = entry_font

        # filter elements
        self.label_full_name = ctk.CTkLabel(master=self, text="Наименование организации",
                                            font=self.label_font)
        self.entry_full_name = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_date_reg = ctk.CTkLabel(master=self, text="Дата регистрации",
                                           font=self.label_font)
        self.entry_date_reg = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_region = ctk.CTkLabel(master=self, text="Регион", font=self.label_font)
        self.entry_region = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_town = ctk.CTkLabel(master=self, text="Город", font=self.label_font)
        self.entry_town = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_main_okved = ctk.CTkLabel(master=self, text="Основной ОКВЭД",
                                             font=self.label_font)
        self.entry_main_okved = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_additional_okved = ctk.CTkLabel(master=self, text="Доп. ОКВЭД",
                                                   font=self.label_font)
        self.entry_additional_okved = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_status = ctk.CTkLabel(master=self, text="Статус", font=self.label_font)
        self.switch_status = ctk.CTkSwitch(master=self, text="Только действующие",
                                           onvalue=True, offvalue=False, font=self.entry_font)

        self.button_search = ctk.CTkButton(master=self, text="Поиск", font=self.label_font)

        self.widgets = [(self.label_full_name,
                        self.entry_full_name),
                        (self.label_date_reg,
                        self.entry_date_reg),
                        (self.label_region,
                        self.entry_region),
                        (self.label_town,
                        self.entry_town),
                        (self.label_main_okved,
                        self.entry_main_okved),
                        (self.label_additional_okved,
                        self.entry_additional_okved),
                        (self.label_status,
                        self.switch_status),
                        self.button_search]

        for c in range(7):
            self.columnconfigure(index=c, weight=1)

        for r in range(5):
            self.rowconfigure(index=r, weight=1)

        # pack elements
        self.columnconfigure(index=0, weight=1)
        self.label_full_name.grid(row=0, column=0, padx=10, sticky=ctk.SW)
        self.entry_full_name.grid(row=1, column=0, padx=10, sticky=ctk.EW)

        self.label_date_reg.grid(row=0, column=1, padx=10, sticky=ctk.SW)
        self.entry_date_reg.grid(row=1, column=1, padx=10, sticky=ctk.EW)

        self.label_region.grid(row=0, column=2, padx=10, sticky=ctk.SW)
        self.entry_region.grid(row=1, column=2, padx=10, sticky=ctk.EW)

        self.label_town.grid(row=0, column=3, padx=10, sticky=ctk.SW)
        self.entry_town.grid(row=1, column=3, padx=10, sticky=ctk.EW)

        self.label_main_okved.grid(row=0, column=4, padx=10, sticky=ctk.SW)
        self.entry_main_okved.grid(row=1, column=4, padx=10, sticky=ctk.EW)

        self.label_additional_okved.grid(row=0, column=5, padx=10, sticky=ctk.SW)
        self.entry_additional_okved.grid(row=1, column=5, padx=10, sticky=ctk.EW)

        self.label_status.grid(row=2, column=0, padx=10, sticky=ctk.SW)
        self.switch_status.grid(row=3, column=0, padx=10, sticky=ctk.EW)

        self.button_search.grid(row=4, column=0, sticky=ctk.S)
