import allure

from framework.api.services.users_api.users_api import UsersAPI
from framework.api.services.users_api.users_data_generator import UsersDataGenerator
from tests.api import TestBase


@allure.feature('Users API')
class TestUsersBase(TestBase):
    @classmethod
    def setup_class(cls):
        cls.users_api = UsersAPI()
        cls.users_data_generator = UsersDataGenerator()
