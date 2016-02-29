import os
import re
import sys
import glob
import subprocess
import plistlib
import platform
import tempfile
from config import APPID, BUILDSERVER, DEVBRANCH, PRODBRANCH, SSHKEY, USER, \
    PASSWORD, GIT_REMOTE, PROJECTNAME, TEAMID, XCCONFIG

serverProfilePath = "/Library/Developer/XcodeServer/ProvisioningProfiles"
userProfilePath = os.path.expanduser("~/Library/MobileDevice/Provisioning Profiles")

#################################
# Utility
#################################
def envSetup():
    os.environ["DELIVER_USER"] = USER
    os.environ["DELIVER_PASSWORD"] = PASSWORD
    os.environ["FASTLANE_DISABLE_COLORS"] = "1"

    # Add /usr/loca/bin where fastlane, etc live
    path = os.environ["PATH"] 
    os.environ["PATH"] = "%s:/usr/local/bin" % path
    
def deColorize(theStr):
    return theStr
#     return re.sub(u'\u001b\[.*?[@-~]', '', theStr)
    
def doCmd(cmd, extraEnv=None):
    print "Executing cmd:", cmd
    e = None
    if extraEnv:
        print "Adding env variables:", extraEnv
        e = os.environ
        e.update(extraEnv)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=e)
        output, err = proc.communicate()
    except subprocess.CalledProcessError, e:
        print "Error output:", deColorize(e.output)
        raise(e)
    if err != "":
        print "Standard Out:", deColorize(output)
        print "Standard Error:", deColorize(err)
    txt = output.strip()
    return deColorize(txt)

def sshKeyPath():
    cwd = os.path.abspath(os.curdir)
    path = os.path.join(cwd, SSHKEY)
    return path
    
# def doGitOverSsh(cmd, env={}):
#     #prefix = 'env GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -i %s" ' % os.path.join(getKeyRoot(), sshKey)
#     keyPath = sshKeyPath()
#     print doCmd("chmod 400 %s" % keyPath)
#     env["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -i %s" % keyPath 
#     print doCmd(cmd, env)

def doGitOverSsh(cmd, env={}):
    keyPath = sshKeyPath()
    print doCmd("chmod 400 %s" % keyPath)
    # start an agent and grep out the important bits
    out = doCmd("ssh-agent -s |grep SSH |awk -F \; '{print $1}'")
    print out
    for line in out.split("\n"):
        if not line.startswith("SSH_"):
            continue
        fields = line.split("=")
        env[fields[0]] = fields[1]
    print doCmd("ssh-add %s" % keyPath, env)
    print doCmd(cmd, env)
    print doCmd("kill $SSH_AGENT_PID", env)


#################################
# Git stuff
#################################
def isDevBranch():
    return DEVBRANCH == gitBranchName()
    
def isProdBranch():
    return PRODBRANCH == gitBranchName()
    
def gitBranchName():
    cmd = "git rev-parse --abbrev-ref HEAD"
    return doCmd(cmd)

def getBuildNum():
    # get the time stamp of the current commit
    currentTimestamp = doCmd("git show -s --format=%at")
    # count the number of commits across all branches dated earlier than the current commit 
    buildNum = doCmd("git rev-list --all --count --until %s" % currentTimestamp)
    return buildNum
    
def tagRevision():
    buildNum = getBuildNum()
    revTag = "rev%s" % buildNum
    print "Revision Tag:", revTag
    currentTags = doCmd('git tag').strip().split('\n')
    # Build server should be the authoritative tagger.
    # Anybody else gets nuked from orbit.
    if platform.node() == BUILDSERVER: 
        if revTag in currentTags:
            print "Found existing tag >%s<, deleting..." % revTag
            doCmd("git tag -d %s" % revTag)
        doCmd("git tag %s" % revTag)
        doGitOverSsh("git push %s --tags" % GIT_REMOTE)
    else:
        print "Skipping tagging %s -- I'm not the build server."
    
#################################
# Xcode Server stuff
#################################
def buildIsGood():
    # This will throw an exception if XCS_INTEGRATION_RESULT is not in the environment, 
    #   so it should only be called in the context of a post-build trigger script
    return "succeeded" == os.environ['XCS_INTEGRATION_RESULT']

def getSrcRoot(): 
    plist = os.environ["PRODUCT_SETTINGS_PATH"]     # Info.plist is usually in the source directory
    (sourcePath, dummy) = os.path.split(plist)
    return sourcePath
    
    
#################################
# Packaging Profile stuff
#################################

def makeIpaAdHoc():
    # This will throw an exception if XCS_INTEGRATION_TINY_ID, XCS_ARCHIVE is not in the environment, 
    #   so it should only be called in the context of a post-build trigger script
    xcsID = os.environ["XCS_INTEGRATION_TINY_ID"]
    ipaName = "%s.%s.ipa" % (PROJECTNAME, xcsID)
    ipaPath = "/tmp/%s" % ipaName
    archivePath = os.environ["XCS_ARCHIVE"]
        
    # "exportPath" here is a file name
    cmd = '''xcodebuild -exportArchive -archivePath "%s" -exportFormat ipa -exportPath %s''' % \
            (archivePath, ipaPath)
    doCmd(cmd)
        
    return ipaPath

def makeIpaAppStore():
    # This will throw an exception if XCS_INTEGRATION_TINY_ID, XCS_ARCHIVE is not in the environment, 
    #   so it should only be called in the context of a post-build trigger script
    xcsID = os.environ["XCS_INTEGRATION_TINY_ID"]
    ipaDir = "/tmp/%s.%s" % (PROJECTNAME, xcsID)
    archivePath = os.environ["XCS_ARCHIVE"]
    
    # tmp copy for debugging -- can be deleted once fixed
    cmd = """cp -r "%s" /tmp/""" % archivePath
    doCmd(cmd)
    # end tmp copy
    
    plistFileHandle = tempfile.NamedTemporaryFile('w', suffix="plist", delete=False)
    plistPath = plistFileHandle.name
    
    cwd = os.path.abspath(os.curdir)
    plistTemplatePath = os.path.join(cwd, "exportOptions.plist.template")
    f = open(plistTemplatePath, 'r')
    plistData = f.read()
    f.close()
    
    plistDict = {}
    plistDict["TEAMID"] = TEAMID
    plistFinal = plistData % plistDict
    print "######### Export Options Plist #########"
    print plistFinal
    print "########################################"
    plistFileHandle.write(plistFinal)
    plistFileHandle.close()
    
    # "exportPath" here is an output directory
    cmd = '''xcodebuild -exportArchive -archivePath "%s" -exportOptionsPlist %s -exportPath %s''' % \
            (archivePath, plistPath, ipaDir)
    doCmd(cmd)
    
    os.unlink(plistPath)
    
    ipaPath = None
    for p in glob.glob("%s/*.ipa" % ipaDir):
        # quote it b/c of spaces in name
        ipaPath = '''"%s"''' % p     # should just be one 
        
    return ipaPath
    
#################################
# Provisioning Profile stuff
#################################

def get_provision_profile_dir():
    if os.path.isdir(serverProfilePath):
        return serverProfilePath
    return userProfilePath
    
def find_uuid(profType):
    ppdir = get_provision_profile_dir()
    name = "%s %s" % (APPID, profType)
    uuid = None
    pattern = os.path.join(ppdir,"*.mobileprovision")
    for pp in glob.glob(pattern):
        tmpUuid = uuidForName(pp, name) 
        if tmpUuid:
            uuid = tmpUuid
    return uuid
    
def infoForProfilePath(profilePath):
    cmd = 'security cms -D -i "%s"' % profilePath
    plistData = doCmd(cmd) 
    plist = plistlib.readPlistFromString(plistData)
    name = plist["Name"]
    uuid = plist["UUID"]
    return (name, uuid)
    
def uuidForName(profilePath, profileName):
#     cmd = 'security cms -D -i "%s"' % profilePath
#     plistData = doCmd(cmd) 
#     plist = plistlib.readPlistFromString(plistData)
#     name = plist["Name"]
#     uuid = plist["UUID"]
    name, uuid = infoForProfilePath(profilePath)
        
    if profileName == name:
        return uuid
    else:
        return None
    
def find_uuid_development():
    return find_uuid("Development")

def find_uuid_adhoc():
    return find_uuid("AdHoc")

def find_uuid_appstore():
    return find_uuid("AppStore")

#################################
# xcConfig Stuff
#################################
def oclBuildNum():
    return "OCL_BUILD_NUMBER=%s" % getBuildNum()
    
def oclDebugUuid():
    return "OCL_DEBUG_PROFILE_ID=%s" % find_uuid_development()
    
def oclAdHocUuid():
    return "OCL_ADHOC_PROFILE_ID=%s" % find_uuid_adhoc()
    
def oclAppStoreUuid():
    return "OCL_RELEASE_PROFILE_ID=%s" % find_uuid_appstore()
    
def writeLine(handle, line):
    handle.write(line)
    handle.write('\n')
    
def buildXcConfig():
    f = open(XCCONFIG, 'w')
    writeLine(f, oclBuildNum())
    writeLine(f, oclDebugUuid())
    writeLine(f, oclAdHocUuid())
    writeLine(f, oclAppStoreUuid())
    f.write('\n')
    f.close()
    f = open(XCCONFIG, 'r')
    d = f.read()
    f.close()
    print "Wrote XCCONFIG file:\n", d