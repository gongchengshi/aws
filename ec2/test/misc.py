from aws import USWest2 as AwsConnections


ec2 = AwsConnections.ec2()

# instances = ec2.get_only_instances()
instances = ec2.get_all_instance_status()
for instance in instances:
    print instance.tags['Name'], " is ", instance.state
