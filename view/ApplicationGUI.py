import customtkinter as ctk
import model.Company as Company
import view.Table as Table
import view.Filter as Filter
import threading

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ApplicationGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set new window geometry, placement
        # self.geometry(
        #     f"{self.winfo_screenwidth() // 2}x{self.winfo_screenheight() // 2}+{self.winfo_width() // 2}+{self.winfo_height() // 2}")

        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()-70}")

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

        # self.main_frame.rowconfigure(index=0, weight=1)
        # self.main_frame.rowconfigure(index=1, weight=19)
        # self.main_frame.columnconfigure(index=0, weight=1)

        # pack filter
        self.filter_frame.pack(expand=False, fill=ctk.BOTH, padx=10, pady=10)
        self.filter_frame.grid_all()
        # self.filter_frame.grid(row=0, column=0, sticky=ctk.NSEW)

        # pack table
        self.table_frame.pack(expand=True, fill=ctk.BOTH, padx=10, pady=10)
        # self.table_frame.grid(row=1, column=0, sticky=ctk.NSEW)

    def add_company(self, company: Company.Company):
        # for attrib in dir(company):
        #     if not attrib.startswith("__"):
        #         print(attrib, company.__getattribute__(attrib))

        self.table_frame.table.insert(parent="",
                                      index=ctk.END,
                                      values=(company.small_name,
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

    def clear_table(self):
        self.table_frame.table.delete(*self.table_frame.table.get_children())

    def set_ctrl(self, ctrl):
        self.filter_frame.entry_full_name.configure(textvariable=ctrl.full_name)
        self.filter_frame.entry_date_reg.configure(textvariable=ctrl.date_reg)
        self.filter_frame.entry_region.configure(textvariable=ctrl.region)
        self.filter_frame.entry_town.configure(textvariable=ctrl.town)
        self.filter_frame.entry_main_okved.configure(textvariable=ctrl.main_okved)
        self.filter_frame.entry_additional_okved.configure(textvariable=ctrl.additional_okved)

        self.filter_frame.switch_status.configure(variable=ctrl.status)
        self.filter_frame.switch_email.configure(variable=ctrl.email)

        self.filter_frame.button_prev_10.configure(command=ctrl.prev_file_x10)
        self.filter_frame.button_prev.configure(command=ctrl.prev_file)
        self.filter_frame.button_search.configure(command=ctrl.search)
        self.filter_frame.button_next.configure(command=ctrl.next_file)
        self.filter_frame.button_next_10.configure(command=ctrl.next_file_x10)

        self.filter_frame.button_settings.configure(command=ctrl.open_config_window)
        self.filter_frame.button_xlsx.configure(command=ctrl.save_xlsx)

    def choose_window(self, event):
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
