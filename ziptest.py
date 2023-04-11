import datetime
import time
from datetime import timedelta
import os
import xml.etree.ElementTree
import xml.etree.ElementTree as ElementTree
from zipfile import ZipFile


# count tags amount
def count_tag(element: xml.etree.ElementTree.Element, tag: str):
    if not element.tag:
        return 0

    if not tag:
        return 0

    return len(element.findall(tag))


# show pretty look xml
def show_xml(element: xml.etree.ElementTree.Element, depth: int = 0):
    if not element.tag:
        return

    tag = ""
    attrib = ""
    text = ""
    tail = ""

    if element.tag:
        tag = element.tag

    if element.attrib:
        attrib = element.attrib

    if element.text:
        text = element.text.rstrip()

    if element.tail:
        tail = element.tail.rstrip()

    print(depth * "\t", f"{tag} {attrib} {text} {tail}", end="\n")

    if len(element):
        depth += 1
        for child in element:
            show_xml(element=child, depth=depth)


def find_element_with_attrib(element: xml.etree.ElementTree.Element, attrib_name: str):
    return element.get(attrib_name)


# count files in directory
def count_files(directory_path: str):
    try:
        result = len(os.listdir(directory_path))
    except Exception as e:
        print(e)
        return 0

    return result


# count size of files in directory
def count_files_size(directory_path: str):
    result = 0
    try:
        for file in os.scandir(directory_path):
            result += os.path.getsize(file)
    except Exception as e:
        print(e)
        return 0

    return result


def func(archives_size=0, archives_amount=0, companies_amount=0, data_path="E:\\data\\",
         start_time=time.time()):
    directory = os.listdir(data_path)
    archives_total = count_files(data_path)
    data_size = count_files_size(data_path)

    for filename in directory:
        if not filename.endswith(".zip"):
            return

        zip_archive = ZipFile(os.path.join(data_path, filename), "r")
        archives_size += os.path.getsize(os.path.join(data_path, filename))
        archives_amount += 1

        xml_stack = zip_archive.namelist()
        for xml_name in xml_stack:
            xml_bytes = zip_archive.read(xml_name)
            xml_data = str(xml_bytes, encoding="windows-1251")

            egrul_root = ElementTree.fromstring(xml_data)
            companies = egrul_root.findall("СвЮЛ")
            companies_amount += len(companies)

            for company in companies:
                try:
                    company_name_info = company.find("СвНаимЮЛ")
                    company_name_str = company_name_info.get("НаимЮЛПолн")

                    if "НТЦ ГЭ" in company_name_str:
                        company_inn_str = company.get("ИНН")

                        okved = company.find("СвОКВЭД")
                        okved_main = okved.find("СвОКВЭДОсн")
                        okved_main_str = okved_main.get("КодОКВЭД")
                        okved_secondary_info = okved.findall("СвОКВЭДДоп")

                        print(f"\n{company_name_str}")
                        print(f"{company_inn_str}")
                        print(f"{okved_main_str}")
                        for okved_secondary in okved_secondary_info:
                            okved_secondary_str = okved_secondary.get("КодОКВЭД")
                            print(f"{okved_secondary_str}")
                        print("\n")

                except Exception as e:
                    print(e)
                    continue

        current_time = time.time()
        temp_time = current_time - start_time
        archive_data_ratio = archives_size / data_size
        predicted_companies = int(companies_amount / archive_data_ratio)
        estimated_time = int(predicted_companies / (companies_amount / temp_time))

        print(f"\n{datetime.datetime.now()}")
        print(f"Total archives inspected: {archives_amount}/{archives_total} ({(archive_data_ratio * 100):.4}%)")
        print(f"Last one: {zip_archive.filename}")
        print(f"Total companies detected: {companies_amount}")
        print(f"Predicted companies amount: {predicted_companies}")
        print(f"Estimated waiting time: {timedelta(seconds=estimated_time)}\n")


func()
