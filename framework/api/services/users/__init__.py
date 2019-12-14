from configuration.config_parse import global_config
from framework.api.base_api import BaseAPI


class UsersAPIInit(BaseAPI):
    def __init__(self):
        super().__init__()
        self.get_users_path = global_config.get('USERS_PATH', 'get_users')
        self.create_user_path = global_config.get('USERS_PATH', 'create_user')
