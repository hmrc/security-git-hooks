import os
import pkg_resources
import yaml
import re

CONF_YAML = pkg_resources.resource_string(__name__, "conf.yaml")

IGNORE_KEYWORD = "LDS ignore"


def validate_expressions(ITEM):
    for rule in yaml.safe_load(CONF_YAML)[ITEM].values():
        try:
            re.compile(rule["pattern"])
        except re.error:
            print(
                "{rule} failed to compile and has not been tested against the staged files".format(
                    rule=rule
                )
            )
