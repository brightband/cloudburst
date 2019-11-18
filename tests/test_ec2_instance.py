import os
import json
from unittest import TestCase, mock

import boto3
import botocore

from cloudburst.providers.aws import EC2Instance
from cloudburst.utils.shared_vars import AWS_REGIONS

TEST_FILE = "test-fixtures/test_responses.json"
MYPATH = os.path.dirname(os.path.abspath(__file__))


class TestEC2Instance(TestCase):
    def setUp(self):
        sess = boto3.session.Session()
        self.service = EC2Instance(sess)

    def test_resources(self):
        assert self.service.resources == []

    def test_client(self):
        assert type(self.service.client()).__name__ == 'EC2'
        assert type(self.service.client('us-west-2')).__name__ == 'EC2'

    def test_supported_regions(self):
        assert self.service.supported_regions == AWS_REGIONS

    @mock.patch('cloudburst.providers.aws.ec2_instance.aws_paginator')
    def test_fetch_all(self, paginator_mock):
        with open(os.path.join(MYPATH, TEST_FILE), 'r') as tf:
            paginator_mock.return_value = json.loads(tf.read())

        self.service.fetch_all()
        assert isinstance(self.service.resources, list)
        # Test if region field is appropriately applied
        getattr(self.service.resources[0], "Region")
