import configparser
import platform

from base_definitions import os, ROOT_DIR

env_config = configparser.ConfigParser()
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
env_config.read_file(open(f'{os.path.dirname(os.path.abspath(__file__))}/{ENVIRONMENT}.ini'))

global_config = configparser.ConfigParser()
global_config.read_file(open(f'{os.path.dirname(os.path.abspath(__file__))}/global.ini'))

# Environment settings
TOKEN = env_config.get('CREDENTIALS', 'token')
MAIN_API_URL = env_config.get('PATH', 'main_API_url')
OS_NAME = platform.system()
OS_VERSION = platform.version()
OS_ARCHITECTURE = platform.architecture()
TEST_DATA_DIR = 'framework/api/test_data'
BROWSER = os.getenv('BROWSER', 'chrome')
PROJECT = global_config.get('ENVIRONMENT', 'project')
LINK_TYPE_TEST_CASE = global_config.get('ENVIRONMENT', 'link_type_test_case')
LINK_TYPE_LINK = global_config.get('ENVIRONMENT', 'link_type_link')
TEST_CASE = global_config.get('ENVIRONMENT', 'test_case')
BUG = global_config.get('ENVIRONMENT', 'bug')
GITHUB = global_config.get('ENVIRONMENT', 'git_path')
