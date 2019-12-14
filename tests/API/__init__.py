import allure


@allure.epic('API migration')
class TestBase:
    @staticmethod
    @allure.step('Compare actual and expected values')
    def compare_values(field, actual_value, expected_value):
        assert actual_value == expected_value, f"{field} is - '{actual_value}' instead of - '{expected_value}'"
