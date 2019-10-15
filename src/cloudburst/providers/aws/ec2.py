"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import Service, Resource

import boto3

class EC2(Service):
    def __init__(self, session):
        self._session = session
        self._resources = []
        self._client = None

    @property
    def resources(self):
        return self._resources

    @property
    def client(self):
        """
        Initialize a client from the session object if one does not
        already exist, otherwise return the existing client
        """
        if self._client is None:
            self._client = self._session.client('ec2')
        return self._client

    def fetch_all(self):
        self.client

    def resource_factory(self, resource_objs):
        
