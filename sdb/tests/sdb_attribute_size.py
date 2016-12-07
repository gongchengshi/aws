from sdb.sdb_helpers import TruncateAttributeFromBeginning, TruncateAttributeFromEnd

truncated = TruncateAttributeFromBeginning(('x' * 1024) + 'y')
print len(truncated)
print truncated

truncated = TruncateAttributeFromEnd('y' + ('x' * 1024))
print len(truncated)
print truncated
