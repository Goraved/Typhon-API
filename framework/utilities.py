import datetime
import json
import random
import string

import gevent
import pytz

from base_definitions import ROOT_DIR
from configuration.config_parse import os, MAIN_API_URL, OS_NAME, GITHUB, TEST_DATA_DIR


class Utilities:

    @staticmethod
    def generate_random_key(length: int = 16) -> str:
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(length)])

    @staticmethod
    def generate_random_str_num(length: int = 16) -> str:
        return ''.join([random.choice(string.digits) for _ in range(length)])

    @staticmethod
    def convert_dict_to_json(dictionary: dict) -> str:
        return json.dumps(dictionary)

    @staticmethod
    def get_current_datetime():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def delta_time(start_time, end_time):
        return datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ") - \
               datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_days(plus_days: int) -> str:
        date = datetime.datetime.now() + datetime.timedelta(days=plus_days)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_seconds(plus_seconds: int) -> str:
        date = datetime.datetime.utcnow() + datetime.timedelta(seconds=plus_seconds)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_minus_specific_seconds(minus_seconds: int) -> str:
        date = datetime.datetime.utcnow() - datetime.timedelta(seconds=minus_seconds)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_minutes(plus_minutes: int) -> str:
        date = datetime.datetime.utcnow() - datetime.timedelta(minutes=plus_minutes)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def current_kyiv_time() -> datetime:
        # Kyiv
        timezone = pytz.timezone('Europe/Kiev')
        return datetime.datetime.now(timezone)

    @staticmethod
    def kyiv_get_current_datetime_plus_specific_minutes(plus_minutes: int, date_format: str = "%Y-%m-%dT%H:%M:%S"):
        date = Utilities.current_kyiv_time() + datetime.timedelta(minutes=plus_minutes)
        return date.strftime(date_format)

    @staticmethod
    def kyiv_get_current_datetime_minus_specific_minutes(minus_minutes: int, date_format: str = "%Y-%m-%dT%H:%M:%S"):
        date = Utilities.current_kyiv_time() - datetime.timedelta(minutes=minus_minutes)
        return date.strftime(date_format)

    @staticmethod
    def fix_api_properties():
        if os.path.isdir(f"{ROOT_DIR}/allure-results"):
            if os.path.exists(f"{ROOT_DIR}/allure-results/environment.properties"):
                remove_cycles = 10
                wait_interval = 1
                for _ in range(remove_cycles):
                    try:
                        os.remove(f"{ROOT_DIR}/allure-results/environment.properties")
                        break
                    except FileNotFoundError:
                        gevent.sleep(wait_interval)  # will be useful in parallel mode
        else:
            os.mkdir(f"{ROOT_DIR}/allure-results")
        file = open(f"{ROOT_DIR}/allure-results/environment.properties", "w+")
        file.write(f"Environment {os.getenv('ENVIRONMENT', 'dev').upper()}\n")
        file.write(f"URL {MAIN_API_URL}\n")
        file.write(f"Git {GITHUB}\n")
        file.write(f"OS_NAME {OS_NAME}\n")

    @staticmethod
    def create_executor_file():
        if os.path.isdir(f"{ROOT_DIR}/allure-results"):
            if os.path.exists(f"{ROOT_DIR}/allure-results/executor.json"):
                remove_cycles = 10
                wait_interval = 1
                for _ in range(remove_cycles):
                    try:
                        os.remove(f"{ROOT_DIR}/allure-results/executor.json")
                        break
                    except FileNotFoundError:
                        gevent.sleep(wait_interval)  # will be useful in parallel mode
        file_exec = '''{
  "name" : "Jenkins",
  "type" : "Jenkins",
  "url" : "http://example.org",
  "buildOrder" : "%s",
  "buildName" : "Build %s",
  "buildUrl" : "%s",
  "reportName" : "Demo allure report",
  "reportUrl" : "%s/allure"
}''' % (os.getenv('BUILD_NUMBER'), os.getenv('BUILD_NUMBER'), os.getenv('BUILD_URL'), os.getenv('BUILD_URL'))
        file = open(f"{ROOT_DIR}/allure-results/executor.json", "w+")
        file.write(file_exec)

    @staticmethod
    def log(msg: str, msg_type: str = 'DEBUG'):
        """
        Method will write log message to the allure report int 'stdout' tab
        """
        current_time = Utilities.get_current_datetime()
        print(f'{current_time} - {msg_type}: \n {msg}\n-------')

    @staticmethod
    def generate_txt_file(name: str, text: str = 'test') -> str:
        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')
        file = open(f"temp_files/{name}.txt", "w")
        file.write(text)
        file.close()
        return os.path.abspath(f"temp_files/{name}.txt")

    @staticmethod
    def remove_file(name: str):
        if os.path.exists(name):
            os.remove(name)

    @staticmethod
    def read_json_from_file(filename: str):
        full_file_path = f"{ROOT_DIR}/{TEST_DATA_DIR}/{filename}"
        with open(full_file_path, 'r') as file:
            file_content = json.load(file)
        return file_content

    @staticmethod
    def check_correct_order(input_list: str, order_type: str = 'desc') -> bool:
        reverse_sort = order_type.lower() == 'desc'
        sorted_list = list(input_list)
        sorted_list.sort(reverse=reverse_sort)
        return input_list == sorted_list

    @staticmethod
    def randomise_string_case(text: str):
        return ''.join(random.choice((str.upper, str.lower))(c) for c in text)
