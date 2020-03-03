import datetime


class Bundle:
    bundle_id = None
    bucket_name = None
    locked = None
    locked_by = None
    tag_name = None
    properties = None
    created_at = None
    created_by = None
    updated_at = None
    updated_by = None

    def __init__(self,
                 bucket_name: str,
                 bundle_id: int = None,
                 tag_name: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 properties=None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None):

        self.bucket_name = bucket_name
        self.bundle_id = bundle_id
        self.tag_name = tag_name
        self.locked = locked
        self.locked_by = locked_by
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def get_property(self, path: str):
        return self.__get(self.properties, path)

    def set_property(self, path: str, value):
        self.__put(self.properties, path, value)

    def remove_property(self, path: str):
        self.__remove(self.properties, path)

    def __put(self, d, keys, item):
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key not in d:
                d[key] = {}
            self.__put(d[key], rest, item)
        else:
            d[keys] = item

    def __get(self, d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key in d:
                return self.__get(d[key], rest)
            else:
                return None
        else:
            if keys in d:
                return d[keys]
            else:
                return None

    def __remove(self, d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key in d:
                self.__remove(d[key], rest)
        else:
            if keys in d:
                del d[keys]
