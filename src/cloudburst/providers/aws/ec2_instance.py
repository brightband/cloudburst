"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import AWSService, opcode
from cloudburst.utils.resource_factory import aws_factory 
from cloudburst.utils.errors import NoResourcesError
from cloudburst.utils.utils import aws_paginator

import boto3

class EC2Instance(AWSService):
    """
    Service object for an EC2 Instance
     
    Args:
        session (boto3.session): A boto3 session to use for fetching resources
    """
    def __init__(self, session):
        self._session = session
        self._resources = []
        self._client = None

    @opcode
    def TERMINATE(self, resource):
        """
        Terminate an EC2 instance, registered as an OPCODE
         
        Args:
            resource (Resource): The resource object to terminate
         
        Returns:
            N/A
         
        Raises:
            N/A
        """
        self.client.terminate_instances(
            InstanceIds=[
                resource.InstanceId
            ]
        )

    @property
    def resources(self):
        """
        The property for returning/modifying resources for an EC2
        instance
        """
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
        """
        Fetch all EC2 instances from boto3
         
        Args:
            N/A
         
        Returns:
            N/A (Objects generated in this function are exposed through the resources property)
         
        Raises:
            NoResourcesError: If no resources of the given type could be found
        """
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
        """
        Transform a list of resource dictionaries into resource objects and place them
        under the resources property
         
        Args:
            resource_objs (list): A list of resource objects to transform
         
        Returns:
            N/A
         
        Raises:
            N/A
        """
        for resource in resource_objs:
            r = aws_factory(type(self).__name__, resource)
            setattr(r, "__id__", r.InstanceId)
            self._resources.append(r)
