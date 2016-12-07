def GetFreeCrawlerInstances(self, max):
    reservations = self.ec2.get_all_instances()
    crawlerInstances = []

    instances = [i for r in reservations for i in r.instances]

    num = 0

    for i in instances:
        if i.__dict__['tags']['Purpose'] == 'Crawler' and i.state != 'running':
            crawlerInstances.append(i)
            num += 1
            if num == max:
                break

    return crawlerInstances


def GetFreeJobInstances(self):
    return [i for i in self.GetFreeCrawlerInstances(10000) if i.__dict__['tags'][JobEc2TagName] == self.crawlJob.Name]


def CreateComputingInstances(self, num):
    reservation = self.ec2.run_instances(
        AmiId,
        min_count=num,
        key_name=Ec2KeyPairName,
        security_groups=[PullmanSshSecurityGroupName],
        instance_type='t1.micro',
        placement=AwsRegion,
        instance_initiated_shutdown_behavior='stop'
    )

    # The documentation says 'resource_ids' so I'm not entirely sure that reservation.id is correct here
    self.ec2.create_tags([reservation.id], {'Purpose': 'Crawler', JobEc2TagName: self.crawlJob.Name})

    return reservation


def SetupComputingInstances(self, num):
    instances = self.GetFreeCrawlerInstances(num)

    for instance in instances:
        # The documentation says 'resource_ids' so I'm not entirely sure that instance.id is correct here
        self.ec2.create_tags([instance.id], {'Purpose': 'Crawler', JobEc2TagName: self.crawlJob.Name})

    if len(instances) < num:
        self.CreateComputingInstances(num - len(instances))

    instances = self.GetFreeJobInstances()

    unassociatedAddresses = []
    for address in self.ec2.get_all_addresses():
        if address.instance_id is None:
            unassociatedAddresses.append(address)

    for instance in instances:
        if instance.ip_address is None:
            if unassociatedAddresses:
                unassociatedAddresses.pop().associate(instance.id)
            else:
                # assign a new elastic IP address
                self.ec2.allocate_address().associate(instance.id)

    return instances