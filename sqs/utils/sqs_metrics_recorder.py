#!/usr/bin/python2

from datetime import datetime
import time
import os
import argparse
import csv

import aws

from atrax.common.crawl_job import CrawlJob


parser = argparse.ArgumentParser()
parser.add_argument('job', type=str)
parser.add_argument('minutes', type=int)
cmdlineArgs = vars(parser.parse_args())

crawl_job = CrawlJob(cmdlineArgs['job'])

filename = '%s_sqs_metrics.csv' % crawl_job.Name

sqs = aws.sqs()

robotExclusionCompliantFrontier = sqs.get_queue(crawl_job.CompliantFrontierQueueName)
highPriorityRobotExclusionCompliantFrontier = sqs.get_queue(crawl_job.HighPriorityComplientFrontierQueueName)
robotExclusionNonCompliantFrontier = sqs.get_queue(crawl_job.NonCompliantFrontierQueueName)


def csv_writer(f):
    return csv.DictWriter(f,
                          fieldnames=[
                              'timestamp',
                              crawl_job.CompliantFrontierQueueName,
                              crawl_job.HighPriorityComplientFrontierQueueName,
                              crawl_job.NonCompliantFrontierQueueName,
                              'sum'])


def open_file():
    fileExists = os.path.exists(filename)
    f = open(filename, 'a')
    if not fileExists:
        csv_writer(f).writeheader()
    return f


print "Running"

while True:
    print '.'
    robotExclusionCompliantFrontierCount = robotExclusionCompliantFrontier.count()
    highPriorityRobotExclusionCompliantFrontierCount = highPriorityRobotExclusionCompliantFrontier.count()
    robotExclusionNonCompliantFrontierCount = robotExclusionNonCompliantFrontier.count()

    sizes = {
        'timestamp': datetime.now(),
        crawl_job.CompliantFrontierQueueName: robotExclusionCompliantFrontierCount,
        crawl_job.HighPriorityComplientFrontierQueueName: highPriorityRobotExclusionCompliantFrontierCount,
        crawl_job.NonCompliantFrontierQueueName: robotExclusionNonCompliantFrontierCount,
        'sum': (robotExclusionCompliantFrontierCount +
                highPriorityRobotExclusionCompliantFrontierCount +
                robotExclusionNonCompliantFrontierCount)
    }

    with open_file() as f:
        csv_writer(f).writerow(sizes)

    if sizes['sum'] > 0:
        time.sleep(cmdlineArgs['minutes'] * 60)
