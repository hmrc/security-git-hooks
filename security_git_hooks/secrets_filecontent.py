#!/usr/bin/env python3

import argparse
import re
import yaml
#from . import conf
import conf

RULES = {}

for key, value in yaml.safe_load(conf.CONF_YAML)["FILE_CONTENT_REGEXES"].items():
    RULES[value] = re.compile(value)
    RULES[key] = key

def main(argv=None):
    conf.validate_expressions("FILE_CONTENT_REGEXES")
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
                rule = RULES[value]
                if rule:
                    print(
                        "Potentially sensitive string matching rule: {rule} found at line {line_number} of {file}".format(
                            rule=RULES[key], line_number=i + 1, file=filename
                        )
                    )
                    exit_code = 1   
    return exit_code


if __name__ == "__main__":
    exit(main())

    
