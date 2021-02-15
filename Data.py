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
            try:
                start=report["start"]
            except:
                break
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
            try: 
                start=report["start"]
            except:
                continue
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
    def calculate_worked_hours_today(today=datetime.now()):
        report = Data.get_today_report_object()

        start = report['start']
        end = report['end']
        delta = end - start

        weekday = today.weekday()
        if weekday < 5:
            delta_lunch = report["lunch-end"] - report["lunch-start"]
            delta = delta - delta_lunch
            human_readable = str(delta)
            return re.sub(r'\..*', '', human_readable)
        else:
            human_readable = str(delta)
            return re.sub(r'\..*', '', human_readable)

    @staticmethod
    def get_parsed_report(report):
        config = Config.load_get_config_object()

        config_format = report["format"]
        format_parse = config[config_format]

        # parse start
        start = report['start']
        start_human = start.strftime("%H:%M")
        format_parse = re.sub(r'<start>', start_human, format_parse)

        # parse lunch start
        try:
            lunch_start = report['lunch-start']
            lunch_start_human = lunch_start.strftime("%H:%M")
            format_parse = re.sub(r'<lunch-start>', lunch_start_human, format_parse)
        except:
            format_parse = re.sub(r'<lunch-start>', '', format_parse)

        # parse lunch end
        try:
            lunch_end = report['lunch-end']
            lunch_end_human = lunch_end.strftime("%H:%M")
            format_parse = re.sub(r'<lunch-end>', lunch_end_human, format_parse)
        except:
            format_parse = re.sub(r'<lunch-end>', '', format_parse)

        # parse end
        try:
            end = report['end']
            end_human = end.strftime("%H:%M")
            format_parse = re.sub(r'<end>', end_human, format_parse)
        except:
            format_parse = re.sub(r'<end>', '', format_parse)
        
        # worked hours
        try:
            if report['end']:
                worked_hours_today = Data.calculate_worked_hours_today()
                format_parse = re.sub(r'<worked-hours-today>', worked_hours_today, format_parse)
        except:
            pass

        return format_parse
