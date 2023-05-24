import customtkinter as ctk
import model.Company as Company
import view.Table as Table
import view.Filter as Filter
import threading

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ConfigGUI(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry(
            f"{self.winfo_screenwidth()//2}x{self.winfo_screenheight()//2}")

        # set miscellaneous properties
        self.title("Настройки")
        self.iconbitmap("assets/company.ico")

        # set font for application widgets
        self.label_font = ctk.CTkFont(family="Calibri", size=16)
        self.entry_font = ctk.CTkFont(family="Calibri", size=14)

        # main frame that allows to drag by any part of window and master for other widgets
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.bind(LMB, self.choose_window)

        # settings elements
        self.label_data_path = ctk.CTkLabel(master=self.main_frame, text="Расположение данных",
                                            font=self.label_font)
        self.entry_data_path = ctk.CTkEntry(master=self.main_frame, font=self.entry_font)

        # settings buttons
        self.button_save = ctk.CTkButton(master=self.main_frame, text="Сохранить", font=self.label_font)
        self.button_exit = ctk.CTkButton(master=self.main_frame, text="Отмена", font=self.label_font)

    def pack_all(self):
        self.main_frame.pack(expand=True, fill=ctk.BOTH)
        self.label_data_path.pack(expand=True)
        self.entry_data_path.pack(expand=True)
        self.button_save.pack(side=ctk.LEFT)
        self.button_exit.pack(side=ctk.RIGHT)

    def choose_window(self, event):
        delta_x = self.winfo_x()
        delta_y = self.winfo_y()

        delta_x -= event.x_root
        delta_y -= event.y_root

        def move_window(event):
            self.geometry(
                f"{self.winfo_width()}x{self.winfo_height()}+{event.x_root + delta_x}+{event.y_root + delta_y}")

        self.main_frame.bind(LMM, move_window)