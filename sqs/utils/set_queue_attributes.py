import sys
from aws import USWest2 as AwsConnections

prefix = sys.argv[1]

sqs = AwsConnections.sqs()

for queue in sqs.get_all_queues(prefix):
    queue.set_attribute('MaximumMessageSize', 256144)  # 256 KB
