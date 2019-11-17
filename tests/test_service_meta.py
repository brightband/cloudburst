"""
Tests the metaprogramming hooks in Service
"""

# Builtin imports
from unittest import TestCase
import json
import os

from cloudburst.providers.base import Service


CODE_STR_REGISTER_SERVICES = """
from cloudburst.providers.base import Service
class ServiceA(Service): pass
class ServiceB(Service): pass
class NotAService: pass
"""


class TestServiceMeta(TestCase):
    def setUp(self):
        pass

    def test_service_registry(self):
        """
        Tests that subclassing Service correctly adds the new subclass to Service.registry
        """
        def check_service_registered(service_name: str) -> bool:
            for serv in Service.registry:
                if serv.__name__ == service_name:
                    return True
            return False

        self.assertFalse(check_service_registered("ServiceA"))
        self.assertFalse(check_service_registered("ServiceB"))
        exec(CODE_STR_REGISTER_SERVICES)
        self.assertTrue(check_service_registered("ServiceA"))
        self.assertTrue(check_service_registered("ServiceB"))
        self.assertFalse(check_service_registered("NotAService"))

    def test_types_decorator(self):
        """
        Tests that the @Types(Type) decorator correctly registers the function to the Service
        
        Use ServiceName.get_heuristic_fns to get a list of heuristic fns and make sure ONLY the ones you
        registered are in there
        """
        pass


