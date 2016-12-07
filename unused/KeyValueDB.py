import aws
from ec2.helpers import CreateSdbDomain


class KeyValueDatabases:
    SimpleDB = 1
    DynamoDB = 0
    LocalRedis = 2


class KeyValueDb:
    def __init__(self, databaseToUse):
        self.databaseToUse = databaseToUse
        self.ddb = aws.ddb()
        self.sdb = aws.sdb()

    def CreateTable(self, name):
        if self.databaseToUse == KeyValueDatabases.SimpleDB:
            CreateSdbDomain(self.sdb, self.crawlJob.CrawledUrlsTableName)
        elif self.databaseToUse == KeyValueDatabases.DynamoDB:
            pass


