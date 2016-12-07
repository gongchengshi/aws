from boto.s3.connection import Location
import aws
import codecs
from aws import USWest2 as AwsConnections


def create_bucket(s3, bucket_name):
    return s3.create_bucket(bucket_name, location=Location.USWest2)


def get_or_create_bucket(s3, bucket_name):
    return s3.lookup(bucket_name) or create_bucket(s3, bucket_name)


def bulk_delete_keys(bucket, prefix=None):
    batch = []
    for key in bucket.list(prefix):
        if len(batch) < 1000:
            batch.append(key)
        else:
            bucket.delete_keys(batch, quiet=True)
            batch = []
    if batch:
        bucket.delete_keys(batch, quiet=True)


def delete_non_empty_bucket(bucket):
    bulk_delete_keys(bucket)
    bucket.delete()


def write_key_names_to_file(bucket_name, filename):
    s3 = aws.USWest2.s3()
    bucket = s3.lookup(bucket_name)

    outfile = codecs.open(filename, 'w', 'utf-8')

    keys = bucket.list()
    for key in keys:
        # name = key.name if isinstance(key.name, str) else key.name.encode('utf-8')
        # outfile.write(name + '\n')

        outfile.write(key.name + '\n')
    outfile.close()

