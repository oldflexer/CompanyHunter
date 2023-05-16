import datetime
import os
from xml.etree import ElementTree
from zipfile import ZipFile
import model.Company
import threading


class CompaniesRepository(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.directory_list = os.listdir(self.data_path)
        self.archive_list = list(self.find_archive_list())

    def find_archive_list(self):
        for filename in self.directory_list:
            if filename.endswith(".zip"):
                yield ZipFile(os.path.join(self.data_path, filename), "r")

    def find_xml_list(self, archive_index):
        # print(self.archive_list[archive_index].filename)
        return self.archive_list[archive_index].namelist()

    # def find_small_name(self, company):
    #     if company.find("СвНаимЮЛ") is not None:
    #         if company.find("СвНаимЮЛ").find("СвНаимЮЛСокр") is not None:
    #             company.small_name = company.find("СвНаимЮЛ").find("СвНаимЮЛСокр").get("НаимСокр")

    def get_companies(self, archive_index, xml_name, controller):
        xml_bytes = self.archive_list[archive_index].read(xml_name)
        xml_data = str(xml_bytes, encoding="windows-1251")

        egrul_root = ElementTree.fromstring(xml_data)
        companies = egrul_root.findall("СвЮЛ")

        for company in companies:
            new_company = model.Company.Company()

            if company.find("СвНаимЮЛ") is not None:
                if company.find("СвНаимЮЛ").find("СвНаимЮЛСокр") is not None:
                    new_company.small_name = company.find("СвНаимЮЛ").find("СвНаимЮЛСокр").get("НаимСокр")
                    if controller.full_name.get() and controller.full_name.get() not in new_company.small_name:
                        continue
                elif controller.full_name.get():
                    continue
            elif controller.full_name.get():
                continue

            if company.find("СвАдрЭлПочты") is not None:
                new_company.email = company.find("СвАдрЭлПочты").get("E-mail")
            elif controller.email.get():
                continue

            new_company.inn = company.get("ИНН")

            if company.find("СвРегОрг") is not None:
                if company.find("СвРегОрг").find("ГРНДата") is not None:
                    new_company.date_reg = company.find("СвРегОрг").find("ГРНДата").get("ДатаЗаписи")
                    if controller.date_reg.get() and controller.full_name.get() != new_company.date_reg:
                        continue
                elif controller.date_reg.get():
                    continue
            elif controller.date_reg.get():
                continue

            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("АдресРФ") is not None:
                    if company_address_info.find("АдресРФ").find("Регион") is not None:
                        new_company.region = company_address_info.find("АдресРФ").find("Регион").get("НаимРегион")
                        if controller.region.get() and controller.region.get() not in new_company.region:
                            continue
                    elif controller.region.get():
                        continue

                    if company_address_info.find("АдресРФ").find("Город") is not None:
                        new_company.town = company_address_info.find("АдресРФ").find("Город").get("НаимГород")
                        if controller.town.get() and controller.town.get() != new_company.town:
                            continue
                    elif controller.town.get():
                        continue

                    if company_address_info.find("АдресРФ").find("Улица") is not None:
                        new_company.street = company_address_info.find("АдресРФ").find("Улица").get("НаимУлица")

                    new_company.building = company_address_info.find("АдресРФ").attrib.get("Дом", None)
                    new_company.apartments = company_address_info.find("АдресРФ").attrib.get("Кварт", None)

                elif company_address_info.find("СвАдрЮЛФИАС") is not None:
                    if company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион") is not None:
                        new_company.region = company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион").text
                        if controller.region.get() and controller.region.get() not in new_company.region:
                            continue
                    elif controller.region.get():
                        continue

                    if company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт") is not None:
                        new_company.town = company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт").get("Наим")
                        if controller.town.get() and controller.town.get() != new_company.town:
                            continue
                    elif controller.town.get():
                        continue

                    if company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети") is not None:
                        new_company.street = company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети").get(
                            "Наим")

                    if company_address_info.find("СвАдрЮЛФИАС").find("Здание") is not None:
                        new_company.building = company_address_info.find("СвАдрЮЛФИАС").find("Здание").get("Номер")

                    if company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания") is not None:
                        new_company.apartments = company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания").get(
                            "Номер")

                elif controller.region.get() or controller.town.get():
                    continue
            elif controller.region.get() or controller.town.get():
                continue

            if company.find("СведДолжнФЛ") is not None:
                company_people_info = company.find("СведДолжнФЛ")

                director_surname = ""
                director_name = ""
                director_secondname = ""

                if company_people_info.find("СвФЛ") is not None:
                    director_surname = company_people_info.find("СвФЛ").get("Фамилия")

                if company_people_info.find("СвФЛ") is not None:
                    director_name = company_people_info.find("СвФЛ").get("Имя")

                if company_people_info.find("СвФЛ") is not None:
                    director_secondname = company_people_info.find("СвФЛ").get("Отчество")

                new_company.director = f"{director_surname} {director_name} {director_secondname}"

            if company.find("СвОКВЭД") is not None:
                company_okved_info = company.find("СвОКВЭД")
                if company_okved_info.find("СвОКВЭДОсн") is not None:
                    new_company.main_okved = f'{company_okved_info.find("СвОКВЭДОсн").get("КодОКВЭД")} {company_okved_info.find("СвОКВЭДОсн").get("НаимОКВЭД")}'
                    if controller.main_okved.get() and controller.main_okved.get() not in new_company.main_okved:
                        continue
                elif controller.main_okved.get():
                    continue

                if company_okved_info.findall("СвОКВЭДДоп") is not None:
                    additional_okved = [add_okved.get("КодОКВЭД") for add_okved in
                                        company_okved_info.findall("СвОКВЭДДоп")]
                    if controller.additional_okved.get():
                        flag = False
                        for okved in additional_okved:
                            if controller.additional_okved.get() in okved:
                                flag = True
                        if not flag:
                            continue
                    new_company.additional_okved = "; ".join(additional_okved)
                elif controller.additional_okved.get():
                    continue
            elif controller.main_okved.get() or controller.additional_okved.get():
                continue

            new_company.status = True
            if company.find("СвПрекрЮЛ") is not None:
                new_company.status = False
                if controller.status.get() and controller.status.get() != new_company.status:
                    continue

            match new_company.status:
                case False:
                    new_company.status = "Нет"
                case True:
                    new_company.status = "Да"
                case _:
                    new_company.status = "Не опр"

            yield new_company
        # break

    # def start_getting_companies(self, archive_index, controller):
    #     self.thread = threading.Thread(target=self.get_companies, args=(archive_index, controller), daemon=False)
    #     print(threading.main_thread().name)
    #     print(self.thread.name)
    #     self.thread.start()
    #     # self.check_thread(self.thread)

    # def check_thread(self, thread):
    #     if thread.is_alive():
    #         print(f"{datetime.datetime.now()} | TASK RUNNING")
    #         self.view.after(500, lambda: self.check_thread(thread))
    #     else:
    #         print(f"{datetime.datetime.now()} | TASK COMPLETED")
