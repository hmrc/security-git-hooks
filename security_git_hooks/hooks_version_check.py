#!/usr/bin/env python3

import requests
import yaml
import sys


"""This hook checks the security-git-hooks release contained in .pre-commit-config.yaml against
 the latest release from https://github.com/hmrc/security-git-hooks. It is an information only
 hook, and will always pass as to prevent the interruption of workflow, however it will produce
 output to advise when a new release is available"""


def check_release_version_from_config(pre_commit_config_yaml):
    """checks the pre-commit-config.yaml in the current directory and returns the release tag detailed there"""
    try:
        with open(pre_commit_config_yaml, "r") as file:
            config = yaml.safe_load(file)
            res = filter(lambda x: "security-git-hooks" in x["repo"], config["repos"])
            return next(res)["rev"]
    except Exception:
        raise Exception("Local checks failed")


def check_release_version_from_remote_repo():
    """checks the GitHub API and returns the latest release tag detailed there"""
    try:
        req = requests.get(
            "https://api.github.com/repos/hmrc/security-git-hooks/releases/latest"
        )
        content = req.json()
        return content["tag_name"]
    except Exception:
        raise Exception("Remote checks failed")


def main():
    try:
        config_version = check_release_version_from_config(".pre-commit-config.yaml")
        latest_release = check_release_version_from_remote_repo()
        if config_version == latest_release:
            print("All HMRC hooks are up to date")
        else:
            print(
                "Your security-git-hooks version is {yours} and latest is {latest}."
                ' Please run the following command in this directory: "pre-commit autoupdate"'.format(
                    yours=config_version, latest=latest_release
                )
            )

    except Exception as e:
        print(
            "Checking for updates against HMRC hooks failed ({error}). Run 'pre-commit autoupdate' in this directory \
            as a precaution".format(
                error=e
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
