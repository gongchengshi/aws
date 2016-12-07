import bz2
import math
import time

SimpleDbMaxBatchSize = 25


def count(domain, where_cond=None):
    if not where_cond:
        return domain.connection.domain_metadata(domain).item_count

    query = "select count(*) from `%s` where %s" % (domain.name, where_cond)
    items = domain.select(query, max_items=1000000)
    sum = 0
    for item in items:
        sum += int(item['Count'])
    return sum


def create_domain(sdb, table_name):
    table = sdb.lookup(table_name)
    if table is None:
        table = sdb.create_domain(table_name)
        time.sleep(5)
        while sdb.lookup(table_name) is None:
            time.sleep(2)
    return table


def get_or_create_domain(sdb, table_name):
    return create_domain(sdb, table_name)


def batch_put_attributes(domain, items, replace=True):
    list_of_items = items.items()
    for i in range(0, len(list_of_items), SimpleDbMaxBatchSize):
        domain.batch_put_attributes(dict(list_of_items[i:i + SimpleDbMaxBatchSize]), replace)


def batch_delete_attributes(domain, items):
    list_of_items = items.items()
    for i in range(0, len(list_of_items), SimpleDbMaxBatchSize):
        domain.batch_delete_attributes(dict(list_of_items[i:i + SimpleDbMaxBatchSize]))


def item_exists(table, item_name, attr_name=None):
    # get_item() is faster than doing a select according to: https://forums.aws.amaxon.com/thread.jspa?messageID=144404
    # get_attributes() with a single attribute is faster than get_item() according to:
    #   http://www.daemonology.net/blog/2008-06-25-dissecting-simpledb-boxusage.html
    return bool(table.get_attributes(item_name, attribute_name=attr_name))


def truncate_attribute_from_beginning(value, max=1024):
    if value is None:
        return None

    length = len(value.encode('utf-8'))
    if length > max:
        overflow, overhead = _calculate_overflow(length, max)
        return '%s+...%s' % (overflow, value[overflow:])
    return value


def truncate_attribute_from_end(value, max=1024):
    if value is None:
        return None

    try:
        length = len(value.encode('utf-8'))
    except UnicodeDecodeError:
        length = len(value)
    if length > max:
        overflow, overhead = _calculate_overflow(length, max)
        return '%s...+%s' % (value[:max-overhead], overflow)
    return value


def _calculate_overflow(length, max):
    overflow = length - (max - 4)
    num_digits = int(math.log10(overflow))+1
    overflow += num_digits
    return overflow, num_digits + 4


def compress_if_larger_than_1024(value, compression_level):
    if value and len(value) > 1024:
        return bz2.compress(value, compression_level)
    return value


def select_one(domain, query):
    items = domain.select(query, max_items=1)
    found = None
    for item in items:
        found = item
        break
    return found
