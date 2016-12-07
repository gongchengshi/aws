from boto.sqs.message import RawMessage as SqsMessage

from aws import USWest2
from aws.s3 import get_or_create_bucket
from aws.sqs import persist_to_s3, restore_from_s3


def test_sqs_to_s3_to_sqs():
    sqs = USWest2.sqs()
    s3 = USWest2.s3()

    queue1 = sqs.create_queue("dummy_queue_1")
    message = SqsMessage(body="message 1")
    queue1.write(message)
    message = SqsMessage(body="message 2")
    queue1.write(message)

    queue2 = sqs.create_queue("dummy_queue_2")
    message = SqsMessage(body="message 1")
    queue2.write(message)
    message = SqsMessage(body="message 2")
    queue2.write(message)

    persisted_queues_bucket = get_or_create_bucket(s3, "jeremymclain.dummy-bucket")

    persist_to_s3(sqs, 'dummy_queue', persisted_queues_bucket)

    restore_from_s3(sqs, persisted_queues_bucket)


test_sqs_to_s3_to_sqs()
