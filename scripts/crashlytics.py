import os

from config import CRL_APIKEY, CRL_BUILDSECRET, CRL_EMAIL, CRL_SUBMIT
from common import doCmd, makeIpaAdHoc

def upload_crashlytics():    
    ipaPath = makeIpaAdHoc()
    
    cmdDict = {
        "submit": CRL_SUBMIT,
        "apiKey": CRL_APIKEY,
        "buildSecret": CRL_BUILDSECRET,
        "emails": CRL_EMAIL,
        "ipaPath": ipaPath,
    }
    cmd = "%(submit)s %(apiKey)s %(buildSecret)s -ipaPath %(ipaPath)s -emails %(emails)s" % cmdDict
    print doCmd(cmd)
