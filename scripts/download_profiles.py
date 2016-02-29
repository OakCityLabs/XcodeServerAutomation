#!/usr/bin/env python

#####################################
# Notes:
#
#  -- If this script says "No existing profiles" and
#     makes a new cert with a random number on the end,
#     then the server probably doesn't have the developer
#     profile (private keys) installed.
#####################################

import os
import shutil
from config import APPID
from common import envSetup, doCmd, get_provision_profile_dir, userProfilePath, infoForProfilePath

def downloadProfiles():
    dev = "Development"
    adhoc = "AdHoc"
    appstore = "AppStore"

    modes = [
        dev,
        adhoc,
        appstore,
    ]

    flags = "--skip_install -a %s download_all" % APPID

    cmds = {}
    cmds[dev] = "sigh --development %s" % flags
    cmds[adhoc] = "sigh --adhoc %s" % flags
    cmds[appstore] = "sigh %s" % flags

    try:
        # necessary on the server b/c _xcsbuildd user won't have this dir by default
        os.makedirs(userProfilePath)
    except OSError, e:
        print e

    for mode in modes:
        cmd = cmds[mode]
        profile = "%s_%s.mobileprovision" % (mode, APPID)
        print "Downloading profile: ", profile
#         print doCmd("echo $PATH")
#         print doCmd("which xcode-select")
        print doCmd(cmd)
        if not os.path.isfile(profile):
            msg = "ERROR! (%s) - Profile download failed for %s" % \
                (mode, profile)
            raise Exception(msg)
        try:
            (name, uuid) = infoForProfilePath(profile)
            print "Download info %s -- UUID: %s" % (name, uuid)
        except Exception, e:
            print "Error reading UUID:", e
        # Copy to active profile dir and the user profile dir (for xcodebuild).
        # Might be a duplicate copy, depending on config.
        print "Copy profile to:", get_provision_profile_dir()
        shutil.copy(profile, get_provision_profile_dir())
        print "Copy profile to:", userProfilePath
        shutil.copy(profile, userProfilePath)

def main():
    envSetup()
    downloadProfiles()

if __name__ == "__main__":
    print "Download Profiles Script"
    exit(main())
