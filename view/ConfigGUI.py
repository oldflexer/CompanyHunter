import customtkinter as ctk
import logging

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
LMB = "<Button-1>"
LMM = "<B1-Motion>"


class ConfigGUI(ctk.CTkToplevel):
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
            super().__init__()

            self.geometry(
                f"{self.winfo_screenwidth() // 3}x{self.winfo_screenheight() // 3}+{self.winfo_screenwidth() // 3}+{self.winfo_screenheight() // 3}")

            # set miscellaneous properties
            self.title("Настройки")
            # self.iconbitmap("assets/company.ico")
            self.after(200, lambda: self.iconbitmap("assets/company.ico"))
            self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())

            # set font for application widgets
            self.label_font = ctk.CTkFont(family="Calibri", size=16)
            self.entry_font = ctk.CTkFont(family="Calibri", size=14)

            # main frame that allows to drag by any part of window and master for other widgets
            self.main_frame = ctk.CTkFrame(master=self)
            self.main_frame.bind(LMB, self.choose_window)

            # settings elements
            self.label_data_path = ctk.CTkLabel(master=self.main_frame, text="Данные расположены в",
                                                font=self.label_font)
            self.entry_data_path = ctk.CTkEntry(master=self.main_frame, font=self.entry_font)

            self.label_xlsx_path = ctk.CTkLabel(master=self.main_frame, text="Сохранять xlsx в",
                                                font=self.label_font)
            self.entry_xlsx_path = ctk.CTkEntry(master=self.main_frame, font=self.entry_font)

            # settings buttons
            self.button_save = ctk.CTkButton(master=self.main_frame, text="Сохранить", font=self.label_font)
            self.button_exit = ctk.CTkButton(master=self.main_frame, text="Отмена", font=self.label_font,
                                             command=self.dismiss)

            # setting user grab
            self.grab_set()

            self.logger.info("init successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def pack_all(self):
        try:
            self.logger.info("pack_all started")
            self.main_frame.pack(expand=True, fill=ctk.BOTH)
            self.label_data_path.pack(expand=False, padx=10, pady=10, anchor=ctk.W)
            self.entry_data_path.pack(expand=False, fill=ctk.BOTH, padx=10, anchor=ctk.W)
            self.label_xlsx_path.pack(expand=False, padx=10, pady=10, anchor=ctk.W)
            self.entry_xlsx_path.pack(expand=False, fill=ctk.BOTH, padx=10, anchor=ctk.W)
            self.button_save.pack(side=ctk.LEFT, expand=True, padx=10, pady=10, anchor=ctk.SW)
            self.button_exit.pack(side=ctk.RIGHT, expand=True, padx=10, pady=10, anchor=ctk.SE)
            self.logger.info("pack_all successfully completed")

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

        except Exception as exception:
            self.logger.exception(exception)

    def set_ctrl(self, ctrl):
        try:
            self.button_save.configure(command=ctrl.save_config)
        except Exception as exception:
            self.logger.exception(exception)

    def dismiss(self):
        try:
            self.grab_release()
            self.destroy()
        except Exception as exception:
            self.logger.exception(exception)
