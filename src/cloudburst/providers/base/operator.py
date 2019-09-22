"""
Baseclass for an operator

Reqs:
    1) __repr__ should return an easy-to-understand string about the operation for a --dryrun
    2) operations for all opcodes
    3) Linkage to resource reader
"""

class OPCODES(object):
    TERMINATE = None
    START = None
     

class Operator(object):
    def __init__(self, resource: cloudburst.base.Resource, opcode: OPCODE):
        return
