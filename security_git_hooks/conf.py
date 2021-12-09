import pkg_resources
import yaml
import re

CONF_YAML = pkg_resources.resource_string(__name__, "conf.yaml")

IGNORE_KEYWORD = "LDS ignore"


def validate_expressions(ITEM):
    for rule in yaml.safe_load(CONF_YAML)[ITEM].values():
        re.compile(rule["pattern"])
