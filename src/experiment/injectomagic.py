from cloudburst.providers.aws import EC2Instance
from cloudburst.parser.types import Types


@Types(EC2Instance)
def check_ec2():
    print("Running check_ec2")
    print("and the instance id is... " + EC2Instance.instance_id)
    if EC2Instance.instance_id == "ami-04b762b4289fba92b":
        return EC2Instance.TERMINATE


class Stub:
    pass

stub = Stub()
stub.instance_id = "chonkyboi"

print(check_ec2.__globals__)
check_ec2.__globals__['EC2Instance'] = stub

check_ec2()

print("did i fuck it up long term tho? or is it scoped properly...")
print(dir(EC2Instance))

print("Name of instance stub: " + stub.__class__.__name__)


def my_super_sick_fn():
    pass

print("Name of func: " + my_super_sick_fn.__name__)