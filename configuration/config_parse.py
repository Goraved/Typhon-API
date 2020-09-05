import os
import platform

import yaml

# All configs placed into config/configs.yaml file. Please declare only variables here and set all values in yaml file

CONFIGS = yaml.safe_load(open(f'{os.path.dirname(os.path.abspath(__file__))}/configs.yaml'))
ENV_CONFIGS = CONFIGS['environments'][os.getenv('ENVIRONMENT', 'dev')]
URLS = CONFIGS['urls']
GENERAL = CONFIGS['general']
CONTROLLERS = CONFIGS['controllers']


def get_value(key, key_type, *args):
    """
    Get constant value from YAML file by default, or from environment variables if exists
    """
    value = os.getenv(key.upper(), key_type[key])
    if args and not os.getenv(key.upper()):
        value = value.format(*args)
    return value


# Environment settings
TOKEN = get_value('token', CONFIGS)
MAIN_API_URL = get_value('main_api_url', URLS)

PROJECT = get_value('project', GENERAL)
LINK_TYPE_TEST_CASE = get_value('link_type_test_case', GENERAL)
LINK_TYPE_LINK = get_value('link_type_link', GENERAL)
TEST_CASE = get_value('test_case', GENERAL)
BUG = get_value('bug', GENERAL)
GITHUB = get_value('git_path', GENERAL)

OS_NAME = platform.system()
OS_VERSION = platform.version()
OS_ARCHITECTURE = platform.architecture()
TEST_DATA_DIR = 'framework/api/test_data'

USERS_PATH = get_value('users', CONTROLLERS)
