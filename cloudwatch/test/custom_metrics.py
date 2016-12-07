from datetime import datetime
import time
import random

from aws import USWest2 as AwsConnections

cw = AwsConnections.cloudwatch()

for _ in xrange(0, 30):
    cw.put_metric_data(namespace='atrax/selinc20150101/i-567890:0',
                       name='queue_count',
                       unit='Count',
                       timestamp=datetime.utcnow(),
                       dimensions={'fetcher_id': 'i-567890:0'},
                       value=random.randint(10, 20))
    time.sleep(10)
