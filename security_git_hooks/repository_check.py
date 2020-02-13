#!/usr/bin/env python3

import os


def repository_check():
    if os.path.exists("./repository.yaml") is True:
        return 0
    else:
        print("No repository.yaml found")
        return 1


def main():
    repository_check()


if __name__ == "__main__":
    exit(main())
