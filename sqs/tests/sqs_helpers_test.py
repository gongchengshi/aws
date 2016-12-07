import aws
from sqs.sqs_helpers import MoveSqsQueueContents

sqs = aws.sqs()
source = sqs.get_queue('temp')
dest = sqs.get_queue('high-priority-compliant-frontier_' + 'siemens17042013')

MoveSqsQueueContents(source, dest)
