"""
Import the service classes from all of the service files. This is to simplify
import statements for the end user

Instead of:
    from cloudburst.providers.aws.ec2 import EC2

you get:
    from cloudburst.providers.aws import EC2

This has the added benefit of allowing the providers to be specified in their own
files for clarity in the filesystem tree
"""

from .ec2 import EC2
