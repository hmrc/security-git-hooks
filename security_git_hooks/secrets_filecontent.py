#!/usr/bin/env python3
import argparse
import re
import yaml

from . import conf

# import conf

PRIVATE_RULES = yaml.safe_load(conf.CONF_YAML)["PRIVATE_RULES"]

PUBLIC_RULES = yaml.safe_load(conf.CONF_YAML)["PUBLIC_RULES"]


def repository_yaml_check(repository_yaml):
    """Apply appropriate ruleset per repoVisibility in repository.yaml file"""
    """
    - load repository.yaml (open, read, parse)
    - access value of repoVisibility
    - return rulesets according to value

    """
    try:
        with open(repository_yaml, "r") as file:
            yamlfile = yaml.safe_load(file)
            if (
                yamlfile["repoVisibility"]
                == "public_0C3F0CE3E6E6448FAD341E7BFA50FCD333E06A20CFF05FCACE61154DDBBADF71"
            ):
                return PUBLIC_RULES
            elif (
                yamlfile["repoVisibility"]
                == "private_12E5349CFB8BBA30AF464C24760B70343C0EAE9E9BD99156345DD0852C2E0F6F"
            ):
                return PRIVATE_RULES
    except FileNotFoundError:
        print("no repository.yaml data found, searching against all rules")
        return PUBLIC_RULES


repository_yaml_check("repository.yaml")


def detect_secret_in_line(line_to_check, filename):
    """compiles regex and checks against line."""
    rules = repository_yaml_check("repository.yaml")

    rules_to_check = {
        rule_name: rule
        for rule_name, rule in rules.items()
        if not is_rule_excluded(filename, rule)
    }

    for rule_name, rule in rules_to_check.items():
        if re.search(rule["pattern"], line_to_check):
            return rule_name


def is_rule_excluded(filename, rule):
    for exclusion in rule["exclusions"]:
        if re.search(exclusion, filename):
            return True


def main(argv=None):
    conf.validate_expressions("PRIVATE_RULES")
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to check")
    args = parser.parse_args(argv)
    exit_code = 0

    for filename in args.filenames:
        with open(filename, "r") as f:
            flag = False
            for i, line in enumerate(f):
                if re.search(conf.IGNORE_KEYWORD, line):
                    flag = True
                    continue
                if flag:
                    flag = False
                    continue
                rule = detect_secret_in_line(line, filename)
                if rule:
                    print(
                        "Potentially sensitive string matching rule: {rule} "
                        "found on line {line_number} of {file}".format(
                            rule=rule, line_number=i + 1, file=filename
                        )
                    )
                    exit_code = 1
    return exit_code


if __name__ == "__main__":
    exit(main())
