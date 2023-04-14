import customtkinter as ctk
# import tkinter.constants as constants
import model.Company as Company
import view.ScrollableFrame as ScrollableFrame
import view.Table as Table

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ApplicationGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set new window geometry, placement
        self.geometry(
            f"{self.winfo_screenwidth() // 2}x{self.winfo_screenheight() // 2}+{self.winfo_width() // 2}+{self.winfo_height() // 2}")

        # set miscellaneous properties
        self.title("Company Hunter")
        self.iconbitmap("assets/company.ico")

        # set font for application widgets
        self.label_font = ctk.CTkFont(family="Calibri", size=14)
        self.entry_font = ctk.CTkFont(family="Calibri", size=14)

        # main frame that allows to drag by any part of window and master for other widgets
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.bind(LMB, self.choose_window)

        # frame with filter boxes
        self.filter_frame = ScrollableFrame.ScrollableFrame(master=self.main_frame)
        self.filter_frame.bind(LMB, self.choose_window)

        # filter boxes
        self.label_full_name = ctk.CTkLabel(master=self.filter_frame, text="Наименование организации",
                                            font=self.label_font)
        self.entry_full_name = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_date_reg = ctk.CTkLabel(master=self.filter_frame, text="Дата регистрации",
                                           font=self.label_font)
        self.entry_date_reg = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_region = ctk.CTkLabel(master=self.filter_frame, text="Регион", font=self.label_font)
        self.entry_region = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_town = ctk.CTkLabel(master=self.filter_frame, text="Город", font=self.label_font)
        self.entry_town = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_main_okved = ctk.CTkLabel(master=self.filter_frame, text="Основной ОКВЭД",
                                             font=self.label_font)
        self.entry_main_okved = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_additional_okved = ctk.CTkLabel(master=self.filter_frame, text="Дополнительный ОКВЭД",
                                                   font=self.label_font)
        self.entry_additional_okved = ctk.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_status = ctk.CTkLabel(master=self.filter_frame, text="Статус", font=self.label_font)
        self.switch_status = ctk.CTkSwitch(master=self.filter_frame, text="Только действующие",
                                           onvalue=True, offvalue=False, font=self.entry_font)

        self.button_search = ctk.CTkButton(master=self.filter_frame, text="Поиск", font=self.label_font)

        # frame with table
        self.table_frame = Table.Table(master=self.main_frame,
                                       headings=("Название организации",
                                                 "ИНН",
                                                 "КПП",
                                                 "Дата регистрации",
                                                 "Регион",
                                                 "Город",
                                                 "Улица",
                                                 "Строение",
                                                 "Помещение",
                                                 "Руководитель",
                                                 "Основной ОКВЭД",
                                                 "Дополнительные ОКВЭДы",
                                                 "Действующее"),
                                       rows=())
        self.table_frame.bind(LMB, self.choose_window)

        # pack all elements
        self.main_frame.pack(expand=True, fill=ctk.Y)

        # pack filters elements
        self.filter_frame.pack(expand=True, fill=ctk.Y, anchor=ctk.W, padx=5, pady=5, ipadx=5, ipady=5)

        self.label_full_name.pack(anchor=ctk.W)
        self.entry_full_name.pack(anchor=ctk.W)

        self.label_date_reg.pack(anchor=ctk.W)
        self.entry_date_reg.pack(anchor=ctk.W)

        self.label_region.pack(anchor=ctk.W)
        self.entry_region.pack(anchor=ctk.W)

        self.label_town.pack(anchor=ctk.W)
        self.entry_town.pack(anchor=ctk.W)

        self.label_main_okved.pack(anchor=ctk.W)
        self.entry_main_okved.pack(anchor=ctk.W)

        self.label_additional_okved.pack(anchor=ctk.W)
        self.entry_additional_okved.pack(anchor=ctk.W)

        self.label_status.pack(anchor=ctk.W)
        self.switch_status.pack(anchor=ctk.W)

        self.button_search.pack(anchor=ctk.W)

        # pack table
        self.table_frame.pack(expand=True, anchor=ctk.E, padx=5, pady=5, ipadx=5, ipady=5)

    def add_company(self, company: Company.Company):
        # for attrib in dir(company):
        #     if not attrib.startswith("__"):
        #         print(attrib, company.__getattribute__(attrib))

        self.table_frame.table.insert(parent="",
                                      index=ctk.END,
                                      values=(company.small_name,
                                              company.inn,
                                              company.kpp,
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

    def set_ctrl(self, ctrl):
        self.button_search.configure(command=ctrl.search)
        self.entry_full_name.configure(textvariable=ctrl.full_name)
        self.entry_date_reg.configure(textvariable=ctrl.date_reg)
        self.entry_region.configure(textvariable=ctrl.region)
        self.entry_town.configure(textvariable=ctrl.town)
        self.entry_main_okved.configure(textvariable=ctrl.main_okved)
        self.entry_additional_okved.configure(textvariable=ctrl.additional_okved)
        self.switch_status.configure(variable=ctrl.status)

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


if __name__ == "__main__":
    app = ApplicationGUI()
    app.mainloop()
