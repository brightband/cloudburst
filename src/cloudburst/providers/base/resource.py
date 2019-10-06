"""
Baseclass for Resource

This class is intended to transform returned information about a given Service's resources
into properties to homogenize the format cross-cloud
"""

from abc import ABC, abstractmethod
from cloudburst.parser.types import HEURISTICS_ATTR


class ResourceMeta(type):
    """
    Metaclass to register resource classes
    """
    registry = []

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ResourceMeta.registry.append(clsobj)
        return clsobj


class Resource(ABC, metaclass=ResourceMeta):
    def __init__(self):
        return

    # TODO @davis this is an ABC so sync up with colin on what the proper base class we will be using for these bois
    @classmethod
    def get_heuristic_fns(cls) -> list:
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []
