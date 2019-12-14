from framework.api.services.users import UsersAPIInit


class UsersAPI(UsersAPIInit):
    def get_all_users(self, **kwargs):
        response = self.get(f'{self.base_url}{self.get_users_path}?first_name={kwargs.get("first_name")}')
        return self.parse_response_to_json(response)['result']

    def get_user_info(self, user_id):
        response = self.get(f'{self.base_url}{self.get_users_path}?{user_id}')
        return self.parse_response_to_json(response)['result']

    def create_user(self, body):
        response = self.post(f'{self.base_url}{self.create_user_path}', body=body['json'])
        return self.parse_response_to_json(response)['result']

    def delete_user(self, user_id):
        response = self.delete(f'{self.base_url}{self.get_users_path}/{user_id}')
        return self.parse_response_to_json(response)['result']
