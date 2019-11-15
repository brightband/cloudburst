"""
S3 Resource(s) for AWS provider
"""

import boto3
import json

from cloudburst.providers.base import AWSService
from cloudburst.utils.resource_factory import aws_factory
from cloudburst.utils.errors import NoResourcesError
from cloudburst.utils.utils import aws_paginator, datetime_handler

class S3Bucket(AWSService):
    @property
    def client(self):
        if self._client is None:
            self._client = self._session.client('s3')
        return self._client

    def fetch_all(self):
        resps = aws_paginator(self.client.list_buckets)
        print(json.dumps(resps, indent=2, default=datetime_handler))

if __name__ == "__main__":
    sess = boto3.Session()

    s3b = S3Bucket(sess)
    s3b.fetch_all()
