"""
Resource factories for different clouds
"""

import json
from collections import namedtuple
from cloudburst.utils.utils import datetime_handler

class Resource():
    def __getattr__(self, attr):
        if attr not in dir(self):
            # TODO: Record this somewhere so the user knows they tried to
            #       access a field that doesnt exist
            return Resource()

def aws_factory(resource_type, resource_obj): 
    """
    Generate a Resource object from the provided representation
    of that object.
     
    Args:
        resource_type (str):    The name of the resource object we are
                                generating
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
    if type(resource_obj) not in (list, dict):
        return resource_obj

    new_obj = type('', (Resource,object), {})() if type(resource_obj) is dict else []

    for element in resource_obj:
        if type(resource_obj) is dict:
            setattr(new_obj, element, aws_factory(resource_type, resource_obj[element]))
        else:
            new_obj.append(aws_factory(resource_type, element))

    return new_obj
