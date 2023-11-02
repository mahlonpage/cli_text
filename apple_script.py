from subprocess import Popen, PIPE

"""
Runs an apple script an handles opening and closing of application
script -- applescript to run
application -- application to open/close if necessary.
"""
def run_applescript_open_close(script, application):
     opened = open_application(application)

     info = run_applescript(script)

     if opened: close_application(application)

     return info

"""
Runs applescripts and handles errors
script -- apple script to run
"""
def run_applescript(script):
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
def open_application(application):
    open_script = f"""
    tell application "System Events"
        if not (exists process "{application}") then
            do shell script "open -g /System/Applications/{application}.app"
            delay 2
            return "opened"
        else
            return "already_open"
        end if
    end tell
    """
    result = run_applescript(open_script)
    result = result.strip()

    if result == "opened": return True
    else: return False

"""
Closes a given application on the device
application -- application to close.
"""
def close_application(application):
    close_script = f"""
    tell application "{application}" to quit
    """

    run_applescript(close_script)
    return

def send_user_message(contact, msg):
	send_user_script = f"""
		tell application "Messages"
			set targetService to 1st account whose service type = iMessage
			set targetCell to participant "{contact}" of targetService
			send "{msg}" to targetCell
		end tell
	"""

	return run_applescript(send_user_script)

def send_group_message(chat_name, msg):
	send_group_script = f"""
        tell application "Messages"
	        send "{msg}" to chat "{chat_name}"
        end tell
    """

	return run_applescript(send_group_script)