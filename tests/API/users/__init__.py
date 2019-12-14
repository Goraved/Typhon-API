import allure

from framework.api.services.users.users_api import UsersAPI
from framework.api.services.users.users_data_generator import BooksDataGenerator
from tests.API import TestBase


@allure.feature('Users API')
class TestUsersBase(TestBase):
    def setup(self):
        self.users_api = UsersAPI()
        self.users_data_generator = BooksDataGenerator()
