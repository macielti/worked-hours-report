import json
import os
from datetime import datetime
import dateutil.parser
from Config import Config
import re

FILE_PATH="data.json"

def dt_parser(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = dateutil.parser.parse(value)
        except:
            pass
    return json_dict

class Data:
    @staticmethod
    def creates_data_file():
        if not os.path.exists("data.json"):
            initial_content = []
            with open(FILE_PATH, "w") as data_file_obj:
                json.dump(initial_content, data_file_obj)

    @staticmethod
    def get_all_reports():
        with open(FILE_PATH, "r") as data_file_obj:
            all_reports = json.load(data_file_obj, object_hook=date_hook)
        return all_reports
    
    @staticmethod
    def get_format_type_based_on_day(today=datetime.now()):
        weekday = today.weekday()
        if weekday < 5:
            return "format-week"
        else:
            return "format-weekend"


    @staticmethod
    def get_today_report_object():
        Data.creates_data_file()

        all_reports = Data.get_all_reports()

        for report in all_reports:
            start=report["start"]
            if start.date() == datetime.today().date():
                return report
            
        default_empty_report = {}
        format_type = Data.get_format_type_based_on_day()
        default_empty_report["format"] = format_type
        return default_empty_report

    @staticmethod
    def save_report(report_to_push):
        # loads all reports 
        all_reports = Data.get_all_reports()

        # get the index of the today's report
        for i, report in enumerate(all_reports):
            start=report["start"]
            if start.date() == datetime.today().date():
                all_reports[i] = report_to_push
                with open(FILE_PATH, "w") as data_file_obj:
                    json.dump(all_reports, data_file_obj, default=dt_parser)
                return True
               
        all_reports.append(report_to_push)
        with open(FILE_PATH, "w") as data_file_obj:
            json.dump(all_reports, data_file_obj, default=dt_parser)
        return True

    @staticmethod
    def get_parsed_report(report):
        config = Config.load_get_config_object()

        config_format = report["format"]
        format_parse = config[config_format]

        # parse start
        start = report['start']
        start_human = start.strftime("%H:%M")
        format_parse = re.sub(r'<start>', start_human, format_parse)

        # parse end
        try:
            start = report['end']
            start_human = start.strftime("%H:%M")
            format_parse = re.sub(r'<end>', start_human, format_parse)
        except:
            format_parse = re.sub(r'<end>', '', format_parse)

        return format_parse

        




