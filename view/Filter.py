import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk


class Filter(ctk.CTkScrollableFrame):
    def __init__(self, label_font, entry_font, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label_font = label_font
        self.entry_font = entry_font

        # settings and save to xlsx buttons
        self.button_settings = ctk.CTkButton(master=self, text="Настройки", font=self.label_font)
        self.button_xlsx = ctk.CTkButton(master=self, text="Сохранить в Excel", font=self.label_font)

        # filter elements
        self.label_full_name = ctk.CTkLabel(master=self, text="Наименование организации",
                                            font=self.label_font)
        self.entry_full_name = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_date_reg = ctk.CTkLabel(master=self, text="Дата регистрации",
                                           font=self.label_font)
        self.entry_date_reg = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_region = ctk.CTkLabel(master=self, text="Субъект", font=self.label_font)
        self.entry_region = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_town = ctk.CTkLabel(master=self, text="Нас. пункт", font=self.label_font)
        self.entry_town = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_main_okved = ctk.CTkLabel(master=self, text="Основной ОКВЭД",
                                             font=self.label_font)
        self.entry_main_okved = ctk.CTkEntry(master=self, font=self.entry_font)

        self.label_additional_okved = ctk.CTkLabel(master=self, text="Доп. ОКВЭД",
                                                   font=self.label_font)
        self.entry_additional_okved = ctk.CTkEntry(master=self, font=self.entry_font)

        self.switch_status = ctk.CTkSwitch(master=self, text="Только действующие",
                                           onvalue=True, offvalue=False, font=self.entry_font)

        self.switch_email = ctk.CTkSwitch(master=self, text="Только с почтой",
                                          onvalue=True, offvalue=False, font=self.entry_font)

        self.info_frame = ctk.CTkFrame(master=self)
        self.label_current_archive = ctk.CTkLabel(master=self.info_frame, font=self.label_font)
        self.label_current_xml = ctk.CTkLabel(master=self.info_frame, font=self.label_font)

        self.button_frame = ctk.CTkFrame(master=self)
        self.button_prev_10 = ctk.CTkButton(master=self.button_frame, text="<-10", font=self.label_font)
        self.button_prev = ctk.CTkButton(master=self.button_frame, text="<-1", font=self.label_font)
        self.button_search = ctk.CTkButton(master=self.button_frame, text="Поиск", font=self.label_font)
        self.button_next = ctk.CTkButton(master=self.button_frame, text="1->", font=self.label_font)
        self.button_next_10 = ctk.CTkButton(master=self.button_frame, text="10->", font=self.label_font)

        self.input_widgets = [(self.label_full_name,
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
                               self.entry_additional_okved)]

        self.switch_widgets = [self.switch_status,
                               self.switch_email]

    def grid_all(self):
        # grid widgets
        rows = 4
        for row in range(rows):
            self.rowconfigure(index=row, weight=1)

        columns = 7
        for column in range(columns):
            self.columnconfigure(index=column, weight=1, pad=5, minsize=self.winfo_screenwidth()//(columns+1))

        self.label_current_archive.pack(side=ctk.TOP, expand=True, anchor=ctk.E)
        self.label_current_xml.pack(side=ctk.TOP, expand=True, anchor=ctk.E)
        self.info_frame.grid(row=0, column=0, rowspan=2, sticky=ctk.NSEW, padx=5, pady=5)

        self.button_settings.grid(row=2, column=0, padx=5, pady=5)
        self.button_xlsx.grid(row=3, column=0, padx=5, pady=5)

        for column in range(0, len(self.input_widgets)):
            self.input_widgets[column][0].grid(row=0, column=column+1, sticky=ctk.SW, padx=5, pady=5)

        for column in range(0, len(self.input_widgets)):
            self.input_widgets[column][1].grid(row=1, column=column+1, sticky=ctk.EW, padx=5, pady=5)

        for column in range(0, len(self.switch_widgets)):
            self.switch_widgets[column].grid(row=2, column=column+1, sticky=ctk.EW, padx=5, pady=5)

        self.button_prev_10.pack(side=ctk.LEFT, expand=True, padx=5, pady=5)
        self.button_prev.pack(side=ctk.LEFT, expand=True, padx=5, pady=5)
        self.button_search.pack(side=ctk.LEFT, expand=True, padx=5, pady=5)
        self.button_next.pack(side=ctk.LEFT, expand=True, padx=5, pady=5)
        self.button_next_10.pack(side=ctk.LEFT, expand=True, padx=5, pady=5)
        self.button_frame.grid(row=3, column=1, columnspan=4, sticky=ctk.NSEW, padx=5, pady=5)
