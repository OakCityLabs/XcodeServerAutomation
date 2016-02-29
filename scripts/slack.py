#!/usr/bin/env python

import os
import requests
import json
from common import getBuildNum, gitBranchName, buildIsGood
from config import SLACK_HOOK

"""
Sample environment passed to script after integration

XCS=1
XCS_ANALYZER_WARNING_CHANGE=0
XCS_ANALYZER_WARNING_COUNT=0
XCS_BOT_ID=710e92380c223f0cc4553eb09c02142f
XCS_BOT_NAME=Noteables Bot
XCS_BOT_TINY_ID=4BA7AF5
XCS_ERROR_CHANGE=0
XCS_ERROR_COUNT=0
XCS_INTEGRATION_ID=e6087498151a723b692c579232115bb9
XCS_INTEGRATION_NUMBER=14
XCS_INTEGRATION_RESULT=succeeded
XCS_INTEGRATION_TINY_ID=64E9825
XCS_OUTPUT_DIR=/Library/Developer/XcodeServer/Integrations/Integration-e6087498151a723b692c579232115bb9
XCS_SOURCE_DIR=/Library/Developer/XcodeServer/Integrations/Caches/710e92380c223f0cc4553eb09c02142f/Source
XCS_TESTS_CHANGE=0
XCS_TESTS_COUNT=11
XCS_TEST_FAILURE_CHANGE=0
XCS_TEST_FAILURE_COUNT=0
XCS_WARNING_CHANGE=0
XCS_WARNING_COUNT=0
XCS_XCODEBUILD_LOG=/Library/Developer/XcodeServer/Integrations/Integration-e6087498151a723b692c579232115bb9/build.log
"""

def bot2slack():
    e = os.environ

    botname = e['XCS_BOT_NAME']
    status = e['XCS_INTEGRATION_RESULT']
    bot_build_number = e['XCS_INTEGRATION_NUMBER']
    version_number = getBuildNum()

    theKeys = [ 'e', 'w', 'a', 't']

    names = {
        'e' : "Error",
        'w' : "Warning",
        't' : "Test Failure",
        'a' : "Analyzer Warning",
    }

    error = {
        'e' : int(e['XCS_ERROR_COUNT']),
        'w' : int(e['XCS_WARNING_COUNT']),
        't' : int(e['XCS_TEST_FAILURE_COUNT']),
        'a' : int(e['XCS_ANALYZER_WARNING_COUNT']),
    }

    change = {
        'e' : int(e['XCS_ERROR_CHANGE']),
        'w' : int(e['XCS_WARNING_CHANGE']),
        't' : int(e['XCS_TEST_FAILURE_CHANGE']),
        'a' : int(e['XCS_ANALYZER_WARNING_CHANGE']),
    }

    test_count = int(e['XCS_TESTS_COUNT'])
    test_fail = error['t']
    test_pass = test_count - test_fail

    msg = "Hello.  Bot Build %s (git rev%s) finished and %s." % (bot_build_number, version_number, status)
    msg += "\n  Building on branch '%s'." % gitBranchName()
    msg += "\n  Passed %s of %s tests." % (test_pass, test_count)

    if error['e'] == error['w'] == error['a'] == error['t'] == 0 and buildIsGood() :
        msg += "\n  Light is green, trap is clean.  No problems detected."
    else:
        for k in theKeys:
            if error[k] == 0: continue
            msg += "\n  Found %s problems in %s, a change of %s." % (error[k], names[k], change[k])
    
    print msg 

    good_icon = ":bot:"
    bad_icon = ":no_entry_sign:"

    if buildIsGood():
      icon = good_icon
    else:
      icon = bad_icon

    payload={
        "username": botname,
        "icon_emoji": icon,
        "text": msg
        }

    post_response = requests.post(url=SLACK_HOOK, data=json.dumps(payload))
    print "Post response:", post_response.text

def main():
    bot2slack()
 
if __name__ == "__main__":
    exit(main())