#!/usr/bin/env python3

import requests
import json
import yaml
import sys


def check_release_version_from_config():
    try:
        with open(".pre-commit-config.yaml", "r") as file:
            config = yaml.safe_load(file)
            res = filter(lambda x: "mobile-token-proxy" in x["repo"], config["repos"])
            return next(res)["rev"]
    except:
        raise Exception("Local checks failed.")


def check_release_version_from_remote_repo():
    try:
        req = requests.get(
            "https://api.github.com/repos/hmrc/mobile-token-proxy/releases/latest"
        )
        content = req.json()
        return content["tag_name"]
    except:
        raise Exception("Remote checks failed.")


def main():
    try:
        config_version = check_release_version_from_config()
        latest_release = check_release_version_from_remote_repo()
        if config_version == latest_release:
            print("All hooks from HMRC are currently up to date")
        else:
            print(
                "Your security-git-hooks version is {yours} and the latest version is {latest}."
                ' Please run the following command in this repo: "pre-commit autoupdate"'.format(
                    yours=config_version, latest=latest_release
                )
            )

    except Exception:
        print(
            "Checking automatically for updates failed. Check manually or run 'pre-commit autoupdate' as a precaution"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
