import datetime

def datetime_handler(dt):
    """
    Handle datetime conversion for non-standard datetime
    formats during the conversion of dicts <-> json through
    the json library
     
    Args:
        dt (datetime.datetime): Datetime object to be
                                converted
     
    Returns:
        dt (datetime.isoformat): Datetime converted to ISO
                                 format
     
    Raises:
        TypeError: If the provided datetime object is not
                   of a type that we know how to convert
    """
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()
    raise TypeError("Unknown type")

def aws_paginator(fn, *args, **kwargs):
    """
    Iterative paginator for AWS resources. Uses the
    common NextToken pagination scheme used in many
    AWS API calls. The first call is always made
    without specifying NextToken so this method will
    work even for resources not supporting the NextToken
    syntax.
     
    Args:
        fn (function):      A callable function to fetch
                            the resources
        *args (iterable):   The arguments to pass to the
                            fetching function
        **kwargs (dict):    The keyword arguments to pass
                            to the fetching function
     
    Returns:
        responses (list of dicts): The responses returned
                                   from the boto3 calls
     
    Raises:
        ValueError: The reserved kwarg 'NextToken' was
                    erroneously provided by the user
    """
    # Ensure the user is not specifying NextToken when calling
    # the paginator
    if 'NextToken' in kwargs:
        raise ValueError("Do not specify 'NextToken' in the **kwargs when calling the paginator")

    responses = []
    next_token = None
    while True:
        if next_token is not None:
            kwargs['NextToken'] = next_token

        resp = fn(*args, **kwargs)
        responses.append(resp)
        if 'NextToken' not in resp:
            break
        next_token = resp['NextToken']

    return responses
