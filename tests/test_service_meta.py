"""
Tests the metaprogramming hooks in Service
"""

# Builtin imports
from unittest import TestCase
import json
import os

from cloudburst.providers.base import Service, opcode
from cloudburst.providers.aws import EC2Instance

CODE_STR_REGISTER_SERVICES = """
from cloudburst.providers.base import Service
class ServiceA(Service): pass
class ServiceB(Service): pass
class NotAService: pass
"""

CODE_STR_DEFINE_HEURISTIC_FN = """
from cloudburst.providers.aws import EC2Instance
from cloudburst.parser.types import Types

@Types(EC2Instance)
def test_heuristic_fn():
    pass

@Types(EC2Instance)
def test_heuristic_fn_2():
    pass
"""

CODE_STR_TEST_OPCODE_REGISTRY = """
print('a')
from cloudburst.providers.base import Service, opcode
print('b')
class ServiceAA(Service):
    @opcode
    def opcode_1(self, resource): pass

    @opcode
    def opcode_2(self, resource): pass

class ServiceBB(Service): pass
"""

class TestServiceMeta(TestCase):
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
        
        me.get_heuristic_fns to get a list of heuristic fns and make sure ONLY the ones you
        registered are in there
        """
        self.assertTrue(EC2Instance.get_heuristic_fns() == [])
        exec(CODE_STR_DEFINE_HEURISTIC_FN)
        self.assertTrue(len(EC2Instance.get_heuristic_fns()) == 2)
        self.assertTrue(EC2Instance.get_heuristic_fns()[0].__name__ == 'test_heuristic_fn')
        self.assertTrue(EC2Instance.get_heuristic_fns()[1].__name__ == 'test_heuristic_fn_2')

    def test_opcode_registry(self):
        """
        Tests that the @opcode decorator correctly registers opcodes to the specific Service class
        """
        class ServiceAA(Service):
            @opcode
            def opcode_1(self, resource): pass

            @opcode
            def opcode_2(self, resource): pass

        class ServiceBB(Service): pass
        
        def has_opcode(service: Service, opcode_name: str) -> bool:
            for opcode_fun in service.ops_fns:
                if opcode_fun.__name__ == opcode_name:
                    return True
            return False
        
        self.assertTrue(len(ServiceAA.ops_fns) == 2)
        self.assertTrue(len(ServiceBB.ops_fns) == 0)
        self.assertTrue(has_opcode(ServiceAA, 'opcode_1'))
        self.assertTrue(has_opcode(ServiceAA, 'opcode_2'))

