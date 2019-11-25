#!/usr/bin/env python3
import argparse
import re
import yaml

from . import conf

# import conf

PRIVATE_RULES = yaml.safe_load(conf.CONF_YAML)["PRIVATE_RULES"]

PUBLIC_RULES = yaml.safe_load(conf.CONF_YAML)["PUBLIC_RULES"]


def repository_yaml_check():
    for filename in args.filenames:
        if filename == "repository.yaml":
            with open(filename, "r") as repo:
                for line in repo:
                    if re.search(CONF.REPOSITORY_YAML_CONTENT[public]):
                        return PRIVATE_RULES, PUBLIC_RULES
                    elif re.search(CONF.REPOSITORY_YAML_CONTENT[private]):
                        return PRIVATE_RULES
                    else:
                        print(
                            "No repository,yaml file found, checking against all rules"
                        )
                        return PRIVATE_RULES, PUBLIC_RULES


def detect_secret_in_line(line_to_check, filename):
    """compiles regex and checks against line."""
    rules = repository_yaml_check()

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
    conf.validate_expressions("FILE_CONTENT_RULES")
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
                        "Potentially sensitive string matching rule: {rule} found on line {line_number} of {file}".format(
                            rule=rule, line_number=i + 1, file=filename
                        )
                    )
                    exit_code = 1
    return exit_code


if __name__ == "__main__":
    exit(main())
