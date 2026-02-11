import importlib.resources
import yaml
import re

with importlib.resources.files(__package__).joinpath("conf.yaml").open("r") as f:
    CONF_YAML = f.read()

IGNORE_KEYWORD = "LDS ignore"


def validate_expressions(ITEM):
    for rule in yaml.safe_load(CONF_YAML)[ITEM].values():
        re.compile(rule["pattern"])
