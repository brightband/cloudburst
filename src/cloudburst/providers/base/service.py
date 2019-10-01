"""
Baseclass for service
"""

from abc import ABC, abstractmethod

class Service(ABC):
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

    @abstractmethod
    def __iter__(self):
        """
        Iterate over resources available in the service
        """
        pass
