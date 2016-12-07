from aws import USWest2 as aws
from aws.sqs import oldest_message_timestamp


queue_prefix = "siemens17042013"
queue_prefix = "siemens17042013--103_28_22_0_24"

print "QueueName,Count,OldestMessageTimestamp"

for queue in aws.sqs().get_all_queues(queue_prefix):
    print '%s,%s,%s' % (queue.name, queue.count(), oldest_message_timestamp(queue) or '')
