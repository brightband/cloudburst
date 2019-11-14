"""
Baseclass for service
"""

from cloudburst.parser.types import HEURISTICS_ATTR

class ServiceMeta(type):
    """
    Metaclass to handle the registries of the service class.

    Registries under management:
      - Heuristic function registry
      - Opcode registry
    """
    registry = []

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ServiceMeta.registry.append(clsobj)
        return clsobj


class Service(metaclass=ServiceMeta):
    def __init__(self):
        pass

    @classmethod
    def get_heuristic_fns(cls) -> list:
        """
        Fetch the heuristic functions registered for the given
        service during runtime.
        """
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []

    @property
    def resources(self):
        """
        Resources property that must exist for the service
        """
        pass

    def fetch_all(self):
        """
        Fetch all of the resources for the service
        """
        pass

    def resource_factory(self, resource_objs):
        """
        Factory for generating dynamic Resource objects
        """
        pass

