import json

import allure
import requests
import xmltodict as xmltodict

from configuration.config_parse import MAIN_API_URL, TOKEN
from framework.utilities import Utilities


class BaseAPI:
    properties = False

    def __init__(self):
        # Gather info for Allure environment block
        if not self.properties:
            Utilities.fix_api_properties()
            Utilities.create_executor_file()
            self.properties = True
        self.log = Utilities.log
        self.base_url = MAIN_API_URL
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    def get(self, path, **kwargs):
        headers = kwargs.get('headers', self.headers)
        self.log(f'Sent GET request with: \n  URL = {path} \n  Headers = {headers}', msg_type='REQUEST')
        response = requests.get(path, headers=headers)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    def post(self, path, body, **kwargs):
        headers = kwargs.get('headers', self.headers)
        self.log(f'Sent POST request with: \n  URL = {path} \n  Headers = {headers} \n  Body = {body}',
                 msg_type='REQUEST')
        response = requests.post(path, data=body, headers=headers)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    def post_upload(self, path, files, **kwargs):
        headers = kwargs.get('headers', self.headers)
        del headers['Content-Type']
        self.log(f'Sent POST request with: \n  URL = {path} \n  Headers = {headers} \n File = {files}',
                 msg_type='REQUEST')
        response = requests.post(path, headers=headers, files=files)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    def put(self, path, body={}, **kwargs):
        headers = kwargs.get('headers', self.headers)
        self.log(f'Sent PUT request with: \n  URL = {path} \n  Headers = {headers} \n  Body = {body}',
                 msg_type='REQUEST')
        if body == {}:
            response = requests.put(path, headers=headers)
        else:
            response = requests.put(path, data=body, headers=headers)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    def patch(self, path, body, **kwargs):
        headers = kwargs.get('headers', self.headers)
        self.log(f'Sent PATCH request with: \n  URL = {path} \n  Headers = {headers} \n  Body = {body}',
                 msg_type='REQUEST')
        response = requests.patch(path, data=body, headers=headers)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    def delete(self, path, **kwargs):
        headers = kwargs.get('headers', self.headers)
        self.log(f'Sent DELETE request with: \n  URL = {path} \n  Headers = {headers}', msg_type='REQUEST')
        response = requests.delete(path, headers=headers)
        self.log(f'Status = {response.status_code} \n Response = {response.content}', msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @staticmethod
    def check_status_code_success(response):
        """
        Check status code is in success category heading
        """
        try:
            error = BaseAPI.parse_response_to_json(response)
        except:
            try:
                xml_response = BaseAPI.parse_xml_to_json(response)
                error = xml_response['Error']['Message']
            except:
                error = 'Unable to parse error'
        assert str(response.status_code)[0] == '2', f'Response code = {response.status_code}, ' \
                                                    f'error = {error}'

    @staticmethod
    def check_status_code(response, expected_code):
        """
        Check status code is in success category heading
        """
        try:
            error = BaseAPI.parse_response_to_json(response)
        except:
            error = 'Unable to parse error'
        assert response.status_code == expected_code, f'Wrong response code from the server. Expected = {expected_code}, ' \
                                                      f'received = {response.status_code} | error = {error}'

    @allure.step('Generating request link')
    def generate_request_link(self, url, attributes):
        return MAIN_API_URL + url + '&'.join(
            ['%s=%s' % (key, value) for (key, value) in attributes.items()])

    @staticmethod
    def dict_to_url_parameters(parameters):
        return '&'.join([f'{_}={parameters[_]}' for _ in parameters])

    @staticmethod
    def parse_response_to_json(response):
        return response.json()

    @staticmethod
    def parse_xml_to_json(response):
        xml_response = response.content
        string_response = json.dumps(xmltodict.parse(xml_response))
        dict_response = json.loads(string_response)
        return dict_response

    # ---> OLD METHODS

    # Get value from response by needed field
    @allure.step('Get value by specific field')
    def get_value(self, field, response):
        values = response.json()
        return values.get(field)

    # Check that all mentioned fields present in response
    @allure.step('Check that all needed fields present')
    def check_all_fields_present(self, fields, response):
        response_values = response.json()
        missed_fields = []
        for field in fields:
            if field not in response_values:
                missed_fields.append(field)
        if len(missed_fields) is 0:
            missed_fields = None
        else:
            ', '.join(missed_fields)
        return missed_fields

    # Check that all fields has needed types
    @allure.step('Check that all fields have correct format type')
    def check_types_of_fields(self, types, response):
        wrong_types = []
        for field_type in types:
            value = self.get_value(field_type, response)
            actual_type = str(type(value).__name__)
            expected_type = types.get(field_type)
            if actual_type != expected_type:
                wrong_types.append('%s is {%s} instead of {%s}' % (field_type, actual_type, expected_type))
        if len(wrong_types) is 0:
            wrong_types = None
        else:
            ', '.join(wrong_types)
        return wrong_types
