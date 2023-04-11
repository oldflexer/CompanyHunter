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
        # print(self.archive_list[archive_index].filename)
        return self.archive_list[archive_index].namelist()

    def get_companies(self, archive_index, controller):
        xml_list = self.find_xml_list(archive_index)

        for xml_name in xml_list:
            # print(xml_name)
            xml_bytes = self.archive_list[archive_index].read(xml_name)
            xml_data = str(xml_bytes, encoding="windows-1251")

            egrul_root = ElementTree.fromstring(xml_data)
            companies = egrul_root.findall("СвЮЛ")

            for company in companies:
                company_tags = [item.tag for item in company.iter()]

                if "СвНаимЮЛ" in company_tags:
                    company_name_info = company.find("СвНаимЮЛ")
                    full_name = company_name_info.get("НаимЮЛПолн")
                    if controller.full_name.get() and controller.full_name.get() not in full_name:
                        continue
                else:
                    full_name = None

                if "СвРегОрг" in company_tags:
                    company_reg_info = company.find("СвРегОрг")
                    date_reg = company_reg_info.find("ГРНДата").get("ДатаЗаписи")
                    if controller.date_reg.get() and controller.full_name.get() != date_reg:
                        continue
                else:
                    date_reg = None

                if "СвАдресЮЛ" in company_tags:
                    company_address_info = company.find("СвАдресЮЛ")
                    address_tags = [item.tag for item in company_address_info.iter()]

                    if "АдресРФ" in address_tags:
                        region = company_address_info.find("АдресРФ").find("Регион").get("НаимРегион")
                        if controller.region.get() and controller.region.get() not in region:
                            continue

                        town = company_address_info.find("Город").get("НаимГород")
                        if controller.town.get() and controller.town.get() not in town:
                            continue

                        building = company_address_info.find("АдресРФ").get("Дом")
                        apartments = company_address_info.find("АдресРФ").get("Кварт")

                    elif "СвАдрЮЛФИАС" in address_tags:
                        region = company_address_info.find("СвАдрЮЛФИАС").find("НаимРегион").text
                        if controller.region.get() and controller.region.get() not in region:
                            continue

                        town = company_address_info.find("СвАдрЮЛФИАС").find("НаселенПункт").get("Наим")
                        if controller.town.get() and controller.town.get() not in town:
                            continue

                        building = company_address_info.find("СвАдрЮЛФИАС").find("Здание").get("Номер")
                        apartments = company_address_info.find("СвАдрЮЛФИАС").find("ПомещЗдания").get("Номер")

                    else:
                        region = None
                        town = None
                        building = None
                        apartments = None
                        print(self.archive_list[archive_index].filename)
                        print(xml_name)
                        print(full_name)
                        exit(code="666")

                if "СвОКВЭД" in company_tags:
                    company_okved_info = company.find("СвОКВЭД")
                    main_okved = company_okved_info.find("СвОКВЭДОсн").get(
                        "КодОКВЭД") + company_okved_info.find("СвОКВЭДОсн").get(
                        "НаимОКВЭД")
                    if controller.main_okved.get() and controller.main_okved.get() not in main_okved:
                        continue

                    additional_okved = [add_okved.get("КодОКВЭД") for add_okved in
                                        company_okved_info.findall("СвОКВЭДДоп")]
                    if controller.additional_okved.get():
                        flag = False
                        for okved in additional_okved:
                            if controller.additional_okved.get() in okved:
                                flag = True
                        if not flag:
                            continue

                status = True
                if company.find("СвПрекрЮЛ"):
                    status = False
                if controller.status.get() and controller.status.get() != status:
                    continue

                company_people_info = company.find("СведДолжнФЛ")

                inn = company.get("ИНН")
                kpp = company.get("КПП")

                try:
                    street = company_address_info.find("Улица").get("НаимУлица")
                except AttributeError:
                    street = None

                director_surname = company_people_info.find("СвФЛ").get("Фамилия") or ""
                director_name = company_people_info.find("СвФЛ").get("Имя") or ""
                director_secondname = company_people_info.find("СвФЛ").get("Отчество") or ""

                director = director_surname + director_name + director_secondname

                new_company = model.Company.Company(full_name=full_name,
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
