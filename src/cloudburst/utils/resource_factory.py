"""
Resource factories for different clouds
"""

import json
from collections import namedtuple

from cloudburst.providers.base import AWSResource

class AWS(object):
    """
    Factory for AWS resources
     
    Args:
        resource_type (str):    The name of the resource object we are
                                generating
    """

    def __init__(self, resource_type):
        self._name = resource_type

    def generate(self, resource_obj): 
        """
        Generate a Resource object from the provided representation
        of that object.
         
        Args:
            resource_obj (dict):    In the case of AWS resource objects
                                    will be dictionaries returned from
                                    the Boto3 SDK
         
        Returns:
            resource (Resource):    Returns the resource after being
                                    transformed into an internal resource
         
        Raises:
            SyntaxError:            If the provided object syntax is not able
                                    to be derived by our generator
        """
        # This may seem unintuitive, but what is happening here is that 
        # we are transforming the resource dictionary object into json to
        # leverage the object_hook function callback baked into the json
        # library. What this does is every time it encounters a dict while
        # decoding it returns the output of the provided function instead of
        # the decoded dictionary
        def dict_caster(d):
            return namedtuple(self._name, d.keys())(*d.values())

        json_obj = json.dumps(resource_obj)
        return json.loads(json_obj, object_hook=dict_caster) 
