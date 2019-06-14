#!/usr/bin/env python3

import argparse
import sys
import re
from conf import _FILE_CONTENT_REGEXES

IGNORE_KEYWORD = "leak-detection-ignore"

for regex in _FILE_CONTENT_REGEXES:
    try:
        re.compile(_FILE_CONTENT_REGEXES[regex])
    except:
        raise


def detect_secret_in_line(line_to_check):
    """compiles regex and checks against line."""
    for rule, regex in _FILE_CONTENT_REGEXES.items():
        if re.search(re.compile(regex), line_to_check):
            return rule


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to check")
    args = parser.parse_args(argv)
    exit_code = 0

    for filename in args.filenames:
        with open(filename, "r") as f:
            flag = False
            for i, line in enumerate(f):
                if re.search(IGNORE_KEYWORD, line):
                    flag = True
                    continue
                if flag:
                    flag = False
                    continue
                rule = detect_secret_in_line(line)
                if rule:
                    print(
                        "Potentially sensitive string matching rule: {rule} found on line {line_number} of {file}".format(
                            rule=rule, line_number=i + 1, file=filename
                        )
                    )
                    exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
