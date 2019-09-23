import AWS.EC2 as EC2

WHITELIST = [
    "i-372982961",
    "i-189231298"
]

@Types(EC2)
def check_ec2_whitelist():
    if EC2.TTL > 30 and EC2.ID not in WHITELIST:
        return EC2.TERMINATE

@Types(EC2)
def check_ec2_production():
    if EC2.TTL > 30 and "Prod" not in EC2.Tags:
        return EC2.TERMINATE
        
