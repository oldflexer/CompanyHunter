import os
from xml.etree import ElementTree
from zipfile import ZipFile
import model.Company


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
        print(self.archive_list[archive_index].filename)
        return self.archive_list[archive_index].namelist()

    def get_companies(self, archive_index, controller):
        xml_list = self.find_xml_list(archive_index)

        temp = 0
        for xml_name in xml_list:
            temp += 1
            print(xml_name)
            xml_bytes = self.archive_list[archive_index].read(xml_name)
            xml_data = str(xml_bytes, encoding="windows-1251")

            egrul_root = ElementTree.fromstring(xml_data)
            companies = egrul_root.findall("СвЮЛ")

            for company in companies:
                small_name = None
                inn = None
                kpp = None
                date_reg = None
                region = None
                town = None
                street = None
                building = None
                apartments = None
                director = None
                main_okved = None
                additional_okved = None
                status = None

                if company.find("СвНаимЮЛ") is not None:
                    if company.find("СвНаимЮЛ").find("СвНаимЮЛСокр") is not None:
                        small_name = company.find("СвНаимЮЛ").find("СвНаимЮЛСокр").get("НаимСокр")
                        if controller.full_name.get() and controller.full_name.get() not in small_name:
                            continue

                # print("!!!!!", company.find("СвРегОрг").find("ГРНДата").get("ДатаЗаписи"))
                # print(company.find("СвРегОрг").find("ГРНДата"))
                if company.find("СвРегОрг") is not None:
                    if company.find("СвРегОрг").find("ГРНДата") is not None:
                        date_reg = company.find("СвРегОрг").find("ГРНДата").get("ДатаЗаписи")
                        if controller.date_reg.get() and controller.full_name.get() != date_reg:
                            continue

                if company.find("СвАдресЮЛ") is not None:
                    company_address_info = company.find("СвАдресЮЛ")
                    if company_address_info.find("АдресРФ") is not None:
                        if company_address_info.find("АдресРФ").find("Регион") is not None:
                            region = company_address_info.find("АдресРФ").find("Регион").get("НаимРегион")
                            if controller.region.get() and controller.region.get() not in region:
                                continue

                        if company_address_info.find("АдресРФ").find("Город") is not None:
                            town = company_address_info.find("АдресРФ").find("Город").get("НаимГород")
                            if controller.town.get() and controller.town.get() not in town:
                                continue

                        if company_address_info.find("АдресРФ").find("Улица") is not None:
                            street = company_address_info.find("АдресРФ").find("Улица").get("НаимУлица")

                        building = company_address_info.find("АдресРФ").attrib.get("Дом", None)
                        apartments = company_address_info.find("АдресРФ").attrib.get("Кварт", None)

                    elif company_address_info.find("СвАдрЮЛФИАС") is not None:
                        if company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион") is not None:
                            region = company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион").text
                            if controller.region.get() and controller.region.get() not in region:
                                continue

                        if company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт") is not None:
                            town = company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт").get("Наим")
                            if controller.town.get() and controller.town.get() not in town:
                                continue

                        if company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети") is not None:
                            street = company_address_info.find("СвАдрЮЛФИАС").find("ЭлУлДорСети").get("Наим")

                        if company_address_info.find("СвАдрЮЛФИАС").find("Здание") is not None:
                            building = company_address_info.find("СвАдрЮЛФИАС").find("Здание").get("Номер")

                        if company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания") is not None:
                            apartments = company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания").get("Номер")

                    else:
                        print(self.archive_list[archive_index].filename)
                        print(xml_name)
                        print(small_name)
                        exit(code="! FUCKING ADDRESS !")

                if company.find("СвОКВЭД") is not None:
                    company_okved_info = company.find("СвОКВЭД")
                    if company_okved_info.find("СвОКВЭДОсн") is not None:
                        main_okved = f'{company_okved_info.find("СвОКВЭДОсн").get("КодОКВЭД")} {company_okved_info.find("СвОКВЭДОсн").get("НаимОКВЭД")}'
                        if controller.main_okved.get() and controller.main_okved.get() not in main_okved:
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

                        additional_okved = "; ".join(additional_okved)

                status = True
                if company.find("СвПрекрЮЛ") is not None:
                    status = False
                if controller.status.get() and controller.status.get() != status:
                    continue

                director_surname = None
                director_name = None
                director_secondname = None

                if company.find("СведДолжнФЛ") is not None:
                    company_people_info = company.find("СведДолжнФЛ")

                    if company_people_info.find("СвФЛ").attrib.get("Фамилия"):
                        director_surname = company_people_info.find("СвФЛ").get("Фамилия")

                    if company_people_info.find("СвФЛ").attrib.get("Имя"):
                        director_name = company_people_info.find("СвФЛ").get("Имя")

                    if company_people_info.find("СвФЛ").attrib.get("Отчество"):
                        director_secondname = company_people_info.find("СвФЛ").get("Отчество")

                    director = f"{director_surname} {director_name} {director_secondname}"

                inn = company.get("ИНН")
                kpp = company.get("КПП")

                match status:
                    case False:
                        status = "Нет"
                    case True:
                        status = "Да"
                    case _:
                        status = "Не опр"

                new_company = model.Company.Company(small_name=small_name,
                                                    inn=inn,
                                                    kpp=kpp,
                                                    date_reg=date_reg,
                                                    region=region,
                                                    town=town,
                                                    street=street,
                                                    building=building,
                                                    apartments=apartments,
                                                    director=director,
                                                    main_okved=main_okved,
                                                    additional_okved=additional_okved,
                                                    status=status)

                yield new_company

            if temp == 3:
                break
