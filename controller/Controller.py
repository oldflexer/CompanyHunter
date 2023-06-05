import configparser
import xlsxwriter
import view.ConfigGUI
import logging
import os
import controller.ParserRPN
import threading
import concurrent.futures
from customtkinter import StringVar, BooleanVar, ThemeManager


def shorten_filename(filename):
    temp = filename[::-1]
    temp = temp[:temp.find("\\")]
    return temp[::-1]


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def call_with_future(func, future, args, kwargs):
    try:
        result = func(*args, **kwargs)
        future.set_result(result)
    except Exception as exception:
        future.set_exception(exception)


def threaded_future(func):
    def wrapper(*args, **kwargs):
        future = concurrent.futures.Future()
        threading.Thread(target=call_with_future, args=(func, future, args, kwargs)).start()
        return future
    return wrapper


class Controller:
    def __init__(self, repo, view, config_path="config.ini"):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
            self.repo = repo
            self.view = view
            self.config_gui = None
            self.list_companies = []

            self.full_name = StringVar()
            self.date_reg = StringVar()
            self.region = StringVar()
            self.town = StringVar()
            self.main_okved = StringVar()
            self.additional_okved = StringVar()
            self.status = BooleanVar(value=True)
            self.email = BooleanVar(value=False)

            self.config = configparser.ConfigParser()
            self.config_data_path = None
            self.config_xlsx_path = None
            self.load_config(config_path)

            self.list_archives = None
            self.index_current_archive = None
            self.name_current_archive = None
            self.list_xmls = None
            self.index_current_xml = None
            self.name_current_xml = None

            self.load_data()
            self.search()

            self.logger.info("init successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def load_data(self):
        self.repo.load_data(self.config_data_path)
        self.list_archives = self.repo.archive_list
        self.index_current_archive = 0

        if self.list_archives is not None:
            self.name_current_archive = shorten_filename(self.list_archives[self.index_current_archive].filename)
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = 0
            self.name_current_xml = self.list_xmls[self.index_current_xml]
        else:
            self.name_current_archive = None
            self.list_xmls = None
            self.index_current_xml = None
            self.name_current_xml = None

        self.update_labels()

    def load_config(self, config_path):
        try:
            self.logger.info("load_config started")
            self.config.read(config_path)
            self.config_data_path = self.load_data_config()
            self.config_xlsx_path = self.load_xlsx_config()
            self.logger.info("load_config completed correctly")
        except Exception as exception:
            self.logger.exception(exception)

    def load_data_config(self):
        try:
            self.logger.info("load_data_config started")
            config_data_path = self.config["Repository"]["datapath"]
            self.logger.info("load_data_config completed correctly")
            return config_data_path
        except Exception as exception:
            self.logger.exception(exception)

    def load_xlsx_config(self):
        try:
            self.logger.info("load_xlsx_config started")
            config_xlsx_path = self.config["Excel"]["savepath"]
            self.logger.info("load_xlsx_config completed correctly")
            return config_xlsx_path
        except Exception as exception:
            self.logger.exception(exception)

    def update_labels(self):
        try:
            self.logger.info("update_labels started")

            if self.name_current_archive is None or self.index_current_archive is None or self.list_archives is None:
                self.logger.warning("update_labels did not complete correctly")
                return
            self.view.filter_frame.label_current_archive.configure(
                text=f"{self.name_current_archive} | {self.index_current_archive + 1}/{len(self.list_archives)}")

            if self.name_current_xml is None or self.index_current_xml is None or self.list_xmls is None:
                self.logger.warning("update_labels did not complete correctly")
                return
            self.view.filter_frame.label_current_xml.configure(
                text=f"{self.name_current_xml} | {self.index_current_xml + 1}/{len(self.list_xmls)}")

            self.logger.info("update_labels successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def prev_archive(self):
        try:
            self.logger.info("prev_archive started")

            if self.index_current_archive is None or self.list_archives is None:
                self.logger.warning("prev_archive did not complete correctly")
                return

            if self.index_current_archive >= 1:
                self.index_current_archive -= 1
            else:
                self.index_current_archive = len(self.list_archives) - 1

            self.name_current_archive = shorten_filename(self.list_archives[self.index_current_archive].filename)
            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = len(self.list_xmls) - 1
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
            self.logger.info("prev_archive successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def next_archive(self):
        try:
            self.logger.info("next_archive started")

            if self.index_current_archive is None or self.list_archives is None:
                self.logger.warning("next_archive did not complete correctly")
                return

            if self.index_current_archive < len(self.list_archives) - 1:
                self.index_current_archive += 1
                self.name_current_archive = shorten_filename(self.list_archives[self.index_current_archive].filename)
            else:
                self.index_current_archive = 0
                self.name_current_archive = shorten_filename(self.list_archives[self.index_current_archive].filename)

            self.list_xmls = self.repo.find_xml_list(self.index_current_archive)
            self.index_current_xml = 0
            self.name_current_xml = self.list_xmls[self.index_current_xml]
            self.search()
            self.logger.info("next_archive successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def prev_file_x10(self):
        try:
            self.logger.info("prev_file_x10 started")

            if self.index_current_xml is None or self.list_xmls is None or self.index_current_xml is None:
                self.logger.warning("prev_file_x10 did not complete correctly")
                return

            if self.index_current_xml >= 10:
                self.index_current_xml -= 10
                self.name_current_xml = self.list_xmls[self.index_current_xml]
                self.search()
            else:
                self.prev_archive()

            self.logger.info("prev_file_x10 successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def prev_file(self):
        try:
            self.logger.info("prev_file started")

            if self.index_current_xml is None or self.list_xmls is None or self.index_current_xml is None:
                self.logger.warning("prev_file did not complete correctly")
                return

            if self.index_current_xml >= 1:
                self.index_current_xml -= 1
                self.name_current_xml = self.list_xmls[self.index_current_xml]
                self.search()
            else:
                self.prev_archive()

            self.logger.info("prev_file successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def next_file_x10(self):
        try:
            self.logger.info("next_file_x10 started")

            if self.index_current_xml is None or self.list_xmls is None or self.index_current_xml is None:
                self.logger.warning("next_file_x10 did not complete correctly")
                return

            if self.index_current_xml < len(self.list_xmls) - 10:
                self.index_current_xml += 10
                self.name_current_xml = self.list_xmls[self.index_current_xml]
                self.search()
            else:
                self.next_archive()

            self.logger.info("next_file_x10 successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def next_file(self):
        try:
            self.logger.info("next_file started")

            if self.index_current_xml is None or self.list_xmls is None:
                self.logger.warning("next_file did not complete correctly")
                return

            if self.index_current_xml < len(self.list_xmls) - 1:
                self.index_current_xml += 1
                self.name_current_xml = self.list_xmls[self.index_current_xml]
                self.search()
            else:
                self.next_archive()

            self.logger.info("next_file successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    @threaded_future
    def filter_companies(self):
        try:
            self.logger.info("filter_companies started")

            if self.list_companies is None:
                raise Exception

            list_companies = []

            for company in self.list_companies:
                if self.full_name.get() and self.full_name.get() not in company.name:
                    continue

                if self.email.get() and company.email == "":
                    continue

                if self.date_reg.get() and self.date_reg.get() != company.date_reg:
                    continue

                if self.region.get() and self.region.get() not in company.region:
                    continue

                if self.town.get() and self.town.get() != company.town:
                    continue

                if self.main_okved.get():
                    try:
                        if company.main_okved.index(self.main_okved.get()) != 0:
                            continue
                    except ValueError:
                        continue

                if self.additional_okved.get():
                    flag = False
                    for okved in company.additional_okved:
                        try:
                            if okved.index(self.additional_okved.get()) != 0:
                                continue
                        except ValueError:
                            continue
                        else:
                            flag = True
                    if not flag:
                        continue

                if self.status.get() and self.status.get() != company.status:
                    continue

                match company.status:
                    case False:
                        company.status = "Нет"
                    case True:
                        company.status = "Да"
                    case _:
                        company.status = "Не опр"

                list_companies.append(company)

            self.logger.info("filter_companies successfully completed")
            return list_companies

        except Exception as exception:
            self.logger.exception(exception)

    @threaded
    def search(self):
        try:
            self.logger.info("search started")

            self.view.filter_frame.switch_buttons()
            self.view.clear_table()
            self.update_labels()
            self.list_companies = self.repo.get_companies(archive_index=self.index_current_archive, xml_name=self.name_current_xml).result()
            self.list_companies = self.filter_companies().result()

            if self.list_companies is None:
                raise Exception

            for company in self.list_companies:
                self.view.add_company(company)

            self.view.filter_frame.switch_buttons()

            self.logger.info("search successfully completed")

        except Exception as exception:
            self.logger.exception(exception)
            self.view.filter_frame.switch_buttons()

    @threaded
    def open_config_window(self):
        try:
            self.logger.info("open_config_window started")
            self.config_gui = view.ConfigGUI.ConfigGUI()
            self.config_gui.set_ctrl(self)
            self.config_gui.entry_data_path.insert(0, self.config_data_path)
            self.config_gui.entry_xlsx_path.insert(0, self.config_xlsx_path)
            self.config_gui.pack_all()
            self.config_gui.focus()
            self.logger.info("open_config_window successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    def save_config(self):
        try:
            self.logger.info("save_config started")

            self.config_data_path = self.config_gui.entry_data_path.get()
            self.config_xlsx_path = self.config_gui.entry_xlsx_path.get()

            match os.path.isdir(self.config_data_path), os.path.isdir(self.config_xlsx_path):
                case False, False:
                    self.config_gui.entry_data_path.configure(border_color="RED")
                    self.config_gui.entry_xlsx_path.configure(border_color="RED")
                    self.logger.warning("save_config did not complete correctly")
                    return
                case False, True:
                    self.config_gui.entry_data_path.configure(border_color="RED")
                    self.config_gui.entry_xlsx_path.configure(
                        border_color=ThemeManager.theme["CTkEntry"]["border_color"])
                    self.logger.warning("save_config did not complete correctly")
                    return
                case True, False:
                    self.config_gui.entry_data_path.configure(
                        border_color=ThemeManager.theme["CTkEntry"]["border_color"])
                    self.config_gui.entry_xlsx_path.configure(border_color="RED")
                    self.logger.warning("save_config did not complete correctly")
                    return
                case True, True:
                    self.config_gui.entry_data_path.configure(
                        border_color=ThemeManager.theme["CTkEntry"]["border_color"])
                    self.config_gui.entry_xlsx_path.configure(
                        border_color=ThemeManager.theme["CTkEntry"]["border_color"])

            self.config["Repository"]["datapath"] = self.config_data_path
            self.config["Excel"]["savepath"] = self.config_xlsx_path

            with open("config.ini", "w") as configfile:
                self.config.write(configfile)

            self.config_gui.dismiss()
            self.load_config("config.ini")
            self.load_data()
            self.search()
            self.logger.info("save_config successfully completed")

        except Exception as exception:
            self.logger.exception(exception)

    @threaded
    def save_xlsx(self):
        try:
            self.logger.info("save_xlsx started")

            if self.config_xlsx_path is None or self.name_current_xml is None:
                self.logger.warning("save_xlsx did not complete correctly")
                return

            workbook = xlsxwriter.Workbook(f"{self.config_xlsx_path}\\{self.name_current_xml}.xlsx")
            worksheet = workbook.add_worksheet()

            column = 0
            for key in self.list_companies[0].__dict__.keys():
                worksheet.write(0, column, key)
                column += 1

            row = 1
            column = 0

            if self.list_companies is None:
                raise Exception

            for company in self.list_companies:
                parser = controller.ParserRPN.ParserRPN()
                response_dict = parser.parse_RPN(company)

                wastes_licenses = []
                for waste_license in response_dict["data"]:
                    for place in waste_license["places_summary"]:
                        wastes_licenses.append(f"Тип: {place['name']}; Классы: {','.join(place['classes'])}; Кол-во ФККО: {place['fkkos']}")

                if len(wastes_licenses) == 0:
                    wastes_licenses.append("Нет")

                wastes_licenses = "| ".join(wastes_licenses)

                company.wastes_licenses = wastes_licenses

                for attr in company.__dict__.keys():
                    match attr:
                        case "wastes_licenses":
                            worksheet.write_url(row,
                                                column,
                                                url=f"https://license.rpn.gov.ru/rpn/license-registry?pcurrent_page=1&pper_page=20&plast_page=1&fstatus=active&finn={company.__getattribute__('inn')}&oissuer_order_at=desc",
                                                string=company.__getattribute__(attr))
                        case "name":
                            worksheet.write_url(row,
                                                column,
                                                url=f"https://www.list-org.com/search?type=inn&val={company.__getattribute__('inn')}",
                                                string=company.__getattribute__(attr))
                        case _:
                            worksheet.write(row, column, company.__getattribute__(attr))

                    column += 1

                row += 1
                column = 0

            workbook.close()
            self.logger.info("save_xlsx successfully completed")

        except Exception as exception:
            self.logger.exception(exception)
