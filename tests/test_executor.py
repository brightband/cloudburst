"""
Test the AWS Resource factory
"""

# Builtin imports
from unittest import TestCase
import json
import os

from cloudburst.utils.resource_factory import aws_factory

TEST_FILE = "test-fixtures/test_ec2.json"
TEST_SERVICE = "EC2"
MYPATH = os.path.dirname(os.path.abspath(__file__))


class TestExecutor(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass
