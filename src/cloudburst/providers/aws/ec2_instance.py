"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import AWSService, opcode
from cloudburst.utils.resource_factory import aws_factory 
from cloudburst.utils.errors import NoResourcesError
from cloudburst.utils.utils import aws_paginator

import boto3

class EC2Instance(AWSService):
    @property
    def client(self):
        """
        Lazy-load our client object
        """
        if self._client is None:
            self._client = self._session.client('ec2')
        return self._client

    @opcode
    def TERMINATE(self, resource):
        self.client.terminate_instances(
            InstanceIds=[
                resource.InstanceId
            ]
        )


    def fetch_all(self):
        resps = aws_paginator(self.client.describe_instances)

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
            r = aws_factory(type(self).__name__, resource)
            setattr(r, "__id__", r.InstanceId)
            self._resources.append(r)

if __name__ == "__main__":
    sess = boto3.session.Session()
    e = EC2Instance(sess)
    e.fetch_all()
    print(e.resources)
