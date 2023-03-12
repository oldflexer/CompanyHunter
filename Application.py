import customtkinter
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkSwitch
from tkinter.constants import *
from ScrollableFrame import ScrollableFrame

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


class Application(CTk):
    def __init__(self):
        super().__init__()

        # set new window geometry, placement
        self.geometry(
            f"{self.winfo_screenwidth() // 2}x{self.winfo_screenheight() // 2}+{self.winfo_width() // 2}+{self.winfo_height() // 2}")

        # set miscellaneous properties
        self.title("Company Hunter")
        self.iconbitmap("assets/company.ico")
        self.bind("<Configure>", self.window_event)

        # main frame that allows to drag by any part of window and master for other widgets
        self.main_frame = CTkFrame(master=self)
        self.main_frame.bind("<Button-1>", self.choose_window)

        # frame with filter boxes
        self.filter_frame = ScrollableFrame(master=self.main_frame, bg_color="WHITE")
        self.filter_frame.bind("<Button-1>", self.choose_window)

        # filter boxes
        self.label_full_name = CTkLabel(master=self.filter_frame, text="Наименование организации")
        self.entry_full_name = CTkEntry(master=self.filter_frame)

        self.label_date_reg = CTkLabel(master=self.filter_frame, text="Дата регистрации")
        self.entry_date_reg = CTkEntry(master=self.filter_frame)

        self.label_region = CTkLabel(master=self.filter_frame, text="Регион")
        self.entry_region = CTkEntry(master=self.filter_frame)

        self.label_town = CTkLabel(master=self.filter_frame, text="Город")
        self.entry_town = CTkEntry(master=self.filter_frame)

        self.label_main_okved = CTkLabel(master=self.filter_frame, text="Основной ОКВЭД")
        self.entry_main_okved = CTkEntry(master=self.filter_frame)

        self.label_additional_okved = CTkLabel(master=self.filter_frame, text="Дополнительный ОКВЭД")
        self.entry_additional_okved = CTkEntry(master=self.filter_frame)

        self.label_status = CTkLabel(master=self.filter_frame, text="Статус")
        self.switch_status_var = customtkinter.BooleanVar(value=True)
        self.switch_status = CTkSwitch(master=self.filter_frame, text="Любая / Действующая",
                                       variable=self.switch_status_var,
                                       onvalue=True, offvalue=False)

        self.button_search = CTkButton(master=self.filter_frame, text="Поиск")
        self.button_search.bind("<Button-1>", self.btn_func)

        # frame with table that display information
        self.table_frame = ScrollableFrame(master=self.main_frame, bg_color="WHITE")
        self.table_frame.bind("<Button-1>", self.choose_window)

        # pack all elements, make grid
        self.main_frame.pack(expand=True, fill=BOTH)

        self.main_frame.columnconfigure(index=0, weight=2)
        self.main_frame.columnconfigure(index=1, weight=8)

        # grid filters elements
        self.filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        self.filter_frame.columnconfigure(index=0, weight=2)
        self.filter_frame.columnconfigure(index=1, weight=8)

        self.label_full_name.grid(row=0, column=0, padx=5, pady=5, sticky=NW)
        self.entry_full_name.grid(row=1, column=0, padx=5, pady=5, sticky=EW, columnspan=2)

        self.label_date_reg.grid(row=3, column=0, padx=5, pady=5, sticky=NW)
        self.entry_date_reg.grid(row=4, column=0, padx=5, pady=5, sticky=EW)

        self.label_region.grid(row=5, column=0, padx=5, pady=5, sticky=NW)
        self.entry_region.grid(row=6, column=0, padx=5, pady=5, sticky=EW, columnspan=2)

        self.label_town.grid(row=7, column=0, padx=5, pady=5, sticky=NW)
        self.entry_town.grid(row=8, column=0, padx=5, pady=5, sticky=EW, columnspan=2)

        self.label_main_okved.grid(row=9, column=0, padx=5, pady=5, sticky=NW)
        self.entry_main_okved.grid(row=10, column=0, padx=5, pady=5, sticky=EW, columnspan=2)

        self.label_additional_okved.grid(row=11, column=0, padx=5, pady=5, sticky=NW)
        self.entry_additional_okved.grid(row=12, column=0, padx=5, pady=5, sticky=EW, columnspan=2)

        self.label_status.grid(row=13, column=0, padx=5, pady=5, sticky=NW)
        self.switch_status.grid(row=14, column=0, padx=5, pady=5, sticky=EW)

        self.button_search.grid(row=15, column=1, padx=5, pady=5, sticky=SE)

        # grid table
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

    def choose_window(self, event):
        delta_x = self.winfo_x()
        delta_y = self.winfo_y()

        delta_x -= event.x_root
        delta_y -= event.y_root

        def move_window(event):
            self.geometry(
                f"{self.winfo_width()}x{self.winfo_height()}+{event.x_root + delta_x}+{event.y_root + delta_y}")

        self.main_frame.bind("<B1-Motion>", move_window)
        self.filter_frame.bind("<B1-Motion>", move_window)
        self.table_frame.bind("<B1-Motion>", move_window)

    def window_event(self, event):
        self.filter_frame.configure(height=self.winfo_height())
        self.table_frame.configure(height=self.winfo_height())

    def btn_func(self, event):
        print(event)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
