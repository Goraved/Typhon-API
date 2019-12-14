import allure
from allure_commons._allure import step

from configuration.config_parse import TEST_CASE
from tests.API.users import TestUsersBase


@allure.feature('Users API')
class TestUsersApi(TestUsersBase):
    # To get token please register here -> https://gorest.co.in/user/login.html
    @allure.testcase('[link to test case]', name=TEST_CASE)
    @allure.link('[link]', name='[link name]')
    @allure.title('Check CRUD for users')
    def test_crud_user(self):
        with step('Create new user'):
            generated_body = self.users_data_generator.generate_user_body()
            created_user = self.users_api.create_user(generated_body)
        with step('Check user appeared in the list'):
            users = self.users_api.get_all_users(first_name=generated_body['dict']['first_name'])
            assert created_user['id'] in [_['id'] for _ in users], 'Create user missed in the total list'
        with step('Delete user'):
            self.users_api.delete_user(created_user['id'])
        with step('Check user missed in the list'):
            users = self.users_api.get_all_users(first_name=generated_body['dict']['first_name'])
            assert created_user['id'] not in [_['id'] for _ in users]
            'Deleted user still present in the total list'
