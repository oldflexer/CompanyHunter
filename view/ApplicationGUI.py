import customtkinter
import tkinter.constants
import model.Company
import view.ScrollableFrame
import view.Table

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ApplicationGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # set new window geometry, placement
        self.geometry(
            f"{self.winfo_screenwidth() // 2}x{self.winfo_screenheight() // 2}+{self.winfo_width() // 2}+{self.winfo_height() // 2}")

        # set miscellaneous properties
        self.title("Company Hunter")
        self.iconbitmap("assets/company.ico")
        # self.bind("<Configure>", self.configure_window)

        # set font for application widgets
        self.label_font = customtkinter.CTkFont(family="Calibri", size=18)
        self.entry_font = customtkinter.CTkFont(family="Calibri", size=14)

        # main frame that allows to drag by any part of window and master for other widgets
        self.main_frame = customtkinter.CTkFrame(master=self)
        self.main_frame.bind(LMB, self.choose_window)

        # frame with filter boxes
        self.filter_frame = view.ScrollableFrame.ScrollableFrame(master=self.main_frame)
        self.filter_frame.bind(LMB, self.choose_window)

        # filter boxes
        self.label_full_name = customtkinter.CTkLabel(master=self.filter_frame, text="Наименование организации", font=self.label_font)
        self.entry_full_name = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_date_reg = customtkinter.CTkLabel(master=self.filter_frame, text="Дата регистрации", font=self.label_font)
        self.entry_date_reg = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_region = customtkinter.CTkLabel(master=self.filter_frame, text="Регион", font=self.label_font)
        self.entry_region = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_town = customtkinter.CTkLabel(master=self.filter_frame, text="Город", font=self.label_font)
        self.entry_town = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_main_okved = customtkinter.CTkLabel(master=self.filter_frame, text="Основной ОКВЭД", font=self.label_font)
        self.entry_main_okved = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_additional_okved = customtkinter.CTkLabel(master=self.filter_frame, text="Дополнительный ОКВЭД",
                                               font=self.label_font)
        self.entry_additional_okved = customtkinter.CTkEntry(master=self.filter_frame, font=self.entry_font)

        self.label_status = customtkinter.CTkLabel(master=self.filter_frame, text="Статус", font=self.label_font)
        self.switch_status = customtkinter.CTkSwitch(master=self.filter_frame, text="Любая / Действующая",
                                       onvalue=True, offvalue=False, font=self.entry_font)

        self.button_search = customtkinter.CTkButton(master=self.filter_frame, text="Поиск", font=self.label_font)
        # self.button_search.bind(LMB, self.btn_func)

        # frame with table
        self.table_frame = view.Table.Table(master=self.main_frame, headings=("Название организации",
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

        # pack all elements, make grid
        self.main_frame.pack(expand=True, fill=tkinter.constants.BOTH)

        self.main_frame.columnconfigure(index=0, weight=1)
        self.main_frame.columnconfigure(index=1, weight=19)
        self.main_frame.rowconfigure(index=0, weight=1)

        # grid filters elements
        self.filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.constants.NSEW)

        self.filter_frame.columnconfigure(index=0, weight=2)
        self.filter_frame.columnconfigure(index=1, weight=8)

        self.label_full_name.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_full_name.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_date_reg.grid(row=3, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_date_reg.grid(row=4, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_region.grid(row=5, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_region.grid(row=6, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_town.grid(row=7, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_town.grid(row=8, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_main_okved.grid(row=9, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_main_okved.grid(row=10, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_additional_okved.grid(row=11, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.entry_additional_okved.grid(row=12, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.label_status.grid(row=13, column=0, padx=5, pady=5, sticky=tkinter.constants.NW, columnspan=2)
        self.switch_status.grid(row=14, column=0, padx=5, pady=5, sticky=tkinter.constants.EW, columnspan=2)

        self.button_search.grid(row=15, column=1, padx=5, pady=5, sticky=tkinter.constants.SE)

        # grid table
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tkinter.constants.NSEW)

    def add_company(self, company: model.Company.Company):
        self.table_frame.table.insert(company)

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
