from subprocess import Popen, PIPE

"""
Runs an apple script, opening the necessary applications and returning
them to their initial opened/closed state
script -- apple script to run
application -- application used by this script
close -- if the application needs to be opened, should we close it afterward?
"""
def run_apple_script(script, application):
    opened = _open_application(application)

    print("enter normal script")
    info = _applescript_runner(script)

    if opened: _close_application(application)

    return info

"""
Runs applescripts and handles errors
script -- apple script to run
"""
def _applescript_runner(script):
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    info, err = p.communicate(script)
    if err:
        print(f"Applescript error: {err}")
        exit(1)
    return info

"""
Opens a given application on the device and returns a bool denoting if it was already open or not.
application -- the application to open.
"""
def _open_application(application):
    print("enter open app")
    open_script = f"""
    tell application "System Events"
        if not (exists process "{application}") then
            tell application "{application}" to activate
            delay 2
            return "opened"
        else
            return "already_open"
        end if
    end tell
    """
    result = _applescript_runner(open_script)
    result = result.strip()

    if result == "opened": return True
    else: return False

"""
Closes a given application on the device
application -- application to close.
"""
def _close_application(application):
    print("enter close app")
    close_script = f"""
    tell application "{application}" to quit
    """

    _applescript_runner(close_script)
    return
