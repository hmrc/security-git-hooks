#!/usr/bin/env python3
import time

start = time.time()
import argparse
import re
import yaml
#from . import conf
import conf

RULES = {}

for key, value in yaml.safe_load(conf.CONF_YAML)["FILE_CONTENT_REGEXES"].items():
    RULES[value] = key


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
                for regex, rule in RULES.items():
                    if re.search(regex, line):
                        print(
                            "Potentially sensitive string matching rule: {rule} found at line {line_number} of {file}".format(
                                rule=rule, line_number=i + 1, file=filename
                            
                            )
                        )
                exit_code = 1
    end = time.time()
    print(end - start)
    return exit_code

if __name__ == "__main__":
    exit(main())
