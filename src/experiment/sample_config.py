from cloudburst.providers.aws import EC2Instance
from cloudburst.parser.types import Types


@Types(EC2Instance)
def check_ec2():
    if EC2Instance.instance_id == "ami-04b762b4289fba92b":
        return EC2Instance.TERMINATE

