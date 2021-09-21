#!/usr/bin/env python3

import argparse
import re
import yaml

from . import conf

# import conf

"""Parse the files in a github commit for potentially sensitive filenames, per rules 
defined at https://github.com/hmrc/app-config-base/blob/HEAD/leak-detection.conf"""

patterns = yaml.safe_load(conf.CONF_YAML)["FILE_NAME_REGEXES"]


def detect_match_against_filename(files_to_check):
    """checks argument against compiled regexes"""
    for rule_name, rule in patterns.items():
        if re.search(rule["pattern"], files_to_check):
            return rule["pattern"]


def main(argv=None):
    """Parses filenames and provides outut.
    Note that if manually passed a directory as argument, checks are not recursive as Git
    adds files to a commit individually."""
    conf.validate_expressions("FILE_NAME_REGEXES")
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to check")
    args = parser.parse_args(argv)
    exit_code = 0
    for filename in args.filenames:
        match = detect_match_against_filename(filename)
        if match:
            exit_code = 1
            print(
                "{file} may contain sensitive information due to the file type".format(
                    file=filename
                )
            )
    return exit_code


if __name__ == "__main__":
    exit(main())
