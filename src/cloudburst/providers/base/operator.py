"""
Baseclass for an operator

Reqs:
    1) __repr__ should return an easy-to-understand string about the operation for a --dryrun
    2) operations for all opcodes
    3) Linkage to resource reader

Note: This may not be necessary as it could logically be part of the Resource. Need to consider
      whether or not to represent this as its own object. May be easier to understand/extend
      this library if it is. Currently under consideration
"""

class OPCODES(object):
    TERMINATE = None
    START = None
     

class Operator(object):
    def __init__(self):
        return
