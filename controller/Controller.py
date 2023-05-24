import datetime
import threading
import time
import configparser
import xlsxwriter

from customtkinter import StringVar, BooleanVar

import view.ConfigGUI


def short_filename(filename):
    temp = filename[::-1]
    temp = temp[:temp.find("\\")]
    return temp[::-1]


class Controller:
    def __init__(self, repo, view, config_path="config.ini"):
        self.repo = repo
        self.view = view
        self.config_gui = None
        self.list_companies = []
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.config_data_path = self.config["Repository"]["DataPath"]

        self.repo.load_data(self.config_data_path)

        self.list_archives = self.repo.archive_list
        self.index_current_archive = 0
        self.name_current_archive = short_filename(self.list_archives[self.index_current_archive].filename)

        self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
        self.index_current_xml = 0
        self.name_current_xml = self.list_xmls[self.index_current_xml]

        self.full_name = StringVar()
        self.date_reg = StringVar()
        self.region = StringVar()
        self.town = StringVar()
        self.main_okved = StringVar()
        self.additional_okved = StringVar()

        self.status = BooleanVar(value=True)
        self.email = BooleanVar(value=False)

        self.update_labels()
        # self.search()

    def update_labels(self):
        self.view.filter_frame.label_current_archive.configure(text=f"{self.name_current_archive} | {self.index_current_archive+1}/{len(self.list_archives)}")
        self.view.filter_frame.label_current_xml.configure(text=f"{self.name_current_xml} | {self.index_current_xml+1}/{len(self.list_xmls)}")

    def prev_archive(self):
        if self.index_current_archive >= 1:
            self.index_current_archive -= 1
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = len(self.list_xmls) - 1
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.index_current_archive = len(self.list_archives) - 1
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = len(self.list_xmls) - 1
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()

    def next_archive(self):
        if self.index_current_archive < len(self.list_archives) - 1:
            self.index_current_archive += 1
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = 0
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.index_current_archive = 0
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = 0
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()

    def prev_file_x10(self):
        if self.index_current_xml >= 10:
            self.index_current_xml -= 10
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.prev_archive()

    def prev_file(self):
        if self.index_current_xml >= 1:
            self.index_current_xml -= 1
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.prev_archive()

    def next_file_x10(self):
        if self.index_current_xml < len(self.list_xmls) - 10:
            self.index_current_xml += 10
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.next_archive()

    def next_file(self):
        if self.index_current_xml < len(self.list_xmls) - 1:
            self.index_current_xml += 1
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
        else:
            self.next_archive()

    def search(self):
        self.view.clear_table()
        # self.repo.start_getting_companies(archive_index=1, controller=self)
        # print(self.list_archives[self.index_current_archive].filename)
        # print(self.name_current_xml)
        self.list_companies = list(self.repo.get_companies(archive_index=self.index_current_archive,
                                                           xml_name=self.name_current_xml,
                                                           controller=self))

        for company in self.list_companies:
            # print(company)
            self.view.add_company(company)

        self.update_labels()

    def open_config_window(self):
        self.config_gui = view.ConfigGUI.ConfigGUI()
        self.config_gui.set_ctrl(self)
        self.config_gui.entry_data_path.insert(0, self.config_data_path)
        self.config_gui.pack_all()

    def save_config(self):
        self.config_data_path = self.config_gui.entry_data_path.get()
        self.config["Repository"]["DataPath"] = self.config_data_path

        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

        self.config_gui.dismiss()

    def save_xlsx(self):
        workbook = xlsxwriter.Workbook(f"{self.name_current_xml}.xlsx")
        worksheet = workbook.add_worksheet()

        column = 0
        for key in self.list_companies[0].__dict__.keys():
            worksheet.write(0, column, key)
            column += 1

        row = 1
        column = 0
        for company in self.list_companies:
            for key in company.__dict__.keys():
                worksheet.write(row, column, company.__getattribute__(key))
                column += 1

            row += 1
            column = 0

        workbook.close()
