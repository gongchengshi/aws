from boto.s3.key import Key
from aws import USWest2 as AwsConnection
from aws.s3 import bulk_delete_keys

s3 = AwsConnection.s3()

def test_bulk_delete_keys():
    bucket = s3.lookup('jeremymclain.dummy-bucket')

    # bulk_delete_keys(bucket, '610509431426/queue_1')
    bulk_delete_keys(bucket, '610509431426')

test_bulk_delete_keys()

def lookup_test():
    bucket = s3.lookup('atrax-configuration-management')

    print bucket

def path_test():
    bucket = s3.lookup('nnnn7777')
    key = Key(bucket, 'one/two/three/four/five/')
    key.set_contents_from_string("Contents")

def url_decoding_test():
    bucket = s3.lookup('nnnn7777')
    # key = Key(bucket, 'https://www.google.com/a%20gogo/search?q=%E6%9A%91%E5%81%87&oq=%E6%9A%91%E5%81%87&aqs=chrome..69i57j0l5.18863j0j4&sourceid=chro+me&es_sm=93&ie=UTF-8')
    key = Key(bucket, 'https://www.google.com/a gogo/search?q=暑假&aqs=chrome..69i57j0l5.18863j0j4&sourceid=chro me&es_sm=93&ie=UTF-8')
    key.set_contents_from_string("Contents")

lookup_test()
