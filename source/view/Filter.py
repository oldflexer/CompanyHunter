import logging

import customtkinter as ctk


class Filter(ctk.CTkScrollableFrame):
    def __init__(self, label_font, entry_font, master=None, **kwargs):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")

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

            # control buttons
            self.control_frame = ctk.CTkFrame(master=self)
            self.button_prev_10 = ctk.CTkButton(master=self.control_frame, text="<-10", font=self.label_font)
            self.button_prev = ctk.CTkButton(master=self.control_frame, text="<-1", font=self.label_font)
            self.button_search = ctk.CTkButton(master=self.control_frame, text="Поиск", font=self.label_font)
            self.button_next = ctk.CTkButton(master=self.control_frame, text="1->", font=self.label_font)
            self.button_next_10 = ctk.CTkButton(master=self.control_frame, text="10->", font=self.label_font)
            self.button_prev_archive = ctk.CTkButton(master=self.control_frame, text="<-1", font=self.label_font)
            self.button_next_archive = ctk.CTkButton(master=self.control_frame, text="1->", font=self.label_font)

            # info labels
            self.info_frame = ctk.CTkFrame(master=self.control_frame)
            self.label_current_archive = ctk.CTkLabel(master=self.info_frame, font=self.label_font)
            self.label_current_xml = ctk.CTkLabel(master=self.info_frame, font=self.label_font)

            # settings and save to xlsx buttons
            self.button_settings = ctk.CTkButton(master=self, text="Настройки", font=self.label_font)
            self.button_xlsx = ctk.CTkButton(master=self, text="Сохранить в Excel", font=self.label_font)

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

            self.buttons = [self.button_prev_10,
                            self.button_prev,
                            self.button_search,
                            self.button_next,
                            self.button_next_10,
                            self.button_settings,
                            self.button_xlsx,
                            self.button_prev_archive,
                            self.button_next_archive]

            self.logger.info("init successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def switch_buttons(self):
        for btn in self.buttons:
            if btn.cget("state") == "normal":
                btn.configure(state="disabled")
            else:
                btn.configure(state="normal")

    def grid_all(self):
        try:
            self.logger.info("grid_all started")
            # grid widgets in filter
            rows = 3
            for row in range(rows):
                self.rowconfigure(index=row, weight=1)

            columns = 9
            for column in range(columns):
                self.columnconfigure(index=column, weight=1, pad=5, minsize=self.winfo_screenwidth() // columns - columns // 2)

            for column in range(0, len(self.input_widgets)):
                self.input_widgets[column][0].grid(row=0, column=column, sticky=ctk.SW, padx=5, pady=5)

            for column in range(0, len(self.input_widgets)):
                self.input_widgets[column][1].grid(row=1, column=column, sticky=ctk.EW, padx=5, pady=5)

            for column in range(0, len(self.switch_widgets)):
                self.switch_widgets[column].grid(row=1, column=column+6, sticky=ctk.EW, padx=5, pady=5)

            self.button_settings.grid(row=0, column=8, padx=5, pady=5, sticky=ctk.E)
            self.button_xlsx.grid(row=1, column=8, padx=5, pady=5, sticky=ctk.E)

            # grid widgets in control_frame
            rows = 3
            for row in range(rows):
                self.control_frame.rowconfigure(index=row, weight=1)

            columns = 5
            for column in range(columns):
                self.control_frame.columnconfigure(index=column, weight=1, pad=5)

            self.button_prev_archive.grid(row=0, column=1, padx=5, pady=5, sticky=ctk.NE)
            self.button_next_archive.grid(row=0, column=3, padx=5, pady=5, sticky=ctk.NW)

            self.button_prev_10.grid(row=1, column=0, padx=5, pady=5, sticky=ctk.NE)
            self.button_prev.grid(row=1, column=1, padx=5, pady=5, sticky=ctk.NE)
            self.button_search.grid(row=2, column=2, padx=5, pady=5, sticky=ctk.N)
            self.button_next.grid(row=1, column=3, padx=5, pady=5, sticky=ctk.NW)
            self.button_next_10.grid(row=1, column=4, padx=5, pady=5, sticky=ctk.NW)

            self.label_current_archive.grid(row=0, column=0, padx=5, pady=5, sticky=ctk.NE)
            self.label_current_xml.grid(row=1, column=0, padx=5, pady=5, sticky=ctk.NE)

            self.info_frame.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky=ctk.NS)
            self.control_frame.grid(row=2, column=0, columnspan=10, padx=5, pady=5, sticky=ctk.NW)

            self.logger.info("grid_all successfully completed")

        except Exception as exception:
            self.logger.exception(exception)
