from aws import USWest2 as AwsConnections
from aws.sqs import create_message
from boto.sqs.message import Message as SqsMessage

queue = AwsConnections.sqs().create_queue('test_queue', 60)  # 1 Minutes
queue.set_attribute('DelaySeconds', 0)
queue.set_attribute('MaximumMessageSize', 10 * 1024)  # 10 KB
queue.set_attribute('MessageRetentionPeriod', 1209600)  # 14 Days.
queue.set_attribute('ReceiveMessageWaitTimeSeconds', 20)  # 20 seconds

# queue.write(create_message("Hi there"))

msg = queue.read()

dummy_msg = SqsMessage()
dummy_msg.receipt_handle = msg.receipt_handle
dummy_msg.queue = queue

dummy_msg.delete()
