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


class TestAWSResourceFactory(TestCase):
    def setUp(self):
        with open(os.path.join(MYPATH, TEST_FILE), "r") as tf:
            self._test_object = json.load(tf)

    def test_generate(self):
        t = aws_factory('ec2', self._test_object)

        # We do not need to check the exhaustive set of fields from
        # test-fixtures, but we should check if nested and non-nested
        # types are valid
        assert(t.Monitoring.State == 'disabled')
        assert(t.VpcId == 'vpc-3f990858')
        assert(t.NetworkInterfaces[0].Status == "in-use")
        assert(t.NetworkInterfaces[0].PrivateIpAddresses[0].Association.PublicIp == "54.191.5.109")
