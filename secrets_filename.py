#!/usr/bin/env python3

import argparse
import sys
import re

file_name_regexes = {
    "aws_2 ": "(?:aws).{0,100}?(:|=|=>|->)\s*\"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])\"?",
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
    "ed25519": "_ed25519$",
    "ecdsa": "_ecdsa$",
    "jks": "\.jks$",
    "bash/zsh rc file": "^\.?(bash|zsh)?rc$",
    "bash/zsh profile": "^\.?(bash|zsh)_profile$",
    "bash/zsh aliases file": "^\.?(bash|zsh)_aliases$",
    "credential(s) file": "^\.credential(s)?$",
    "Github Enterprise file": "^\.githubenterprise$",
    "Apple Keychain file": "^\.*keychain$",
    "Keystore/Keyring file": "^key(store|ring)$"
    }


compiled_file_name_regexes = {}

for regex in file_name_regexes:
    try:
        compiled_file_name_regexes[regex] = re.compile(file_name_regexes[regex])
    except:
        print("Rule:", regex, "failed to compile. This will not be tested against the file(s)\n")


def detect_match_against_filename(files_to_check):
    '''checks argument against compiled regexes'''
    for regex in compiled_file_name_regexes:
        if re.search(compiled_file_name_regexes[regex], files_to_check):
            return regex


def main(argv=None):
    '''Parses filenames and provides outut.
    Note that if manually passed a directory as argument, checks are not recursive as Git 
    adds files to a commit individually.''' 
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Files to check')
    args = parser.parse_args(argv)
    exit_code = 0

    for filename in args.filenames:
        rule = detect_match_against_filename(filename)
        if rule:
            exit_code = 1
            print('{} may contain sensitive information'.format(filename))
    return exit_code
    
if __name__ == '__main__':
    sys.exit(main())
