import json

import allure
import requests
import xmltodict
from requests import Response

from configuration.config_parse import MAIN_API_URL, TOKEN
from framework.utilities import log, fix_api_properties, create_executor_file


class BaseAPI:
    properties = False
    _REQUEST_MSG = 'Sent {} request with: \n  URL = {} \n  Headers = {} \n Params = {}'
    _REQUEST_W_BODY_MSG = 'Sent {} request with: \n  URL = {} \n  Headers = {} \n  Body = {} \n Params = {}'
    _RESPONSE_MSG = 'Status = {} \n Response = {}'

    def __init__(self):
        # Gather info for Allure environment block
        if not self.properties:
            fix_api_properties()
            create_executor_file()
            self.properties = True
        self.log = log
        self.base_url = MAIN_API_URL
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    @allure.step('[API] GET')
    def get(self, url: str, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        is_logged = log(self._REQUEST_MSG.format('GET', url, headers, params), msg_type='REQUEST')
        response = requests.get(url, headers=headers)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @allure.step('[API] POST')
    def post(self, url: str, data, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        is_logged = log(self._REQUEST_W_BODY_MSG.format('POST', url, headers, data, params), msg_type='REQUEST')
        response = requests.post(url, data=data, headers=headers)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @allure.step('[API] POST upload')
    def post_upload(self, url: str, files, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        del headers['Content-Type']
        is_logged = log(self._REQUEST_W_BODY_MSG.format('POST', url, headers, files, params), msg_type='REQUEST')
        response = requests.post(url, headers=headers, files=files)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @allure.step('[API] PUT')
    def put(self, url: str, data=None, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        is_logged = log(self._REQUEST_W_BODY_MSG.format('PUT', url, headers, data, params), msg_type='REQUEST')
        if data is None:
            response = requests.put(url, headers=headers)
        else:
            response = requests.put(url, data=data, headers=headers)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @allure.step('[API] PATCH')
    def patch(self, url: str, data, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        is_logged = log(self._REQUEST_W_BODY_MSG.format('PATCH', url, headers, data, params), msg_type='REQUEST')
        response = requests.patch(url, data=data, headers=headers)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @allure.step('[API] DELETE')
    def delete(self, url: str, params: dict = None, **kwargs) -> Response:
        headers = kwargs.get('headers', self.headers)
        is_logged = log(self._REQUEST_MSG.format('DELETE', url, headers, params), msg_type='REQUEST')
        response = requests.delete(url, headers=headers)
        if is_logged:
            log(self._RESPONSE_MSG.format(response.status_code, response.content), msg_type='RESPONSE')
        if 'response_code' in kwargs:
            BaseAPI.check_status_code(response, kwargs.get('response_code'))
        else:
            BaseAPI.check_status_code_success(response)
        return response

    @staticmethod
    def check_status_code_success(response: Response):
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
    def check_status_code(response: Response, expected_code: int):
        """
        Check status code is in success category heading
        """
        try:
            error = BaseAPI.parse_response_to_json(response)
        except:
            error = 'Unable to parse error'
        assert response.status_code == expected_code, f'Wrong response code from the server. ' \
                                                      f'Expected = {expected_code}, ' \
                                                      f'received = {response.status_code} | error = {error}'

    @staticmethod
    @allure.step('Generating request link')
    def generate_request_link(url: str, attributes) -> str:
        return MAIN_API_URL + url + '&'.join(
            ['%s=%s' % (key, value) for (key, value) in attributes.items()])

    @staticmethod
    def dict_to_url_parameters(parameters) -> str:
        return '&'.join([f'{_}={parameters[_]}' for _ in parameters])

    @staticmethod
    def parse_response_to_json(response: Response) -> dict:
        return response.json()

    @staticmethod
    def parse_xml_to_json(response: Response) -> dict:
        xml_response = response.content
        string_response = json.dumps(xmltodict.parse(xml_response))
        dict_response = json.loads(string_response)
        return dict_response

