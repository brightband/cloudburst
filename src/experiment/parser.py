"""
 Parse python file at given path, extract a list of all resource it touched
 record function pointers to all heuristics

 need mapping of resources -> [fn1 fn2, fn3] ....

 Then we bootstrap by building session
 loading resource for each resource (fetch_all)

 We then call fn pointer for each resource, get the returned FN pointer
 If not None, we pass that resource into the FN

 profit
"""
import os
import sys
import boto3

from cloudburst.providers.base.service import Service
from typing import Callable, Union, List


CONFIG_NAME = "sample_config.py"

CURR_PATH = os.path.realpath(__file__)
CURR_PATH = "/".join(CURR_PATH.split('/')[:-1])
CONFIG_PATH = CURR_PATH + "/" + CONFIG_NAME


class Recorder:
    """
    Recorder is a global data structure used to record operations on instances
    """
    # TODO group resources by services (make resource_operation_map a nested dict)
    resource_operation_map = {}


def load_config_str(path) -> str:
    # TODO validate path exists; return error if not found
    f = open(path, "r")
    return f.read()


def get_registered_services() -> list:
    """
    This function will return a list of Service classes that were referenced in the user's config file. It assumes that
    the config file has been interpreted and loaded into this global namespace
    :return: A list of Service classes
    """
    return list(filter(lambda service: len(service.get_heuristic_fns()) > 0, Service.registry))


def bootstrap_services(service_classes: list) -> (list, boto3.session):
    """
    This function creates the Service instances for each service class supplied in service_classes. They will all share
    a boto3 session, which is returned along side the list of loaded Service instances.
    :param service_classes:
    :return: A tuple of 2, containing (list of Service instances, boto3 session)
    """
    sess = boto3.session.Session()
    services = [service_class(sess) for service_class in service_classes]
    for service in services:
        service.fetch_all()

    return services, sess


def execute_heuristic_fns(service_instances: list):
    """
    This function goes through each resource in each service, and applies any user defined heuristic functions on it.
    If the heuristic function returns non-None, (ie EC2Service.Terminate), then this return value is treated as an
    op code and is executed on the resource
    :param service_instances: A list of Service instances
    :return: None
    """
    for service in service_instances:
        fns = service.get_heuristic_fns()
        for resource in service.resources:
            for fn in fns:
                execute_heuristic(fn, service, service.__class__, resource)


def execute_heuristic(heuristic_fn, service, service_class, resource):
    """
    Behold -- feast your eyes upon this top shelf black magic, courtesy of the masterclass Python wizards of Brightband.

    This function first injects a resource object into the scope of a heuristic fn, so that "ServiceClass.some_property"
    inside a heuristic fn will actually reference "resource.some_property" (where resource is the object passed into
    this function). Afterwards, the injection is reverse such that the global namespace is not altered.

    For example, consider the user defined heuristic:
    -------------------------------------------------------
    @Types(EC2Instance)
    def check_ec2():
        if EC2Instance.instance_id == "...":
            return EC2Instance.TERMINATE
    -------------------------------------------------------
    When this heuristic is invoked, we inject an actual resource to replace the "EC2Instance" class reference inside
    the user's heuristic, such that EC2Instance is essentially replaced with the "resource" arg supplied into this
    function.

    The return value of the heuristic is then captured, and if it is non-None (meaning it is a function pointer to an
    operation such as EC2Service.TERMINATE), this operation is executed and recorded.

    :param heuristic_fn: A function pointer to the user's defined heuristic
    :param service_class: A Service subclass (ie EC2Instance)
    :param resource: A resource object (ie the output of a resource factory)
    :return: None
    """
    service_name = service_class.__name__
    previous_ref = heuristic_fn.__globals__[service_name]

    heuristic_fn.__globals__[service_name] = resource  # Inject the resource
    return_val = heuristic_fn()  # Execute the heuristic and capture the return value
    heuristic_fn.__globals__[service_name] = previous_ref  # Inverse the injection

    if return_val is not None:
        # TODO implement dry-run here, and defer executing the operation if it is set
        #Recorder.resource_operation_map[resource] = return_val.__name__
        real_fn = getattr(service_class, return_val.__name__)
        print("the val of the real fn is: " + return_val.__name__)
        real_fn(service, resource)
        #return_val(resource)  # Execute the operation


if __name__ == "__main__":
    # TODO implement CLI args
    # if len(sys.argv) != 2:
    #     raise Exception("Executor must be passed the absolute directory of config file")
    code_str = load_config_str(CONFIG_PATH)

    # Exec'ing the config file will cause the code to be run by the interpreted, and loaded into this global namespace
    # This will cause all of the decorators in the heuristic functions to bind themselves to their associated Service
    # classes, which are then accessible via Service.get_heuristic_fns
    exec(code_str)

    # Bootstrap, which involves
    # 1) Creating a boto3 session
    # 2) Instantiating the service objects referenced in the user's config
    # 3) Fetch all resources for each of these instantiated service objects
    services, session = bootstrap_services(get_registered_services())

    # Now, we that setup is complete, we get to work and start actually executing the heuristic functions
    execute_heuristic_fns(services)

    # TODO cleanup? Close session or something?
    print(Recorder.resource_operation_map)

