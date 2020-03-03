import json
from http.client import responses
from requests import Response, Session
import requests


class RestClient:
    __enable_logging = False
    __log_headers = False
    __headers = None
    __proxy = None
    request = None
    response = None

    def __init__(self, headers=None, enable_logging: bool = False):
        if headers is None:
            headers = {}
        self.__headers = headers
        self.__enable_logging = enable_logging

    def set_proxy(self, proxy):
        self.__proxy = proxy

    def add_header(self, name: str, value: str):
        self.__headers[name] = value

    def __send_request(self, method: str, url: str, data: str = None, verify_response_status: bool = True, params: dict = None) -> Response:
        self.request = None
        self.response = None

        self.request = requests.Request(method, url, headers=self.__headers, data=data, params=params).prepare()

        session = Session()
        if self.__proxy:
            session.proxies = {'http': self.__proxy, 'https': self.__proxy}
        session.verify = False  # SSL Verification

        try:
            self.response = session.send(self.request, timeout=30)
        except requests.exceptions.InvalidProxyURL:
            raise AssertionError(f'InvaliProxydURL: {session.proxies["https"]} used when connecting to {url}.')
        except requests.exceptions.InvalidURL:
            raise AssertionError(f'InvalidURL exception for {url}.')
        except requests.exceptions.ConnectTimeout:
            raise AssertionError(f'ConnectTimeout ({30} s) exception for {url}.')
        except requests.exceptions.ReadTimeout:
            raise AssertionError(f'Response ReadTimeout ({30} s) exception for {url}.')
        except requests.exceptions.ConnectionError as ex:
            raise AssertionError(f'Failed to connect to {url}.\n{ex} ')

        if self.__enable_logging:
            self.log_request_response()

        if verify_response_status:
            if not self.response.ok:
                raise AssertionError(f'Unexpected response status: {self.response.status_code} ({responses[self.response.status_code]}).\nRequested URL: {url}.')

        return self.response

    def get(self, url: str, verify_response_status: bool = True) -> Response:
        return self.__send_request('GET', url=url, data=None, verify_response_status=verify_response_status)

    def post(self, url: str, data: str = None, verify_response_status: bool = True) -> Response:
        return self.__send_request('POST', url=url, data=data, verify_response_status=verify_response_status)

    def put(self, url: str, data: str = None, verify_response_status: bool = True) -> Response:
        return self.__send_request('PUT', url=url, data=data, verify_response_status=verify_response_status)

    def delete(self, url: str, verify_response_status: bool = True, params: dict = None) -> Response:
        return self.__send_request('DELETE', url=url, data=None, verify_response_status=verify_response_status, params=params)

    def log_request(self):
        if self.__log_headers:
            headers = '\n'.join(f'{k}: {v}' for k, v in self.request.headers.items())
            headers = f'\n{headers}'
            print(f"Request headers: {headers}")

        name = f'{self.request.method} {self.request.url}'
        body = ''

        if self.request.body:
            if 'json' in self.request.headers['Content-Type']:
                body = self.__beautify_json(self.request.body)
            else:
                body = self.request.body

        print(name)
        print(body)

    def log_response(self):
        if self.__log_headers:
            headers = '\n'.join(f'{k}: {v}' for k, v in self.response.headers.items())
            headers = f'\n{headers}'
            print(f"Response headers: {headers}")

        name = f'Response received in {"%.1f" % self.response.elapsed.total_seconds()} s with status: {self.response.status_code}'
        body = ''

        if 'Content-Type' in self.response.headers:
            if 'json' in self.response.headers['Content-Type']:
                body = self.__beautify_json(self.response.text)
        else:
            body = self.response.text

        print(name)
        print(body)

    def log_request_response(self):
        self.log_request()
        self.log_response()

    def __beautify_json(self, text_or_dict)->str:
        try:
            if isinstance(text_or_dict, dict):
                return json.dumps(text_or_dict, indent=2, sort_keys=False)
            else:
                return json.dumps(json.loads(text_or_dict), indent=2, sort_keys=False)
        except Exception as e:
            raise AssertionError(f'Bad JSON string:\n{text_or_dict}\n{e.args}')
