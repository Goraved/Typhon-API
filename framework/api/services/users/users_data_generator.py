from framework.utilities import Utilities


class BooksDataGenerator:

    @staticmethod
    def generate_user_body(**kwargs):
        rand_key = Utilities.generate_random_key(4)
        body = {
            "first_name": kwargs.get('first_name', f'first_name_{rand_key}'),
            "last_name": kwargs.get('last_name', f'last_name_{rand_key}'),
            "gender": kwargs.get('gender', 'male'),
            "email": kwargs.get('email', f'email_{rand_key}@email.com'),
            "status": kwargs.get('status', 'active')
        }
        return {'json': Utilities.convert_dict_to_json(body), 'dict': body}
