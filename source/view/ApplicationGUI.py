import logging

import customtkinter as ctk

import source.model.Company as Company
import source.view.Filter as Filter
import source.view.Table as Table

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ApplicationGUI(ctk.CTk):
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")

            super().__init__()
            # set new window geometry, placement
            self.geometry(
                f"{self.winfo_screenwidth()}x{self.winfo_screenheight()-70}+{0}+{0}")

            # set miscellaneous properties
            self.title("Company Hunter")
            self.iconbitmap("assets/company.ico")

            # set font for application widgets
            self.label_font = ctk.CTkFont(family="Calibri", size=16)
            self.entry_font = ctk.CTkFont(family="Calibri", size=14)

            # main frame that allows to drag by any part of window and master for other widgets
            self.main_frame = ctk.CTkFrame(master=self)
            self.main_frame.bind(LMB, self.choose_window)

            # frame with filter boxes
            self.filter_frame = Filter.Filter(master=self.main_frame,
                                              label_font=self.label_font,
                                              entry_font=self.entry_font,
                                              orientation=ctk.HORIZONTAL)
            self.filter_frame.bind(LMB, self.choose_window)

            # frame with table
            self.table_frame = Table.Table(master=self.main_frame,
                                           headings=("Название организации",
                                                     "Почта",
                                                     "ИНН",
                                                     "Дата регистрации",
                                                     "Субъект",
                                                     "Нас. пункт",
                                                     "Улица",
                                                     "Строение",
                                                     "Помещение",
                                                     "Руководитель",
                                                     "Основной ОКВЭД",
                                                     "Дополнительные ОКВЭДы",
                                                     "Действующее"),
                                           rows=())
            self.table_frame.bind(LMB, self.choose_window)

            # pack main frame
            self.main_frame.pack(expand=True, fill=ctk.BOTH)

            # pack filter
            self.filter_frame.pack(expand=False, fill=ctk.BOTH, padx=5, pady=5, ipady=5)
            self.filter_frame.grid_all()

            # pack table
            self.table_frame.pack(expand=True, fill=ctk.BOTH, padx=5, pady=5)

            self.logger.info("init successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def add_company(self, company: Company.Company):
        try:
            self.table_frame.table.insert(parent="",
                                          index=ctk.END,
                                          values=(company.name,
                                                  company.email,
                                                  company.inn,
                                                  company.date_reg,
                                                  company.region,
                                                  company.town,
                                                  company.street,
                                                  company.building,
                                                  company.apartments,
                                                  company.director,
                                                  company.main_okved,
                                                  company.additional_okved,
                                                  company.status))
        except Exception as exception:
            self.logger.exception(exception)

    def clear_table(self):
        try:
            self.table_frame.table.delete(*self.table_frame.table.get_children())
        except Exception as exception:
            self.logger.exception(exception)

    def set_controller(self, controller):
        try:
            self.filter_frame.entry_full_name.configure(textvariable=controller.full_name)
            self.filter_frame.entry_date_reg.configure(textvariable=controller.date_reg)
            self.filter_frame.entry_region.configure(textvariable=controller.region)
            self.filter_frame.entry_town.configure(textvariable=controller.town)
            self.filter_frame.entry_main_okved.configure(textvariable=controller.main_okved)
            self.filter_frame.entry_additional_okved.configure(textvariable=controller.additional_okved)

            self.filter_frame.switch_status.configure(variable=controller.status)
            self.filter_frame.switch_email.configure(variable=controller.email)

            self.filter_frame.button_prev_10.configure(command=controller.prev_file_x10)
            self.filter_frame.button_prev.configure(command=controller.prev_file)
            self.filter_frame.button_search.configure(command=controller.search)
            self.filter_frame.button_next.configure(command=controller.next_file)
            self.filter_frame.button_next_10.configure(command=controller.next_file_x10)

            self.filter_frame.button_settings.configure(command=controller.open_config_window)
            self.filter_frame.button_xlsx.configure(command=controller.save_xlsx)

            self.filter_frame.button_prev_archive.configure(command=controller.prev_archive)
            self.filter_frame.button_next_archive.configure(command=controller.next_archive)

        except Exception as exception:
            self.logger.exception(exception)

    def choose_window(self, event):
        try:
            delta_x = self.winfo_x()
            delta_y = self.winfo_y()

            delta_x -= event.x_root
            delta_y -= event.y_root

            def move_window(event):
                self.geometry(
                    f"{self.winfo_width()}x{self.winfo_height()}+{event.x_root + delta_x}+{event.y_root + delta_y}")

            self.main_frame.bind(LMM, move_window)
            self.filter_frame.bind(LMM, move_window)
            self.table_frame.bind(LMM, move_window)

        except Exception as exception:
            self.logger.exception(exception)
