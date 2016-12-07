from aws import USWest2 as aws
sqs = aws.sqs()
queue = sqs.lookup('sel17062013--208_73_211_10_32')
try:
    msg = queue.get_messages()
except Exception, e:
    pass

