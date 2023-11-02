from apple_script import run_apple_script, run_apple_script_batch

"""
Runs a script to send a text message to an individual
contact -- phone number to send to
msg -- message to send
"""
def send_user_message(contact, msg):
	send_user_script = f"""
		tell application "Messages"
			set targetService to 1st account whose service type = iMessage
			set targetCell to participant "{contact}" of targetService
			send "{msg}" to targetCell
		end tell
	"""

	return run_apple_script(send_user_script, "Messages")

"""
Runs a script to send a text message to a group chat
contact -- group chat full name
msg -- message to send
"""
def send_group_message(chat_name, msg):
	send_group_script = f"""
        tell application "Messages"
	        send "{msg}" to chat "{chat_name}"
        end tell
    """

	return run_apple_script(send_group_script, "Messages")

"""
Same as send_user_message but repeats
repeat_count -- number of times to send message.
"""
def send_repeat_user_message(contact, msg, repeat_count):
    send_user_script = f"""
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetCell to participant "{contact}" of targetService
            send "{msg}" to targetCell
        end tell
    """

    scripts = [send_user_script for _ in range(repeat_count)]

    return run_apple_script_batch(scripts, "Messages")

"""
Same as send_group_message but repeats
repeat_count -- number of times to send message.
"""
def send_repeat_group_message(chat_name, msg, repeat_count):
    send_group_script = f"""
        tell application "Messages"
            send "{msg}" to chat "{chat_name}"
        end tell
    """

    scripts = [send_group_script for _ in range(repeat_count)]

    return run_apple_script_batch(scripts, "Messages")
