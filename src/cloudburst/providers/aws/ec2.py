"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import Service

class EC2(Service):
    def __init__(self, session):
        self._session = session
        self._resources = []

    @property
    def resources(self):
        return self._resources

    def fetch_all(self):
        pass
