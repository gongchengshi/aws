from aws import USWest2

domain = USWest2.sdb().get_domain('mytable')

# items = domain.select("select * from `mytable` where `attr` > '2'")
items = domain.select("select * from `mytable` where `attr`='42'")

found = next(items)

if found:
    print found.name

# print items.next().name
