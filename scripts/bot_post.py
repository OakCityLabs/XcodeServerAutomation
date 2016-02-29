#!/usr/bin/env python

# 
# This script runs after continuous integration builds, not developer builds.
#
# Should be run in the current directory, like so
#
# cd $XCS_SOURCE_DIR/<projectname>/scripts/
# ./bot_post.py

print "Xcode Bot Post-Integration Script"

import os
from crashlytics import upload_crashlytics
from testflight import upload_testflight
from slack import bot2slack
from common import isDevBranch, isProdBranch, envSetup, buildIsGood

envSetup()

try:
    if buildIsGood():
        print "Build is good!"
        # always upload to crashlytics, so it can symbol map production crashes
        upload_crashlytics()
        if isProdBranch():
            upload_testflight()
    else:
        print "Build failed."
except Exception, e:
    print "Exception:", e
    os.environ["XCS_INTEGRATION_RESULT"] = "bot_post-failure"

bot2slack()
