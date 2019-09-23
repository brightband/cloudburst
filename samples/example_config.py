import AWS.EC2 as EC2
import AWS.S3 as S3
import CB.Types as Types

# how to whitelist/blacklist nodes????
# Whitelist can be done by specifying a literal whitelist in this file and 
# using it in the heuristic

class OPS:

@Types(EC2)
# or Types.EC2 
def check_ec2():
    if EC2.EBS.Available_Memeory> 10 and EC2.Network_Usage > 1000:
        return EC2.TERMINATE
    
@Types(S3)
def check_s3():
    ... 

