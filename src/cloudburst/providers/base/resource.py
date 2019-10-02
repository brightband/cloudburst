"""
Baseclass for Resource

This class is intended to transform returned information about a given Service's resources
into properties to homogenize the format cross-cloud
"""

from abc import ABC, abstractmethod

class Resource(ABC):
    def __init__(self):
        return
