import os
import pkg_resources
import yaml 
import re

CONF_YAML = pkg_resources.resource_string(__name__, "conf.yaml")

IGNORE_KEYWORD = "pre-commit-ignore"


def validate_expressions(MEOW):
    for regex in yaml.safe_load(CONF_YAML)[MEOW].values():
        try:
            re.compile(regex)
        except re.error:
            print("{rule} failed to compile and has not been tested against the staged files".format(rule=rule))
