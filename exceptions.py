class AwsErrorCodes:
    SqsNonExistentQueue = 'AWS.SimpleQueueService.NonExistentQueue'


class NonExistantSqsQueueException(Exception):
    def __init__(self, queue_name):
        self.queue_name = queue_name
        Exception.__init__(self, "SQS Queue '%s' no longer exists" % queue_name)
