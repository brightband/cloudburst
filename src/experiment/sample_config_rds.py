from cloudburst.providers.aws import RDSInstance
from cloudburst.parser.types import Types


@Types(RDSInstance)
def test_stop_instance():
    if RDSInstance.DBInstanceStatus == "available":
        return RDSInstance.STOP_INSTANCE

