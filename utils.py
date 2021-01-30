from Data import Data
from datetime import datetime
from Config import Config

def creates_data_file_if_necessary():
    Data.creates_data_file()

def creates_config_file_if_necessary():
    Config.creates_config_file()

def add_report_operation(operation):
    todays_report = Data.get_today_report_object()
    if operation == "start":
        todays_report["start"] = datetime.now()

    elif operation == "lunch-start":
        todays_report["lunch-start"] = datetime.now()

    elif operation == "lunch-end":
        todays_report["lunch-end"] = datetime.now()

    elif operation == "end":
        todays_report["end"] = datetime.now()
    
    Data.save_report(todays_report)

    return todays_report

def get_human_readable_report(report):
    return Data.get_parsed_report(report)
