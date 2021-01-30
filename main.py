import argparse
from utils import creates_data_file_if_necessary, add_report_operation, creates_config_file_if_necessary, get_human_readable_report
import pyperclip

def main(args):
    action = args.action
    creates_data_file_if_necessary()
    creates_config_file_if_necessary()
    today_report = add_report_operation(action)
    human = get_human_readable_report(today_report)
    pyperclip.copy(human)
    print(human)



parser = argparse.ArgumentParser(description='A simple CLI to automaticaly generates daily report of worked hours and lunch intervals.')
parser.add_argument('--action', choices=['start', 'lunch-start', 'lunch-end', 'personal-start, personal-end', 'end'], type=str.lower, required=True)

args = parser.parse_args()

if __name__ == "__main__":
    main(args)