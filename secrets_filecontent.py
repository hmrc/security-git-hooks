#!/usr/bin/env python3

import argparse
import sys
import re

_FILE_CONTENT_REGEXES = {
    "aws_2": "(?:aws).{0,100}?(:|=|=>|->)\s*\"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])\"?",
    "cert_1": "-----(BEGIN|END).*?PRIVATE.*?-----",
    "application_secret": "application\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "play_crypto_secret": "play\.crypto\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "cookie_deviceId_secret": "cookie\.deviceId\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "sso_encryption_key": "sso\.encryption\.key\s*(=|:|->)\s*(?!(\s*ENC\[))"
}


for regex in _FILE_CONTENT_REGEXES:
    re.compile(_FILE_CONTENT_REGEXES[regex])


def handle_line_to_skip(line_to_skip):
    print("DEBUG - skipping", line_to_skip)
    line_to_skip is None



def detect_secret_in_line(line_to_check):
    """compiles regex and checks against line."""
    for rule, regex in _FILE_CONTENT_REGEXES.items():
        if re.search(re.compile(regex), line_to_check):
            return rule


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Files to check')
    args = parser.parse_args(argv)
    exit_code = 0
    
    for filename in args.filenames:
        with open(filename, 'r') as f:
            flag = False
            for i, line in enumerate(f):
                if re.search("exception phrase TBD", line):
                    flag = True
                    continue
                if flag:
                    flag = False
                    continue
                rule = detect_secret_in_line(line)
                if rule:
                    print("Potential sensitive string found on line {line_number} of {file}: {rule}".format(line_number=i+1, file=filename, rule=rule))
                    exit_code = 1
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
