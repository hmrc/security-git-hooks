#!/usr/bin/env python3

import argparse
import sys
import re

file_content_regexes = {
    "aws_2": "(?:aws).{0,100}?(:|=|=>|->)\s*\"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])\"?",
    "cert_1": "-----(BEGIN|END).*?PRIVATE.*?-----",
    "application_secret": "application\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "play_crypto_secret": "play\.crypto\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "cookie_deviceId_secret": "cookie\.deviceId\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "sso_encryption_key": "sso\.encryption\.key\s*(=|:|->)\s*(?!(\s*ENC\[))"
}

file_name_regexes = {
    "p12": "\.p12$",
    "pfx": "\.pfx$",
    "pkcs12": "\.pkcs12$",
    "pem": "\.pem$",
    "rsa": "_rsa$",
    "dsa": "_dsa$",
    "_ed25519": "_ed25519$",
    "_ecdsa": "_ecdsa$",
    "bash/zsh rc file": "^\.?(bash|zsh)?rc$",
    "bash/zsh profile": "^\.?(bash|zsh)_profile$",
    "bash/zsh aliases file": "^\.?(bash|zsh)_aliases$",
    "credential(s) file": "^\.credential(s)?$",
    "Github Enterprise file": "^\.githubenterprise$",
    "Apple Keychain file": "^\.*keychain$ ",
    "Keystore/Keyring file": "^key(store|ring)$"
    }

compiled_file_content_regexes = {}

for regex in file_content_regexes:
    try:
        compiled_file_content_regexes[regex] = re.compile(file_content_regexes[regex])
    except:
        print("Rule:", regex, "failed to compile. This will not be tested against the file(s)\n")


def detect_secret_in_line(line_to_check):
    for regex in compiled_file_content_regexes:
        if re.search(compiled_file_content_regexes[regex], line_to_check):
            return regex


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Files to check')
    args = parser.parse_args(argv)
    exit_code = 0

    for filename in args.filenames:
        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f):
                    rule = detect_secret_in_line(line)
                    if rule:
                        print('Found on line {line_number} of {file}: {rule}'.format(line_number= i+1, file= filename, rule=rule))
                        exit_code = 1
        except:
            print("File: ", filename, " encountered an error and was not tested")
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
