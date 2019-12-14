import datetime
import json
import random
import string

import gevent
import pytz as pytz

from configuration.config_parse import ROOT_DIR, os, ENVIRONMENT, MAIN_API_URL, OS_NAME, GITHUB, TEST_DATA_DIR


class Utilities:

    @staticmethod
    def generate_random_key(length=16):
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(length)])

    @staticmethod
    def generate_random_str_num(length=16):
        return ''.join([random.choice(string.digits) for _ in range(length)])

    @staticmethod
    def convert_dict_to_json(dictionary):
        return json.dumps(dictionary)

    @staticmethod
    def get_current_datetime():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def delta_time(start_time, end_time):
        return datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ") - \
               datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_days(plus_days):
        date = datetime.datetime.now() + datetime.timedelta(days=plus_days)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_seconds(plus_seconds):
        date = datetime.datetime.utcnow() + datetime.timedelta(seconds=plus_seconds)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_minus_specific_seconds(minus_seconds):
        date = datetime.datetime.utcnow() - datetime.timedelta(seconds=minus_seconds)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_minutes(plus_minutes):
        date = datetime.datetime.utcnow() - datetime.timedelta(minutes=plus_minutes)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def current_kyiv_time():
        tz = pytz.timezone('Europe/Kiev')  # Kyiv
        return datetime.datetime.now(tz)

    @staticmethod
    def ics_get_current_datetime_plus_specific_minutes(plus_minutes, date_format="%Y-%m-%dT%H:%M:%S"):
        date = Utilities.current_kyiv_time() + datetime.timedelta(minutes=plus_minutes)
        return date.strftime(date_format)

    @staticmethod
    def ics_get_current_datetime_minus_specific_minutes(minus_minutes, date_format="%Y-%m-%dT%H:%M:%S"):
        date = Utilities.current_kyiv_time() - datetime.timedelta(minutes=minus_minutes)
        return date.strftime(date_format)

    @staticmethod
    def fix_api_properties():  # TODO add possibility to get env variables
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
        f = open(f"{ROOT_DIR}/allure-results/environment.properties", "w+")
        f.write(f"Environment {ENVIRONMENT.upper()}\n")
        f.write(f"URL {MAIN_API_URL}\n")
        f.write(f"Git {GITHUB}\n")
        f.write(f"OS_NAME {OS_NAME}\n")

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
        f = open(f"{ROOT_DIR}/allure-results/executor.json", "w+")
        f.write(file_exec)

    @staticmethod
    def log(msg, msg_type='DEBUG'):
        """
        Method will write log message to the allure report int 'stdout' tab
        """
        current_time = Utilities.get_current_datetime()
        print(f'{current_time} - {msg_type}: \n {msg}\n-------')

    @staticmethod
    def generate_txt_file(name, text='test'):
        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')
        file = open(f"temp_files/{name}.txt", "w")
        file.write(text)
        file.close()
        return os.path.abspath(f"temp_files/{name}.txt")

    @staticmethod
    def remove_file(name):
        if os.path.exists(name):
            os.remove(name)

    @staticmethod
    def read_json_from_file(filename):
        full_file_path = f"{ROOT_DIR}/{TEST_DATA_DIR}/{filename}"
        with open(full_file_path, 'r') as f:
            file_content = json.load(f)
        return file_content

    @staticmethod
    def check_correct_order(input_list, order_type='desc'):
        reverse_sort = True if order_type.lower() == 'desc' else False
        sorted_list = list(input_list)
        sorted_list.sort(reverse=reverse_sort)
        return input_list == sorted_list

    @staticmethod
    def randomise_string_case(text):
        return ''.join(random.choice((str.upper, str.lower))(c) for c in text)
