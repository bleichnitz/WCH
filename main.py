# ----- IMPORT LIBRARIES & CODE ----------------------------------------------------------------------------------------
# The following imports are from the PyPi repository.
from colorama import Fore

# The following imports are from other *.py files within this project.
from config import find_config_file
import parse_raw_data
from consolidate_data import consolidate_data
from create_WCH_doc import create_doc

# ----- CONFIG DATA ----------------------------------------------------------------------------------------------------
# Configuration data is saved to the 'Configuration' folder within the WCH program file. The following code sorts
# through the folder, looking for the YAML configuration file, opens the file and retrieves the data. If there is an
# error in the file types that the user identifies by responding anything other than "y" or "Y" to the prompt following
# the FILES table that is printed in the run terminal, the program will quit so the user can correct identified issues.
config_folder = "Configuration"
config_data = find_config_file(config_folder)
if config_data == 0:
    print(Fore.RED + "!!! ERROR - verify file paths and formats in config.yaml !!!")
    quit()

# ----- RETRIEVING DATA FROM SOURCE FILES ------------------------------------------------------------------------------
# The user is asked to identify the current semester for generating the Who Can Help document. This data is used for
# retrieving the correct class schedule from the SIS Time Table Report. After a valid entry as "1" or "2", each of the
# files identified in the 'config_data' are opened and data is parsed, sorted and filtered where needed.
valid_semester = False
semester = 1
while valid_semester is False:
    semester = int(input(Fore.RESET + f"Select semester: <1/2>\t"))
    if semester == 1 or semester == 2:
        valid_semester = True
    else:
        print(Fore.RED + f"!!! ERROR - please enter a valid semester !!!")
time_table = parse_raw_data.parse_sis_time_table(path=config_data["FILES"]["SIS_time_table"], semester=semester,
                                                 config=config_data)
sis_iep = parse_raw_data.parse_sis_iep(path=config_data["FILES"]["SIS_spec_ed"], config=config_data)
sis_ell = parse_raw_data.parse_sis_ell(path=config_data["FILES"]["SIS_ell"], config=config_data)
monitor_iep = parse_raw_data.parse_iep_monitor(path=config_data["FILES"]["MONITOR_spec_ed"], config=config_data)
monitor_contact = parse_raw_data.parse_contact_monitor(path=config_data["FILES"]["MONITOR_contact"], config=config_data)
monitor_ell = parse_raw_data.parse_ell_monitor(path=config_data["FILES"]["MONITOR_ell"], config=config_data)
data_lists = {"time_table": time_table,
              "sis_iep": sis_iep,
              "sis_ell": sis_ell,
              "monitor_iep": monitor_iep,
              "monitor_contact": monitor_contact,
              "monitor_ell": monitor_ell}
print(Fore.LIGHTYELLOW_EX + "----- Data Parsed, Sorted and Filtered -----\n")

# ----- CONSOLIDATING_DATA ---------------------------------------------------------------------------------------------
# Data needs to be consolidated into one data array. Each list is contained within the "data_lists" dictionary to pass
# into the consolidation function used below.

valid_periods = False
num_periods = 4
while valid_periods is False:
    num_periods = int(input(Fore.RESET + f"Select number of periods in the school day: <4/5/6>\t"))
    if num_periods >= 4 and num_periods <= 6:
        valid_periods = True
    else:
        print(Fore.RED + f"!!! ERROR - please enter a valid number of periods per day !!!")

consolidated_data = consolidate_data(data=data_lists    )

# ----- CREATING WHO CAN HELP DOC --------------------------------------------------------------------------------------
# After data consolidation, the 'Who Can Help' document can be created.

create_doc(data=consolidated_data)
