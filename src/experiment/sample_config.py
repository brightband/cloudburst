from cloudburst.providers.aws import EC2Instance
from cloudburst.parser.types import Types


@Types(EC2Instance)
def check_ec2():
    if EC2Instance.InstanceId == "i-0e3f41b57129a2744":
        return EC2Instance.TERMINATE

