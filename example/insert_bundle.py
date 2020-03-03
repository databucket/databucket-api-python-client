from client.bundle import Bundle
from client.databucket import Databucket
from constant.bucket import Bucket
from constant.property import Property
from constant.tag import Tag

databucket = Databucket(service_url='http://localhost:8080/api', enable_logging=True)

bundle = Bundle(Bucket.USERS)
bundle.tag_name = Tag.ACTIVE
bundle.locked = False
bundle.set_property(Property.FIRST_NAME, 'John')
bundle.set_property(Property.LAST_NAME, 'Brown')
bundle.set_property(Property.ADDRESS, '123 Avenue')
bundle.set_property(Property.COMPANY, 'Google')
bundle.set_property(Property.EMAIL, 'jb@gmail.com')
bundle.set_property(Property.PHONE, '0965-223-212')
bundle.set_property(Property.WEB, 'https://www.jbrown.com')

bundle = databucket.insert_bundle(bundle)

