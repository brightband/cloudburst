"""
Baseclass for a resource
"""

import typing

class ResourceMeta(type):
    """
    Metaclass to create a registry of generated resources
    """
    registry = []

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ResourceMeta.registry.append(clsobj)
        return clsobj

class AWSResource(metaclass=ResourceMeta):
    def __init__(self, nt):
        self.__name__ == type(nt).__name__
        for field in nt._fields:
            setattr(self, field, getattr(nt, field))
