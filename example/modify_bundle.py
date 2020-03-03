from client.condition import Condition
from client.databucket import Databucket
from client.field import Field
from client.operator import Operator
from client.source import Source
from constant.bucket import Bucket
from constant.property import Property
from constant.tag import Tag

databucket = Databucket(service_url='http://localhost:8080/api', enable_logging=True)

conditions = [
    Condition(left_source=Source.FIELD, left_value=Field.TAG_NAME, operator=Operator.EQUAL, right_source=Source.CONST, right_value=Tag.ACTIVE),
    Condition(left_source=Source.PROPERTY, left_value=Property.CITY, operator=Operator.LIKE, right_source=Source.CONST, right_value='%Rock%')
]

# Get and lock one bundle for given conditions
bundle = databucket.lock_bundle(bucket_name=Bucket.USERS, conditions=conditions, random=True)

# Get one bundle for given conditions
# bundle = databucket.get_bundle(bucket_name=Bucket.USERS, conditions=conditions, random=True)

bundle.tag_name = Tag.TRASH
bundle.locked = False

databucket.update_bundle(bundle)
