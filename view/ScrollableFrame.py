from customtkinter import CTkScrollableFrame


class ScrollableFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
