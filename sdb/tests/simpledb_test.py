from aws import USWest2 as aws
from aws.sdb import item_exists

sdb = aws.sdb()

mytable = sdb.lookup('mytable')

# mytable.put_attributes('2', {'attr': None})
# mytable.put_attributes('3', {'attr': ''})
#
# attr = mytable.get_attributes('2')
# attr = mytable.get_attributes('3')

mytable.put_attributes('11', {'attr': None})

items = mytable.select("select * from `mytable`") #where `redirectsTo`='None' and itemName() like '%/' and `{1}` is null )

for item in items:
    i = 9

i = 9
