from aws import USWest2
import aws.sdb

sdb = USWest2.sdb()
domain = sdb.lookup('crawled-urls.siemens17042013')
# domain = sdb.lookup('logs.siemens17042013')
# domain = sdb.lookup('skipped-urls.siemens17042013')
# domain = sdb.lookup('failed-urls.siemens17042013')
count = aws.sdb.count(domain)
print count
