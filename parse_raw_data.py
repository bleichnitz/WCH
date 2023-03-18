# ----- IMPORT LIBRARIES & CODE ----------------------------------------------------------------------------------------
# The following imports are from the PyPi repository.
from colorama import Fore

# The following imports are from other *.py files within this project.
from load_files import load_file
from excel_columns import find_col_array_index


def parse_sis_time_table(path, semester, config):
    """
    Opens the *.xlsx file for the timetable exported from SIS (export as *.xml).
    Iterates through each row to identify each student, student number and courses being taken in the current school
    year. Based on user input, will only return semester one or semester two courses.

    :param path: the absolute path for where the file is located on the computer
    :param semester: user input for semester 1 or semester 2 to choose courses
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student number, name and courses for chosen semester; each row contains an
    individual's data
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["TIME_TABLE"]["student_number"])
    col_student_name = find_col_array_index(config["TIME_TABLE"]["student_name"])

    col_p1 = ""
    col_p2 = ""
    col_p3 = ""
    col_p4 = ""
    col_p5 = ""
    col_p6 = ""

    if semester == 1:
        col_p1 = find_col_array_index(config["TIME_TABLE"]["s1p1"])
        col_p2 = find_col_array_index(config["TIME_TABLE"]["s1p2"])
        col_p3 = find_col_array_index(config["TIME_TABLE"]["s1p3"])
        col_p4 = find_col_array_index(config["TIME_TABLE"]["s1p4"])
        col_p5 = find_col_array_index(config["TIME_TABLE"]["s1p5"])
        col_p6 = find_col_array_index(config["TIME_TABLE"]["s1p6"])
    elif semester == 2:
        col_p1 = find_col_array_index(config["TIME_TABLE"]["s2p1"])
        col_p2 = find_col_array_index(config["TIME_TABLE"]["s2p2"])
        col_p3 = find_col_array_index(config["TIME_TABLE"]["s2p3"])
        col_p4 = find_col_array_index(config["TIME_TABLE"]["s2p4"])
        col_p5 = find_col_array_index(config["TIME_TABLE"]["s2p5"])
        col_p6 = find_col_array_index(config["TIME_TABLE"]["s2p6"])

    cleaned_data = []
    for row in data_sheet.values:
        student_data = {"student_number": "", "student_name": "",
                        "p1": "", "p2": "", "p3": "", "p4": "", "p5": "", "p6": ""}
        student_data["student_number"] = row[col_student_number]
        student_data["student_name"] = row[col_student_name]
        student_data["p1"] = row[col_p1]
        student_data["p2"] = row[col_p2]
        student_data["p3"] = row[col_p3]
        student_data["p4"] = row[col_p4]
        student_data["p5"] = row[col_p5]
        student_data["p6"] = row[col_p6]
        cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- Time Table Parsed: {len(cleaned_data)} students")

    return cleaned_data


def parse_sis_iep(path, config):
    """
    Opens the *.xlsx file for the iep report exported from SIS (export as *.xml).
    Iterates through each row to identify each student, student number IEP status. Due to the structure of the document
    it is necessary to extract data from each row, sort the created array, and then filter the data to ensure that each
    student is only listed once.

    :param path: the absolute path for where the file is located on the computer
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student numbers to indicate if the student has an IEP
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["IEP_REPORT"]["student_number"])

    cleaned_data = []
    for row in data_sheet.values:
        student_data = row[col_student_number]
        cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- IEP List Parsed: {len(cleaned_data)} students")

    cleaned_data.sort()
    print(Fore.WHITE + f"\t ----- IEP List Sorted: {len(cleaned_data)} students")

    filtered_data = []
    previous_student = 0
    for row in cleaned_data:
        current_student = row
        if current_student != previous_student:
            filtered_data.append(current_student)
        previous_student = current_student
    print(Fore.WHITE + f"\t ----- IEP List Filtered: {len(filtered_data)} students")
    return cleaned_data


def parse_sis_ell(path, config):
    """
    Opens the *.xlsx file for the ELL list exported from SIS (export as *.xml).
    Iterates through each row to identify each student number on the list. Due to the structure of the document
    it is necessary to extract data from each row, sort the created array, and then filter the data to ensure that each
    student is only listed once.

    :param path: the absolute path for where the file is located on the computer
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student numbers to indicate if the student has is designated as an English Language
    Learner
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["ELL_REPORT"]["student_number"])

    cleaned_data = []
    for row in data_sheet.values:
        student_data = row[col_student_number]
        # print(Fore.WHITE + f"\t{student_data}")
        cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- ELL List Parsed: {len(cleaned_data)} students")

    cleaned_data.sort()
    print(Fore.WHITE + f"\t ----- ELL List Sorted: {len(cleaned_data)} students")

    filtered_data = []
    previous_student = 0
    for row in cleaned_data:
        current_student = row
        if current_student != previous_student:
            filtered_data.append(current_student)
        previous_student = current_student
    print(Fore.WHITE + f"\t ----- ELL List Filtered: {len(filtered_data)} students")
    return cleaned_data


def parse_iep_monitor(path, config):
    """
    Opens the *.xlsx file for the IEP monitor list. This document should be created by the special education lead
    teacher as indicated in the config.yaml file.
    Iterates through each row to identify each student number on the list and the connected monitor teacher. As this
    document is a working document used by the special education staff, each student is listed only once and there is
    no need to sort and filter.

    :param path: the absolute path for where the file is located on the computer
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student numbers to indicate if the student has is designated as having an IEP
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["IEP_MONITOR"]["student_number"])
    col_monitor = find_col_array_index(config["IEP_MONITOR"]["monitor"])

    cleaned_data = []

    for row in data_sheet.values:
        student_data = {"student_number": "", "monitor_teacher": ""}
        student_data["student_number"] = row[col_student_number]
        student_data["monitor_teacher"] = row[col_monitor]
        # print(Fore.WHITE + f"\t{student_data}")
        cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- IEP Monitor List Parsed: {len(cleaned_data)} students")
    return cleaned_data


def parse_contact_monitor(path, config):
    """
    Opens the *.xlsx file for the contact monitor list. This document should be created by the special education lead
    teacher OR the contact teacher as indicated in the config.yaml file.
    Iterates through each row to identify each student number on the list and the connected monitor teacher. As this
    document is a working document used by the special education staff, each student is listed only once and there is
    no need to sort and filter.

    :param path: the absolute path for where the file is located on the computer
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student numbers to indicate if the student has is designated as an connected with
    contact
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["CONTACT_MONITOR"]["student_number"])
    col_monitor = find_col_array_index(config["CONTACT_MONITOR"]["monitor"])

    cleaned_data = []

    for row in data_sheet.values:
        student_data = {"student_number": "", "monitor_teacher": ""}
        student_data["student_number"] = row[col_student_number]
        student_data["monitor_teacher"] = row[col_monitor]
        # print(Fore.WHITE + f"\t{student_data}")
        cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- CONTACT Monitor List Parsed: {len(cleaned_data)} students")
    return cleaned_data


def parse_ell_monitor(path, config):
    """
    Opens the *.xlsx file for the ELL monitor list. This document should be created by the ESL/ELL lead
    teacher as indicated in the config.yaml file.
    Iterates through each row to identify each student number on the list and the connected monitor teacher. As this
    document is a working document used by the ESL/ELL staff, each student is listed only once and there is
    no need to sort and filter.

    :param path: the absolute path for where the file is located on the computer
    :param config: configuration data; will utilize the column references listed to determine where data is located
    within the spreadsheet
    :return: an array of data with student numbers to indicate if the student has is designated as an English Language
    Learner
    """

    workbook = load_file(file_name=path)
    sheets = workbook.sheetnames
    data_sheet = workbook[sheets[0]]

    col_student_number = find_col_array_index(config["ELL_MONITOR"]["student_number"])
    col_monitor = find_col_array_index(config["ELL_MONITOR"]["monitor"])

    cleaned_data = []

    for row in data_sheet.values:
        student_data = {"student_number": "", "monitor_teacher": ""}
        student_data["student_number"] = row[col_student_number]
        if student_data["student_number"] == "" or student_data["student_number"] is None:
            pass
        else:
            student_data["monitor_teacher"] = row[col_monitor]
            # print(Fore.WHITE + f"\t{student_data}")
            cleaned_data.append(student_data)
    cleaned_data.pop(0)  # remove header data from parsed array
    print(Fore.WHITE + f"\t ----- ELL Monitor List Parsed: {len(cleaned_data)} students")
    return cleaned_data
