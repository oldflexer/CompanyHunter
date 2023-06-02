import logging

from customtkinter import CTkScrollableFrame


class ScrollableFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
            super().__init__(master, **kwargs)
            self.logger.info("init successfully completed")
        except Exception as exception:
            self.logger.exception(exception)
