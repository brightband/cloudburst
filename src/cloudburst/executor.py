from .providers.base.resource import Resource
from .parser.types import HEURISTICS_ATTR

def execute():
    for resource in Resource.registry:
        # TODO @davis create resource (or 'service'?) instance
        service = object()

        # run that dude, passing in his heuristcs
        heuristics = resource.get_heuristic_fns()
        if heuristics:
            service.run(heuristics)
