import warnings as warnings
import openpyxl as openpyxl
from colorama import Fore, Back

def load_file(file_name):
    """
    Load data from an MS Excel file; NOTE: the load typical throws this error: "UserWarning: Data Validation
    extension is not supported and will be removed warn(msg)", as openpyxl does not support data validation at this
    time; this code simply ignores the warning and does not print it into the console to make for consistent and clear
    communication of what is happening in the program; the 'warnings' module removes the warning from printing
    :param file_name: this is the absolute path of the file to be opened for use with OPENPYXL
    :return: the opened OPENPYXL workbook object for use within different functions of the program
    """

    warnings.simplefilter(action='ignore', category=UserWarning)
    print(Fore.BLUE + "File <" + str(file_name) + "> has loaded successfully.")
    return openpyxl.load_workbook(file_name, data_only=True)