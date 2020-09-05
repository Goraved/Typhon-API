from framework.utilities import Utilities


class UsersDataGenerator:

    @staticmethod
    def generate_user_body(**kwargs):
        rand_key = Utilities.generate_random_key(4)
        body = {
            "name": kwargs.get('name', f'first_name_{rand_key} last_name_{rand_key}'),
            "gender": kwargs.get('gender', 'Male'),
            "email": kwargs.get('email', f'email_{rand_key}@email.com'),
            "status": kwargs.get('status', 'Active')
        }
        return {'json': Utilities.convert_dict_to_json(body), 'dict': body}
