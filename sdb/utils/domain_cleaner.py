from aws import USWest2 as AwsConnection

domain = AwsConnection.sdb().get_domain('speycastingforum01082015.crawled-urls')


query = "select * from `speycastingforum01082015.crawled-urls` where itemName() like 'poppysspeycastingforum.forumchitchat.com/post%'"

while True:
    items = domain.select(query, max_items=25)

    itemNames = {}

    for item in items:
        print 'deleting ' + item.name
        itemNames[item.name] = None  # create dictionary with only keys.

    if len(itemNames) == 0:
        break

    domain.batch_delete_attributes(itemNames)
