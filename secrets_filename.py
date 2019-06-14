#!/usr/bin/env python3

import argparse
import sys
import re
from conf import _FILE_NAME_REGEXES

"""Parse the files in a github commit for potentially sensitive filenames, per rules 
defined at https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf"""


for regex in _FILE_NAME_REGEXES:
    try:
        re.compile(_FILE_NAME_REGEXES[regex])
    except:
        raise


def detect_match_against_filename(files_to_check):
    """checks argument against compiled regexes"""
    for rule, regex in _FILE_NAME_REGEXES.items():
        if re.search(regex, files_to_check):
            return regex


def main(argv=None):
    """Parses filenames and provides outut.
    Note that if manually passed a directory as argument, checks are not recursive as Git 
    adds files to a commit individually."""
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
    sys.exit(main())
