import csv
from client.condition import Condition
from client.databucket import Databucket
from client.field import Field
from client.operator import Operator
from client.source import Source
from constant.bucket import Bucket
from constant.property import Property
from constant.tag import Tag

databucket = Databucket(service_url='http://localhost:8080/api', enable_logging=False)

conditions = [
    Condition(left_source=Source.FIELD, left_value=Field.TAG_NAME, operator=Operator.EQUAL, right_source=Source.CONST, right_value=Tag.ACTIVE),
    Condition(left_source=Source.PROPERTY, left_value=Property.CITY, operator=Operator.LIKE, right_source=Source.CONST, right_value='%Rock%')
]

bundles = databucket.get_bundles(bucket_name=Bucket.USERS, conditions=conditions)

with open('../resources/export/users.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["ID", "Tag", "First name", "Last name", "City", "Email"])

    for bundle in bundles:
        writer.writerow([
            bundle.bundle_id,
            bundle.tag_name,
            bundle.get_property(Property.FIRST_NAME),
            bundle.get_property(Property.LAST_NAME),
            bundle.get_property(Property.CITY),
            bundle.get_property(Property.EMAIL)
        ])

    csv_file.close()

print('Done.')
