"""
Resource factories for different clouds
"""

import json
from collections import namedtuple
from cloudburst.utils.utils import datetime_handler

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
    # This may seem unintuitive, but what is happening here is that 
    # we are transforming the resource dictionary object into json to
    # leverage the object_hook function callback baked into the json
    # library. What this does is every time it encounters a dict while
    # decoding it returns the output of the provided function instead of
    # the decoded dictionary
    def dict_caster(d):
        def TERMINATE():
            pass
        d['TERMINATE'] = TERMINATE
        return namedtuple(resource_type, d.keys())(*d.values())

    json_obj = json.dumps(resource_obj, default=datetime_handler)
    return json.loads(json_obj, object_hook=dict_caster) 
