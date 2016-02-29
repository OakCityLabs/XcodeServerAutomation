## Oak City Automation Scripts

### Main entry points

  * Xcode build steps (Run with every build)
    * `build_pre.py`	
      * Execute as a `Run Script` build phase before the `Compile Sources` build phase
    * `build_post.py` 
      * Excecute as a `Run Script` build phase as the last step
  *  Xcode Server Scripts
    * `bot_pre.py`
      * Run before the bot excecutes
    * `bot_post.py`
      * Run afte the bot executes    

### Manual scripts

  * `download_profiles.py`
    * Downloads provisioning profiles from the dev portal.  Will create profiles if they don't exist.  Might need to run this once on a dev machine to prime the profiles, if no profiles have been created in the dev portal yet.
  * `build_xcconfig.py`
    * Creates `Common.xcconfig` file.  May occasionally need to be run manually if things get out of whack.  Helps solve chicken and egg type problems. 

    
### Configuration Variables

  * `OCL_BUILD_NUMBER`
    * Monotonically increasing build number based on number of previous git repo check-ins.  Useful as build number of app.  Should match revision number tag that build server adds to the get repo.  Calculate on each build.
    * Example: `OCL_BUILD_NUMBER=17`
  * Provisioning Profiled Identifiers:
    * One for each of our build configurations: Debug, AdHoc, Release.  These should be set as the provisioning profile identifier for each configuration.  These are update from the dev portal with each build.
    * Examples:
      * `OCL_DEBUG_PROFILE_ID=37523f7f-2ff5-40f2-a15c-dc05897ab5d5`
      * `OCL_ADHOC_PROFILE_ID=682974e0-4ed3-435b-b277-9d31bdb410ce`
      * `OCL_RELEASE_PROFILE_ID=68a81377-48d9-4cbc-b50b-d81809426b2c`