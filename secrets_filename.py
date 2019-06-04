#!/usr/bin/env python3

import argparse
import sys
import re

'''Parse the files in a github commit for potentially sensitive filenames, per rules 
defined at https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf'''

_FILE_NAME_REGEXES = {
    "p12": "\.p12$",
    "pfx": "\.pfx$",
    "pkcs12": "\.pkcs12$",
    "pem": "\.pem$",
    "rsa": "_rsa$",
    "dsa": "_dsa$",
    "ed25519": "_ed25519$",
    "ecdsa": "_ecdsa$",
    "bash/zsh rc file": "^\.?(bash|zsh)?rc$",
    "bash/zsh profile": "^\.?(bash|zsh)_profile$",
    "bash/zsh aliases file": "^\.?(bash|zsh)_aliases$",
    "credential(s) file": "^\.credential(s)?$",
    "Github Enterprise file": "^\.githubenterprise$",
    "Apple Keychain file": "^\.*keychain$",
    "Keystore/Keyring file": "^key(store|ring)$"
    }


def detect_match_against_filename(files_to_check):
    '''checks argument against compiled regexes'''
    for rule, regex in _FILE_NAME_REGEXES.items():
        if re.search(regex, files_to_check):
            return regex

def main(argv=None):
    '''Parses filenames and provides outut.
    Note that if manually passed a directory as argument, checks are not recursive as Git 
    adds files to a commit individually.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Files to check')
    args = parser.parse_args(argv)
    exit_code = 0

    compiled_file_name_regexes = {}

    for regex in _FILE_NAME_REGEXES:
        try:
            compiled_file_name_regexes[regex] = re.compile(_FILE_NAME_REGEXES[regex])
        except:
            print("Rule:", regex, "failed to compile. This will not be tested against the file(s)\n")

    for filename in args.filenames:
        match = detect_match_against_filename(filename)
        if match:
            exit_code = 1
           # print('{} may contain sensitive information'.format(filename))
    return exit_code
    
if __name__ == '__main__':
    sys.exit(main())
