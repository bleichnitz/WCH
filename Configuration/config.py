from datetime import datetime
from pathlib import Path
import yaml as yaml
import pandas as pd
from tabulate import tabulate
from colorama import Fore



def find_config_file(config_folder):
    valid_config = False
    class_folder = Path(config_folder)
    format_row = "{:"

    for item in class_folder.iterdir():
        if item.suffix == ".yaml" or item.suffix == ".yml":
            valid_config = True
            config_file = item

    if valid_config is True:
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
        keys = config_data.keys()

        directory_verfication = []
        valid_format = False

        for key in keys:
            counter = 0
            sub_keys = list(config_data[key].keys())
            if key == "FILES":
                for item in config_data[key]:
                    item_verification = []
                    sub_key = sub_keys[counter]
                    file_path = Path(config_data[key][sub_key])
                    if file_path.suffix == ".xlsx":
                        valid_format = True
                    else:
                        valid_format = False
                    item_verification.append(sub_key)
                    item_verification.append(valid_format)
                    item_verification.append(file_path)
                    directory_verfication.append(item_verification)

                    counter += 1

                print(f"\n{key}")
                print(Fore.WHITE + tabulate(directory_verfication))
                verified_formats = input(Fore.RESET + "Are all required files listed and valid format (*.xlsx)? <y/n>\t")
                if verified_formats.lower() == "y":
                    pass
                else:
                    return 0

    print(Fore.LIGHTYELLOW_EX + "----- Config data validated -----\n")
    return config_data


def today_date():
    now = datetime.now()
    c_date = now.strftime("%Y-%m-%d")
    return c_date


def current_time():
    now = datetime.now()
    c_time = now.strftime("%H-%M-%S")
    return c_time


def school_year():
    now = datetime.now()
    c_year = now.year
    c_month = now.month
    if c_month <= 6:
        current_school_year = f"{c_year-1}-{c_year}"
    else:
        current_school_year = f"{c_year}-{c_year+1}"
        # print(c_month)

    return current_school_year