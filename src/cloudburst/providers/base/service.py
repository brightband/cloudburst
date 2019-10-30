"""
Baseclass for service
"""

from abc import ABC, abstractmethod


class ServiceMeta(type):
    """
    Metaclass to register resource classes
    """
    registry = []

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ServiceMeta.registry.append(clsobj)
        return clsobj


class Service(ABC, metaclass=ServiceMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def resources(self):
        """
        Resources property that must exist for the service
        """
        pass

    @abstractmethod
    def fetch_all(self):
        """
        Fetch all of the resources for the service
        """
        pass
