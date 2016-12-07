import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from aws import USWest2 as aws

queue_prefix = "siemens17042013"
queue_prefix = "siemens17042013--103_28_22_0_24"
start_datetime = 1373500800

for queue in aws.sqs().get_all_queues(queue_prefix):
    print 'Recycling', queue.name

    count = 0
    breakOuter = False
    while not breakOuter:
        msgs = queue.get_messages(num_messages=10, visibility_timeout=60,
                                  wait_time_seconds=0, attributes='SentTimestamp')
        if len(msgs) == 0:
            break

        msgsToDelete = []
        for msg in msgs:
            timestamp = int(msg.attributes['SentTimestamp'])/1000.0
            if timestamp > start_datetime:
                breakOuter = True
                break
            queue.write(queue.new_message(msg.get_body()))
            msgsToDelete.append(msg)
            count += 1

        if len(msgsToDelete) > 0:
            if not queue.delete_message_batch(msgsToDelete):
                print "Failed to delete messages"
    print 'Finished recycling %s messages in %s' % (count, queue.name)
