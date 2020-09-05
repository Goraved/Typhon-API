from configuration.config_parse import USERS_PATH
from framework.api.base_api import BaseAPI


class UsersAPIInit(BaseAPI):
    def __init__(self):
        super().__init__()
        self.get_users_path = USERS_PATH['get_users']
        self.create_user_path = USERS_PATH['create_user']
