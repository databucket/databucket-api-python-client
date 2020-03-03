import csv

from client.bundle import Bundle
from client.databucket import Databucket
from constant.bucket import Bucket
from constant.property import Property
from constant.tag import Tag

databucket = Databucket(service_url='http://localhost:8080/api', enable_logging=True)

with open('../resources/import/users.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)

    # skip header row
    next(reader)

    for row in reader:
        bundle = Bundle(bucket_name=Bucket.USERS)
        bundle.tag_name = Tag.ACTIVE
        bundle.locked = False
        bundle.set_property(Property.FIRST_NAME, row[0])
        bundle.set_property(Property.LAST_NAME, row[1])
        bundle.set_property(Property.COMPANY, row[2])
        bundle.set_property(Property.ADDRESS, row[3])
        bundle.set_property(Property.CITY, row[4])
        bundle.set_property(Property.STATE, row[5])
        bundle.set_property(Property.POST, row[6])
        bundle.set_property(Property.PHONE, row[7])
        bundle.set_property(Property.EMAIL, row[8])
        bundle.set_property(Property.WEB, row[9])
        databucket.insert_bundle(bundle)

    csv_file.close()

print('Done.')
