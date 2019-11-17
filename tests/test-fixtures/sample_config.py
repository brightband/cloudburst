from cloudburst.providers.aws import EC2Instance
from cloudburst.parser.types import Types


@Types(EC2Instance)
def check_ec2():
    if EC2Instance.InstanceId == "i-0deb12bbb82cd61aa":
        return EC2Instance.TERMINATE

