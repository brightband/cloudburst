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

    def _fetch_buckets(self):
        resps = aws_paginator(self.client.list_buckets)

        buckets = []
        for resp in resps:
            if (
                'Buckets' in resp
                and isinstance(resp['Buckets'], list)
                and len(resp['Buckets']) > 0
            ):
                # Append all of the buckets together so we can take
                # action on them
                buckets += resp['Buckets']

        return buckets

    def _fetch_bucket_objects(self, bucket):
        # Make subsequent API calls to construct our S3 object
        contents = []
        resps = aws_paginator(
            self.client.list_objects_v2,
            Bucket=bucket
            FetchOwner=True
        )
        for resp in resps:
            if (
                'Contents' in resp
                and isinstance(resp['Contents'], list)
                and len(resp['Contents']) > 0
            ):
            contents += resp['Contents']

        return contents

    def _fetch_bucket_accelerate_configuration(self, bucket):
        resp = self.client.get_bucket_accelerate_configuration(Bucket=bucket)
        return resp

    def _fetch_bucket_acl(self, bucket):
        resp = self.client.get_bucket_acl(Bucket=bucket)
        return resp

    def _fetch_bucket_analytics_configuration(self, bucket):
        resp = self.client.get_bucket_analytics_configuration(Bucket=bucket)
        return resp

    def _fetch_bucket_cors(self, bucket):
        resp = self.client.get_bucket_cors(Bucket=bucket)
        return resp

    def _fetch_bucket_encryption(self, bucket):
        resp = self.client.get_bucket_encryption(Bucket=bucket)
        return resp

    def fetch_all(self):
        buckets = self._fetch_buckets()

        # Get our lower-level objects for a given bucket
        for bucket in buckets:
            bucket_obj = {}
            bucket_obj.update(bucket)
            bucket_obj['Contents'] = self._fetch_bucket_contents(bucket)
            bucket_obj['AccelerateConfiguration'] = \
                    self._fetch_bucket_accelerate_configuration(bucket)
            bucket_obj['ACL'] = self._fetch_bucket_acl(bucket)
            bucket_obj['AnalyticsConfiguration'] = \
                    self._fetch_bucket_analytics_configuration(bucket)
            bucket_obj['CORS'] = self._fetch_bucket_cors(bucket)
            

if __name__ == "__main__":
    sess = boto3.Session()

    s3b = S3Bucket(sess)
    s3b.fetch_all()
