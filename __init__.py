import boto
import boto.ec2
import boto.ec2.cloudwatch
import boto.sdb
import boto.sqs
import boto.dynamodb
import boto.sns
from boto.s3.connection import S3Connection

from aws.constants import AwsAccessKey, AwsSecretKey


class USWest2:
    region = 'us-west-2'

    @staticmethod
    def sdb():
        return boto.sdb.connect_to_region(USWest2.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def ddb():
        return boto.dynamodb.connect_to_region(USWest2.region,
                                               aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def ec2():
        return boto.ec2.connect_to_region(USWest2.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def cloudwatch():
        return boto.ec2.cloudwatch.connect_to_region(USWest2.region,
                                                     aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def sqs():
        return boto.sqs.connect_to_region(USWest2.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def s3():
        return boto.s3.connect_to_region(USWest2.region,
                                         aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def sns():
        return boto.sns.connect_to_region(USWest2.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)


class USEast1:
    region = 'us-east-1'

    @staticmethod
    def sdb():
        return boto.sdb.connect_to_region(USEast1.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def ddb():
        return boto.dynamodb.connect_to_region(USEast1.region,
                                               aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def ec2():
        return boto.ec2.connect_to_region(USEast1.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def sqs():
        return boto.sqs.connect_to_region(USEast1.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    @staticmethod
    def s3():
        return S3Connection(AwsAccessKey, AwsSecretKey)

    @staticmethod
    def sns():
        return boto.sns.connect_to_region(USEast1.region,
                                          aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)