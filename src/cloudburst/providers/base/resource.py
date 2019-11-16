"""
Baseclass for a resource
"""


class AWSResource:
    def __init__(self, nt):
        self.__name__ == type(nt).__name__
        for field in nt._fields:
            setattr(self, field, getattr(nt, field))
