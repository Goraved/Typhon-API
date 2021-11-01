from framework.api.services.users_api import UsersAPIInit


class UsersAPI(UsersAPIInit):

    def get_all_users(self, **kwargs) -> dict:
        response = self.get(f'{self.base_url}{self.get_users_path}?name={kwargs.get("name")}')
        return self.parse_response_to_json(response)['data']

    def get_user_info(self, user_id: int) -> dict:
        response = self.get(f'{self.base_url}{self.get_users_path}?{user_id}')
        return self.parse_response_to_json(response)['data']

    def create_user(self, body: dict) -> dict:
        response = self.post(f'{self.base_url}{self.create_user_path}', data=body['json'])
        return self.parse_response_to_json(response)['data']

    def delete_user(self, user_id: int) -> dict:
        response = self.delete(f'{self.base_url}{self.get_users_path}/{user_id}')
        return self.parse_response_to_json(response)['data']
