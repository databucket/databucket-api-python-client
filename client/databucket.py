import getpass
import json
from datetime import datetime

from client.bundle import Bundle
from client.condition import Condition
from client.rest_client import RestClient


class Databucket:
    __DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    __service_url = None
    __user_name = None
    __rest_client = None
    __headers = {'Content-Type': 'application/json', 'Accept': '*/*'}

    def __init__(self, service_url: str, enable_logging: bool = True):
        self.__service_url = service_url
        self.__user_name = getpass.getuser()
        self.__rest_client = RestClient(headers=self.__headers, enable_logging=enable_logging)

    def set_user_name(self, user_name: str):
        self.__user_name = user_name

    def set_proxy(self, proxy: str):
        self.__rest_client.set_proxy(proxy)

    def add_header(self, name: str, value: str):
        self.__rest_client.add_header(name, value)

    def __dump_conditions(self, conditions: [Condition]) -> []:
        result = []
        for condition in conditions:
            result.append(
                dict(
                    left_source=condition.left_source,
                    left_value=condition.left_value,
                    operator=condition.operator.value,
                    right_source=condition.right_source,
                    right_value=condition.right_value
                )
            )
        return result

    def __json_to_bundle(self, bucket_name: str, json_bundle: dict) -> Bundle:
        return Bundle(
            bucket_name=bucket_name,
            bundle_id=json_bundle['bundle_id'],
            tag_name=json_bundle['tag_name'],
            locked=json_bundle['locked'],
            locked_by=json_bundle['locked_by'],
            properties=json_bundle['properties'],
            created_at=self.__parse_datetime(json_bundle['created_at']),
            created_by=json_bundle['created_by'],
            updated_at=self.__parse_datetime(json_bundle['updated_at']),
            updated_by=json_bundle['updated_by']
        )

    def __parse_datetime(self, date) -> datetime:
        if date:
            return datetime.strptime(date, self.__DATE_FORMAT)

    def insert_bundle(self, bundle: Bundle) -> Bundle:
        resource = f'/buckets/{bundle.bucket_name}/bundles?userName=' + self.__user_name
        payload = {'locked': bundle.locked, 'tag_name': bundle.tag_name, 'properties': bundle.properties}
        response = self.__rest_client.post(url=self.__service_url + resource, data=json.dumps(payload))

        bundle_id = response.json()['bundle_id']

        return self.get_bundle(bundle.bucket_name, bundle_id)

    def get_bundle(self, bucket_name: str, bundle_id: int = None, conditions: [Condition] = None, random: bool = False) -> Bundle:
        if bundle_id:
            resource = f'/buckets/{bucket_name}/bundles/{bundle_id}'

            response = self.__rest_client.get(url=self.__service_url + resource)
            resp_json = response.json()

            if resp_json['bundles'].__len__() > 0:
                json_bundle = resp_json['bundles'][0]
                return self.__json_to_bundle(bucket_name=bucket_name, json_bundle=json_bundle)
        else:
            bundles = self.get_bundles(bucket_name=bucket_name, conditions=conditions, random=random, count=1)
            if bundles:
                return bundles[0]

    def get_bundles(self, bucket_name: str, conditions: [Condition], random: bool = False, count: int = -1) -> [Bundle]:
        resource = f'/buckets/{bucket_name}/bundles/custom'

        if count > 0:
            resource += f'?limit={count}'

            if random:
                resource += '&sort=rand()'

        payload = dict(conditions=self.__dump_conditions(conditions))
        response = self.__rest_client.post(url=self.__service_url + resource, data=json.dumps(payload, ensure_ascii=False))
        resp_json = response.json()

        if resp_json['bundles'].__len__() > 0:
            bundles = []
            json_bundles = resp_json['bundles']
            for json_bundle in json_bundles:
                bundles.append(self.__json_to_bundle(bucket_name=bucket_name, json_bundle=json_bundle))
            return bundles

    def lock_bundle(self, bucket_name: str, conditions: [], random: bool = False) -> Bundle:
        bundles = self.lock_bundles(bucket_name=bucket_name, conditions=conditions, count=1, random=random)
        if bundles:
            return bundles[0]

    def lock_bundles(self, bucket_name: str, conditions: [Condition], random: bool = False, count: int = 1) -> [Bundle]:
        resource = f'/buckets/{bucket_name}/bundles/custom/lock?userName={self.__user_name}&limit={count}'

        if random:
            resource += '&sort=rand()'

        payload = dict(conditions=self.__dump_conditions(conditions))

        response = self.__rest_client.post(url=self.__service_url + resource, data=json.dumps(payload, ensure_ascii=False))
        resp_json = response.json()

        if 'bundles' in resp_json and resp_json['bundles'].__len__() > 0:
            json_bundles = resp_json['bundles']
            bundles = []
            for json_bundle in json_bundles:
                bundles.append(self.__json_to_bundle(bucket_name=bucket_name, json_bundle=json_bundle))
            return bundles

    def update_bundle(self, bundle: Bundle) -> Bundle:
        resource = f'/buckets/{bundle.bucket_name}/bundles/{bundle.bundle_id}?userName={self.__user_name}'

        payload = {
            'tag_name': bundle.tag_name,
            'locked': bundle.locked,
            'properties': bundle.properties
        }

        self.__rest_client.put(url=self.__service_url + resource, data=json.dumps(payload, ensure_ascii=False))

        return self.get_bundle(bundle.bucket_name, bundle.bundle_id)
