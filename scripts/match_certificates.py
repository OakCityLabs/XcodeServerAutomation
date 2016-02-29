#!/usr/bin/env python

#####################################
# Notes:
#####################################

import os
import shutil
from config import MATCH_GIT_URL, APPID, TEAMID, MATCH_PASSWORD
from common import envSetup, doGitOverSsh

def matchCertificates():
    env = {
        "MATCH_GIT_URL": MATCH_GIT_URL,
        "MATCH_APP_IDENTIFIER": APPID,
        "FASTLANE_TEAM_ID": TEAMID,
        "MATCH_VERBOSE": "1",
        "MATCH_PASSWORD": MATCH_PASSWORD,
    }
    cmd = "match run"
    doGitOverSsh(cmd, env)

def main():
    envSetup()
    matchCertificates()

if __name__ == "__main__":
    print "Download Profiles Script"
    exit(main())
