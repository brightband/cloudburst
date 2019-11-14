"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import Service
from cloudburst.utils.resource_factory import aws_factory 
from cloudburst.utils.errors import NoResourcesError

import boto3


class EC2Instance(Service):
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
        Lazy-load our client object
        """
        if self._client is None:
            self._client = self._session.client('ec2')
        return self._client

    def fetch_all(self):
        resps = []
        next_token = ""
        while True:
            resp = self.client.describe_instances(NextToken=next_token)
            resps.append(resp)
            if 'NextToken' in resp:
                next_token = resp['NextToken']
            else:
                break

        # Iterate over all fetched response objects from EC2, if we have
        # a lot of resources we'll have multiple responses due to pagination
        for resp in resps:
            if (
                "Reservations" in resp
                and isinstance(resp["Reservations"], list)
                and len(resp["Reservations"]) > 0
            ):
                # Iterate over all the reservations in the response
                for reservation in resp["Reservations"]:
                    # Validate if there are any instances in the response
                    if (
                        "Instances" in reservation
                        and isinstance(reservation["Instances"], list)
                        and len(reservation["Instances"]) > 0
                    ):
                        self._resource_factory(reservation["Instances"])

        if len(self.resources) == 0:
            raise NoResourcesError("Could not find any resources of type {}".format(type(self).__name__))

    def _resource_factory(self, resource_objs):
        for resource in resource_objs:
            self._resources.append(aws_factory('ec2_instance', resource))


if __name__ == "__main__":
    sess = boto3.session.Session()
    e = EC2Instance(sess)
    e.fetch_all()
    print(e.resources)
