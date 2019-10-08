#!/usr/bin/env python3

import os

def repository_check():
    if os.path.exists('./repository.yaml') is True
        return 0
    else:
        print("No repository.yaml found")
        return 1

if __name__ == __main__:
    exit(repository_check())
    exit(repository_check())