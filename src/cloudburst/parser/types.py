HEURISTICS_ATTR = "_heuristic_fns"


# placeholder
class TypeBase:
    @classmethod
    def _get_heuristic_fns(cls) -> list:
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []


# NOTE @davis -- we don't have to use these 'exact' classes below to register, the types, we could (and should?)
# also just use the classes in cb/provides/aws/...
# Im mostly just putting this here as a placeholder for now
class AWS:
    class EC2(TypeBase):
        pass

    class S3(TypeBase):
        pass


class GCP:
    class GCE(TypeBase):
        pass

    class GCS(TypeBase):
        pass


def Types(resource_type):
    """
    Decorator to register a user defined heuristic
    :param resource_type: A valid resource type class
    """
    # TODO @davis validate resource_type is one of the types above (ie AWS.EC2, AWS.S3, GCP.GCE, ect)
    def decorate(func):
        # TODO @davis validate func signature (should take no args with no return val)
        fns_list = getattr(resource_type, HEURISTICS_ATTR)
        fns_list.append(func)
    return decorate
