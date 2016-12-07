from boto.sqs.message import RawMessage as SqsMessage
from aws import USWest2 as AwsConnections

queue = AwsConnections.sqs().lookup('test_queue')


queue.write(SqsMessage(body="Hi there"))
# message = queue.read(message_attributes=['All'])
# message = queue.get_messages(attributes=['All'])
message = queue.get_messages(attributes=['SentTimestamp'])

print message[0].attributes
print message[0].message_attributes

sent = message[0].attributes['SentTimestamp']

