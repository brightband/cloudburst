import os
import json
from unittest import TestCase, mock

import boto3
import botocore

from cloudburst.providers.aws import EC2Instance

TEST_FILE = "test-fixtures/test_responses.json"
MYPATH = os.path.dirname(os.path.abspath(__file__))


class TestEC2Instance(TestCase):
    def setUp(self):
        sess = boto3.session.Session()
        self.resource = EC2Instance(sess)

    def test_resources(self):
        assert self.resource.resources == []

    def test_client(self):
        assert type(self.resource.client).__name__ == 'EC2'

    @mock.patch('cloudburst.providers.aws.ec2_instance.aws_paginator')
    def test_fetch_all(self, paginator_mock):
        with open(os.path.join(MYPATH, TEST_FILE), 'r') as tf:
            paginator_mock.return_value = json.loads(tf.read())

        self.resource.fetch_all()
        assert isinstance(self.resource.resources, list)
