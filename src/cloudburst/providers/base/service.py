"""
Baseclass for service
"""

from cloudburst.parser.types import HEURISTICS_ATTR


OPS_ATTR = "_op_codes"


def opcode(func):
    setattr(func, OPS_ATTR, True)
    return func


class ServiceMeta(type):
    """
    Metaclass to handle the registries of the service class.

    Registries under management:
      - Heuristic function registry
      - Opcode registry
    """
    registry = []  # Note: registry is shared between all Service subclasses

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ServiceMeta.registry.append(clsobj)

        # Logic to handle registration of "op codes", ie functions which specify an operation on
        # a resource (ie TERMINATE)
        ServiceMeta._config_op_codes(clsobj)

        return clsobj

    @staticmethod
    def _config_op_codes(clsobj):
        # Create a new registry of operation function (ie TERMINATE) for each Service subclass
        clsobj.ops_fns = []
        
        for r in dir(clsobj):
            func = getattr(clsobj, r)
            if hasattr(func, OPS_ATTR):
                clsobj.ops_fns.append(func)


class Service(metaclass=ServiceMeta):
    def __init__(self):
        pass

    @classmethod
    def get_heuristic_fns(cls) -> list:
        """
        Fetch the heuristic functions registered for the given
        service during runtime.
        """
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []

    @property
    def resources(self):
        """
        Resources property that must exist for the service
        """
        raise NotImplementedError("Service object needs to implement a resources property")

    def fetch_all(self):
        """
        Fetch all of the resources for the service
        """
        raise NotImplementedError("Service object needs to implement fetch_all logic")

    def resource_factory(self, resource_objs):
        """
        Factory for generating dynamic Resource objects
        """
        raise NotImplementedError("Service object needs to implement a resource_factory")


class AWSService(Service):
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
        raise NotImplementedError("AWSService object needs to implement a client property")
