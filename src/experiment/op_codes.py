from cloudburst.parser.types import HEURISTICS_ATTR

OPS_ATTR = "_op_codes"


def register_op(op_name: str):
    def decorate(func):
        setattr(func, OPS_ATTR, op_name)
        return func

    return decorate


class ResourceMeta(type):
    """
    Metaclass to create a registry of generated resources
    """
    registry = []

    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        ResourceMeta._config_op_codes(clsobj)
        return clsobj

    @staticmethod
    def _config_op_codes(clsobj):
        for r in dir(clsobj):
            func = getattr(clsobj, r)

            if hasattr(func, OPS_ATTR):
                op_name = getattr(func, OPS_ATTR)
                setattr(clsobj, op_name, func)


# class Resource(ABC, metaclass=ResourceMeta):
# ^ this is producing error:
#  "TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases"
# I need to investigate wtf this means @davis
# ...Removing ABC for now as a proof of concept of the register_op decorator

class Resource(metaclass=ResourceMeta):
    def __init__(self):
        return

    @classmethod
    def get_heuristic_fns(cls) -> list:
        if hasattr(cls, HEURISTICS_ATTR):
            return getattr(cls, HEURISTICS_ATTR)
        return []


class AWSResource(metaclass=ResourceMeta):
    def __init__(self, nt):
        self.__name__ == type(nt).__name__
        for field in nt._fields:
            setattr(self, field, getattr(nt, field))


"""
RATCHET INLINE TEST 
TODO @davis MOVE THIS TO A PROPER TEST DIR 

run this file to see it in action. Obviously Pumpkin does not have a user defined method "boo", but we can attach it 
at interpret time 
"""
class Pumpkin(Resource):

    @register_op("BOO")
    def spooky_func(self):
        print("oOOooOOo scary")

p = Pumpkin()
p.BOO()
