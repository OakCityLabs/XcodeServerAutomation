import os

from common import doCmd, makeIpaAppStore

def upload_testflight():    
    ipaPath = makeIpaAppStore()
    
    cmdDict = {
        "ipaPath": ipaPath,
    }
    
    cmd = "pilot upload --ipa %(ipaPath)s" % cmdDict
    doCmd(cmd)
