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
import os, sys
from cloudburst.providers.base.service import Service
CONFIG_NAME = "sample_config.py"

CURR_PATH = os.path.realpath(__file__)
CURR_PATH = "/".join(CURR_PATH.split('/')[:-1])
CONFIG_PATH = CURR_PATH + "/" + CONFIG_NAME


def load_config_str(path) -> str:
    f = open(path, "r")
    return f.read()


def get_registered_services() -> list:
    return list(filter(lambda service: len(service.get_heuristic_fns()) > 0, Service.registry))




if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     raise Exception("Executor must be passed the absolute directory of config file")
    code_str = load_config_str(CONFIG_PATH)
    exec(code_str)
    print("chill 1")
    print("chill 2")
