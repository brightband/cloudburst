# from cloudburst.providers.base.service import Service


HEURISTICS_ATTR = "_heuristic_fns"


# placeholder
class TypeBase:
    @classmethod
    def _get_heuristic_fns(cls) -> list:
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []


# Should we rename this Heuristic??? --davis
def Types(service_type):
    """
    Decorator to register a user defined heuristic
    :param service_type: A valid resource type class
    """
    # TODO @davis validate resource_type is one of the types above (ie AWS.EC2, AWS.S3, GCP.GCE, ect)
    def decorate(func):
        # if not issubclass(service_type, Service):
        #     raise TypeError("Argument 'service_type' must be a Service subclass (i.e. EC2, S3, GCE, ect)")
        # TODO @davis validate func signature (should take no args with no return val)

        if not hasattr(service_type, HEURISTICS_ATTR):
            setattr(service_type, HEURISTICS_ATTR, [])
        fns_list = getattr(service_type, HEURISTICS_ATTR)
        fns_list.append(func)

        return func

    return decorate
