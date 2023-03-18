# ----- IMPORT LIBRARIES & CODE ----------------------------------------------------------------------------------------
# The following imports are from the PyPi repository.
from colorama import Fore
from tabulate import tabulate


def consolidate_data(data):
    """
    The data from all the individual arrays was packaged within a single data array prior to being passed into this
    function (this occurs in the main.py file). The data is pulled out for easier reading of the program. Using the
    master timetable data as a foundation, a new array is created, and the data from the subsequent data is appended.
    The other data arrays are searched to find the data for each student in the master timetable data.
    :param data: an array of arrays that contains all data; needs to be separated out
    :return: a single multi-line array that has the "Who Can Help" data organized by student
    """

    # extract the individual lists from the packaged data object passed into the function
    print(Fore.BLUE + f"Begin consolidation of lists..." + Fore.WHITE)
    time_table = data["time_table"]
    sis_iep = data["sis_iep"]
    sis_ell = data["sis_ell"]
    monitor_iep = data["monitor_iep"]
    monitor_contact = data["monitor_contact"]
    monitor_ell = data["monitor_ell"]

    # initialize the array for consolidating the data
    consolidated_data = []

    # loop through each row of the time table data; each row in this data array represents an individual student
    for row in time_table:
        # initialize / reset the dictionary that will contain individual student data;
        student_data = {"student_number": None, "first_name": None, "last_name": None,
                        "period_1": None, "period_2": None, "period_3": None, "period_4": None, "period_5": None,
                        "iep": False, "iep_monitor": None, "contact_monitor": None,
                        "ell": False, "ell_monitor": None,
                        "gc": None, "vp": None}

        # add data from the time table array to the student dictionary
        student_data["student_number"] = row["student_number"]
        student_name = row["student_name"]
        student_name = student_name.split(",")
        student_data["first_name"] = student_name[1]
        student_data["last_name"] = student_name[0]
        student_data["period_1"] = row["p1"]
        student_data["period_2"] = row["p2"]
        student_data["period_3"] = row["p3"]
        student_data["period_4"] = row["p4"]
        student_data["period_5"] = row["p5"]

        # search IEP list to determine if the student has an IEP
        has_iep = find_iep(current_student=student_data["student_number"], iep_list=sis_iep)
        if has_iep is True:
            student_data["iep"] = True
        else:
            student_data["iep"] = ""

        # search the IEP monitor list to see if the student is being monitored for additional support based on their IEP
        iep_monitor_teacher = find_monitor(current_student=student_data["student_number"], monitor_list=monitor_iep)
        if iep_monitor_teacher != "":
            student_data["iep_monitor"] = iep_monitor_teacher
        else:
            student_data["iep_monitor"] = ""

        # search the contact list to see if the student has a monitor teacher
        contact_teacher = find_monitor(current_student=student_data["student_number"], monitor_list=monitor_contact)
        if contact_teacher != "":
            student_data["contact_monitor"] = contact_teacher
        else:
            student_data["contact_monitor"] = ""

        # search the ELL list to see if the student has an ESL/ELL designation
        ell_designation = find_ell(current_student=student_data["student_number"], ell_list=sis_ell)
        if ell_designation:
            student_data["ell"] = True
        else:
            student_data["ell"] = ""

        # search the ELL monitor list to see if the student has an ELL monitor
        ell_monitor = find_monitor(current_student=student_data["student_number"], monitor_list=monitor_ell)
        if ell_monitor != "":
            student_data["ell_monitor"] = ell_monitor
        else:
            student_data["ell_monitor"] = ""

        # TODO: can add in a function to cross-reference student last name to VP and GC alphas. Currently running into
        #  issues with letters with special characters (e.g. é as they do not have ascii values and using Unicode
        #  (utf-8) requires extensive cross-referencing across the character blocks.

        # append student dictionary to the consolidated data array
        consolidated_data.append(student_data)

    print(tabulate(consolidated_data))
    print(Fore.LIGHTYELLOW_EX + f"----- Data Consolidation Complete -----")
    return consolidated_data


def find_iep(current_student, iep_list):
    """
    Search IEP list. If the current student number is on the list, function will return TRUE. If not, returns FALSE.
    :param current_student: current student from the timetable list
    :param iep_list: the full list
    :return: TRUE/FALSE
    """
    for item in iep_list:
        if item == current_student:
            return True
    return False


def find_ell(current_student, ell_list):
    """
    Search ELL list. If the current student number is on the list, function will return TRUE. If not, returns FALSE.
    :param current_student: current student from the timetable list
    :param ell_list: the full list
    :return: TRUE/FALSE
    """
    for item in ell_list:
        if item == current_student:
            return True
    return False


def find_monitor(current_student, monitor_list):
    """
    Search a monitor list (IEP, spec ed, ell). If the current student number is on the list, function will return TRUE.
    If not, returns FALSE.
    :param current_student: current student from the timetable list
    :param iep_list: the full list
    :return: monitor teacher's name or blank ("")
    """
    blank = ""
    for row in monitor_list:
        if row["student_number"] == current_student:
            return row["monitor_teacher"]
    return blank

# TODO: insert here the function that will be written to locate the VP or guidance councillor for each student. This is
#  currently being explored in another document as I am running into issues with special characters. The comparison
#  between VP/GC alphas and the student last name has more variations than is possible through a strict char to ascii
#  conversion and then comparision.