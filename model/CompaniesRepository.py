import model.Company
import logging
import os
import threading
import concurrent.futures
from xml.etree import ElementTree
from zipfile import ZipFile


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


class CompaniesRepository(object):
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
            self.data_path = None
            self.directory_list = None
            self.archive_list = None
            self.logger.info("init successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def load_data(self, data_path):
        try:
            self.logger.info("load_data started")
            self.data_path = data_path

            if os.path.isdir(self.data_path):
                self.directory_list = os.listdir(self.data_path)
                self.archive_list = list(self.find_archive_list())
                self.logger.info("load_data successfully completed")
            else:
                self.directory_list = None
                self.archive_list = None
                self.logger.warning("load_data did not completed correctly")

        except Exception as exception:
            self.logger.exception(exception)

    def find_archive_list(self):
        try:
            self.logger.info("find_archive_list started")
            for filename in self.directory_list:
                if filename.endswith(".zip"):
                    yield ZipFile(os.path.join(self.data_path, filename), "r")
            self.logger.info("find_archive_list successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def find_xml_list(self, archive_index):
        try:
            self.logger.info("find_xml_list started")
            result = self.archive_list[archive_index].namelist()
            self.logger.info("find_xml_list successfully completed")
            return result
        except Exception as exception:
            print(exception)

    def get_xml_data(self, archive_index, xml_name):
        try:
            self.logger.info("get_xml_data started")

            if self.archive_list is not None and archive_index is not None and xml_name is not None:
                xml_bytes = self.archive_list[archive_index].read(xml_name)
                xml_data = str(xml_bytes, encoding="windows-1251")
                self.logger.info("get_xml_data successfully completed")
            else:
                xml_bytes = None
                xml_data = None
                self.logger.warning("get_xml_data did not complete correctly")

            return xml_data
        except Exception as exception:
            self.logger.exception(exception)

    def find_small_name(self, company):
        try:
            if company.find("СвНаимЮЛ") is not None:
                if company.find("СвНаимЮЛ").find("СвНаимЮЛСокр") is not None:
                    small_name = company.find("СвНаимЮЛ").find("СвНаимЮЛСокр").get("НаимСокр")
                else:
                    small_name = ""
            else:
                small_name = ""
            return small_name
        except Exception as exception:
            self.logger.exception(exception)

    def find_full_name(self, company):
        try:
            if company.find("СвНаимЮЛ") is not None:
                full_name = company.find("СвНаимЮЛ").get("НаимЮЛПолн")
            else:
                full_name = ""
            return full_name
        except Exception as exception:
            self.logger.exception(exception)

    def find_email(self, company):
        try:
            if company.find("СвАдрЭлПочты") is not None:
                email = company.find("СвАдрЭлПочты").get("E-mail")
            else:
                email = ""
            return email
        except Exception as exception:
            self.logger.exception(exception)

    def find_inn(self, company):
        try:
            inn = company.get("ИНН")
            return inn
        except Exception as exception:
            self.logger.exception(exception)

    def find_date_reg(self, company):
        try:
            if company.find("СвРегОрг") is not None:
                if company.find("СвРегОрг").find("ГРНДата") is not None:
                    date_reg = company.find("СвРегОрг").find("ГРНДата").get("ДатаЗаписи")
                else:
                    date_reg = ""
            else:
                date_reg = ""
            return date_reg
        except Exception as exception:
            self.logger.exception(exception)

    def find_address_type(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС") is not None:
                    address_type = "ЮЛФИАС"
                elif company_address_info.find("АдресРФ") is not None:
                    address_type = "Классический"
                else:
                    address_type = None
            else:
                address_type = None
            return address_type
        except Exception as exception:
            self.logger.exception(exception)

    def find_region(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("АдресРФ") is not None:
                    if company_address_info.find("АдресРФ").find("Регион") is not None:
                        region = company_address_info.find("АдресРФ").find("Регион").get("НаимРегион")
                    else:
                        region = ""
                else:
                    region = ""
            else:
                region = ""
            return region
        except Exception as exception:
            self.logger.exception(exception)

    def find_town(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("АдресРФ") is not None:
                    if company_address_info.find("АдресРФ").find("Город") is not None:
                        town = company_address_info.find("АдресРФ").find("Город").get("НаимГород")
                    else:
                        town = ""
                else:
                    town = ""
            else:
                town = ""
            return town
        except Exception as exception:
            self.logger.exception(exception)

    def find_locality(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("АдресРФ") is not None:
                    if company_address_info.find("АдресРФ").find("НаселПункт") is not None:
                        town = company_address_info.find("АдресРФ").find("НаселПункт").get("НаимНаселПункт")
                    else:
                        town = ""
                else:
                    town = ""
            else:
                town = ""
            return town
        except Exception as exception:
            self.logger.exception(exception)

    def find_street(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("АдресРФ").find("Улица") is not None:
                    street = company_address_info.find("АдресРФ").find("Улица").get("НаимУлица")
                else:
                    street = ""
            else:
                street = ""
            return street
        except Exception as exception:
            self.logger.exception(exception)

    def find_building(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                building = company_address_info.find("АдресРФ").attrib.get("Дом", "")
            else:
                building = ""
            return building
        except Exception as exception:
            self.logger.exception(exception)

    def find_apartments(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                apartments = company_address_info.find("АдресРФ").attrib.get("Кварт", "")
            else:
                apartments = ""
            return apartments
        except Exception as exception:
            self.logger.exception(exception)

    def find_region_v2(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС") is not None:
                    if company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион") is not None:
                        region = company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион").text
                    else:
                        region = ""
                else:
                    region = ""
            else:
                region = ""
            return region
        except Exception as exception:
            self.logger.exception(exception)

    def find_town_v2(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт") is not None:
                    town = company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт").get("Наим")
                else:
                    town = ""
            else:
                town = ""
            return town
        except Exception as exception:
            self.logger.exception(exception)

    def find_street_v2(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети") is not None:
                    street = company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети").get("Наим")
                else:
                    street = ""
            else:
                street = ""
            return street
        except Exception as exception:
            self.logger.exception(exception)

    def find_building_v2(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС").find("Здание") is not None:
                    building = company_address_info.find("СвАдрЮЛФИАС").find("Здание").get("Номер")
                else:
                    building = ""
            else:
                building = ""
            return building
        except Exception as exception:
            self.logger.exception(exception)

    def find_apartments_v2(self, company):
        try:
            if company.find("СвАдресЮЛ") is not None:
                company_address_info = company.find("СвАдресЮЛ")
                if company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания") is not None:
                    apartments = company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания").get("Номер")
                else:
                    apartments = ""
            else:
                apartments = ""
            return apartments
        except Exception as exception:
            self.logger.exception(exception)

    def find_company_people_info(self, company):
        try:
            if company.find("СведДолжнФЛ") is not None:
                company_people_info = company.find("СведДолжнФЛ")
            else:
                company_people_info = None
            return company_people_info
        except Exception as exception:
            self.logger.exception(exception)

    def find_director_surname(self, company_people_info):
        try:
            if company_people_info is not None:
                if company_people_info.find("СвФЛ") is not None:
                    director_surname = company_people_info.find("СвФЛ").get("Фамилия")
                else:
                    director_surname = ""
            else:
                director_surname = ""
            return director_surname
        except Exception as exception:
            self.logger.exception(exception)

    def find_director_name(self, company_people_info):
        try:
            if company_people_info is not None:
                if company_people_info.find("СвФЛ") is not None:
                    director_name = company_people_info.find("СвФЛ").get("Имя")
                else:
                    director_name = ""
            else:
                director_name = ""
            return director_name
        except Exception as exception:
            self.logger.exception(exception)

    def find_director_second_name(self, company_people_info):
        try:
            if company_people_info is not None:
                if company_people_info.find("СвФЛ") is not None:
                    director_second_name = company_people_info.find("СвФЛ").get("Отчество")
                else:
                    director_second_name = ""
            else:
                director_second_name = ""
            return director_second_name
        except Exception as exception:
            self.logger.exception(exception)

    def find_main_okved(self, company):
        try:
            if company.find("СвОКВЭД") is not None:
                company_okved_info = company.find("СвОКВЭД")
                if company_okved_info.find("СвОКВЭДОсн") is not None:
                    main_okved = f'{company_okved_info.find("СвОКВЭДОсн").get("КодОКВЭД")} {company_okved_info.find("СвОКВЭДОсн").get("НаимОКВЭД")}'
                else:
                    main_okved = ""
            else:
                main_okved = ""
            return main_okved
        except Exception as exception:
            self.logger.exception(exception)

    def find_additional_okved(self, company):
        try:
            if company.find("СвОКВЭД") is not None:
                company_okved_info = company.find("СвОКВЭД")
                if company_okved_info.findall("СвОКВЭДДоп") is not None:
                    additional_okved = [okved.get("КодОКВЭД") for okved in company_okved_info.findall("СвОКВЭДДоп")]
                else:
                    additional_okved = []
            else:
                additional_okved = []
            return additional_okved
        except Exception as exception:
            self.logger.exception(exception)

    def find_company_status(self, company):
        try:
            if company.find("СвПрекрЮЛ") is not None:
                company_status = False
            else:
                company_status = True
            return company_status
        except Exception as exception:
            self.logger.exception(exception)

    @threaded_future
    def get_companies(self, archive_index, xml_name):
        try:
            self.logger.info("get_companies started")

            list_companies = []

            xml_data = self.get_xml_data(archive_index, xml_name)
            if xml_data is None:
                self.logger.warning("get_companies did not complete correctly")
                return

            egrul_root = ElementTree.fromstring(xml_data)
            companies_xml = egrul_root.findall("СвЮЛ")

            for company_xml in companies_xml:
                new_company = model.Company.Company()

                new_company.name = self.find_small_name(company_xml)
                if new_company.name == "":
                    new_company.name = self.find_full_name(company_xml)

                new_company.email = self.find_email(company_xml)

                new_company.inn = self.find_inn(company_xml)

                new_company.date_reg = self.find_date_reg(company_xml)

                match self.find_address_type(company_xml):
                    case "Классический":
                        new_company.region = self.find_region(company_xml)
                        new_company.town = self.find_town(company_xml)
                        if new_company.town == "":
                            new_company.town = self.find_locality(company_xml)
                        new_company.street = self.find_street(company_xml)
                        new_company.building = self.find_building(company_xml)
                        new_company.apartments = self.find_apartments(company_xml)

                    case "ЮЛФИАС":
                        new_company.region = self.find_region_v2(company_xml)
                        new_company.town = self.find_town_v2(company_xml)
                        if new_company.town == "":
                            new_company.town = self.find_locality(company_xml)
                        new_company.street = self.find_street_v2(company_xml)
                        new_company.building = self.find_building_v2(company_xml)
                        new_company.apartments = self.find_apartments_v2(company_xml)

                    case _:
                        new_company.region = ""
                        new_company.town = ""
                        new_company.street = ""
                        new_company.building = ""
                        new_company.apartments = ""

                company_people_info = self.find_company_people_info(company_xml)
                director_surname = self.find_director_surname(company_people_info)
                director_name = self.find_director_name(company_people_info)
                director_second_name = self.find_director_second_name(company_people_info)
                new_company.director = f"{director_surname} {director_name} {director_second_name}"

                new_company.main_okved = self.find_main_okved(company_xml)

                new_company.additional_okved = self.find_additional_okved(company_xml)
                new_company.additional_okved = "; ".join(new_company.additional_okved)

                new_company.status = self.find_company_status(company_xml)

                list_companies.append(new_company)

            self.logger.info("get_companies successfully completed")
            return list_companies

        except Exception as exception:
            self.logger.exception(exception)
