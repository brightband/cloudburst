"""
EC2 Resource for AWS provider
"""

from cloudburst.providers.base import AWSService, opcode
from cloudburst.utils.resource_factory import aws_factory 
from cloudburst.utils.errors import NoResourcesError
from cloudburst.utils.utils import aws_paginator
from cloudburst.utils.shared_vars import AWS_REGIONS

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
        self._client_map = {}

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
    def supported_regions(self):
        """
        A property for defining the supported regions for a service. For EC2,
        all regions are supported
         
        Returns:
            aws_regions (dict of regions): Return the dictionary of supported regions
                                           formatted as 'region identifier': 'human readable
                                           name'. To be used while fetching and modifying
                                           resources.
        """
        return AWS_REGIONS


    @property
    def resources(self):
        """
        The property for returning/modifying resources for an EC2
        instance

        Returns:
            resources (list of Resource): A list of resource objects for the service
        """
        return self._resources

    def client(self, region=None):
        """
        Return a client for the given region name, implemented this way to lazy-load clients
        for each region to keep memory management intuitive
         
        Args:
            region (string): The name of the region (region unique identifier e.g. 'us-west-2'). If
                             None is provided, the default client will be fetched (region will be
                             whatever is specified in credentials config)
         
        Returns:
            ec2client (boto3.client): The client to be used to make calls for a given region/service
        """
        # Check if the specified region name is in the client map, add if not exists
        if region not in self._client_map.keys():
            self._client_map[region] = None

        # Check if the client map contains the client for a given region
        if self._client_map[region] == None:
            self._client_map[region] = self._session.client('ec2', region_name=region)

        return self._client_map[region]

    def _fetch_for_region(self, region):
        """
        Return a list of instance dictionaries for processing 
        """
        resps = aws_paginator(self.client(region).describe_instances)

        # Iterate over all fetched response objects from EC2, if we have
        # a lot of resources we'll have multiple responses due to pagination
        instances = []
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
                        instances += reservation["Instances"]
        return instances


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
        all_instances = []
        for region in self.supported_regions:
            regional_instances = self._fetch_for_region(region)
            for instance in regional_instances:
                instance["Region"] = region
                self._resource_factory(instance)

        if len(self.resources) == 0:
            raise NoResourcesError("Could not find any resources of type {}".format(type(self).__name__))

    def _resource_factory(self, resource):
        """
        Transform a resource dictionary into a resource object and place it under the resources
        property
         
        Args:
            resource_objs (dict): A resource object to transform and add to the resources property
         
        Returns:
            N/A
         
        Raises:
            N/A
        """
        r = aws_factory(type(self).__name__, resource)
        setattr(r, "__id__", r.InstanceId)
        self._resources.append(r)
