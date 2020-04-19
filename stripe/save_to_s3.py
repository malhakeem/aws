from __future__ import print_function
import json
import urllib
import boto3
import datetime
import csv, re
import botocore

print('loading function...')


def save_source_to_csv(message, context):
    BUCKET_NAME = 'testbucketmalhakeem'  # 'testbucketmalhakeem' # s3 bucket name
    KEY = 'tmp3/OUTPUT.csv'  # path and file

    s3 = boto3.resource("s3")
    # access the json source object
    data = message['data']
    data_object = data['object']
    object_source = data_object['source']

    # csv column names from the json source object
    source_items_list = ['id', 'object', 'last4', 'type', 'brand', 'exp_month', 'exp_year', 'fingerprint', 'customer',
                         'country', 'name', 'address_line1', 'address_line2', 'address_city',
                         'address_state', 'address_zip', 'address_country', 'cvc_check', 'address_line1_check',
                         'address_zip_check']

    # list of values of the json source object
    source_item_values_list = [object_source[source_items_list[0]], object_source[source_items_list[1]],
                               object_source[source_items_list[2]], object_source[source_items_list[3]],
                               object_source[source_items_list[4]], object_source[source_items_list[5]],
                               object_source[source_items_list[6]], object_source[source_items_list[7]],
                               object_source[source_items_list[8]],
                               object_source[source_items_list[9]], object_source[source_items_list[10]],
                               object_source[source_items_list[11]], object_source[source_items_list[12]],
                               object_source[source_items_list[13]],
                               object_source[source_items_list[14]], object_source[source_items_list[15]],
                               object_source[source_items_list[16]], object_source[source_items_list[17]],
                               object_source[source_items_list[18]],
                               object_source[source_items_list[19]]]

    try:
        s3.Object(BUCKET_NAME, KEY).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # target file does not exist
            # create csv file in /tmp and save it to the s3 bucket
            with open('/tmp/data.csv'
                    , 'w') as file:
                csv_file = csv.writer(file)
                csv_file.writerow(source_items_list)
                csv_file.writerow(source_item_values_list)
            csv_binary = open('/tmp/data.csv', 'rb').read()
            obj = s3.Object(BUCKET_NAME, KEY)
            obj.put(Body=csv_binary)
            return 'new csv file created'

        else:
            # something gone wrong
            return e.response  # 'error'

    else:
        # file exists in target
        # append to the file
        # 1. read the s3 file
        # 2. save it in /tmp
        # 3. append the new row from json source object
        # 4. save it again in s3
        obj = s3.Object(BUCKET_NAME, KEY)
        body = obj.get()['Body'].read()

        body_csv = body.decode('utf-8').splitlines()

        with open("/tmp/data.csv", "w") as file:
            csv_file = csv.writer(file)
            for line in body_csv:
                csv_file.writerow(re.split(',', line))
            csv_file.writerow(source_item_values_list)
        csv_binary = open('/tmp/data.csv', 'rb').read()
        print(csv_binary)
        obj = s3.Object(BUCKET_NAME, KEY)
        obj.put(Body=csv_binary)

        return 'appended to existing csv file'
