import argparse
from subprocess import Popen, PIPE

from alias_manager import add_alias, add_group_alias, print_aliases, get_send_goal
from contact_manager import generate_contacts

def call_applescript(script):
	p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	stdout, stderr = p.communicate(script)
	return {"output": stdout, "error": stderr, "code": p.returncode}

def send_message_to_user(contact, msg):
	send_to_user_script = f"""
		tell application "Messages"
			set targetService to 1st account whose service type = iMessage
			set targetCell to participant "{contact}" of targetService
			send "{msg}" to targetCell
		end tell
	"""

	return call_applescript(send_to_user_script)

def send_message_to_group(chat_name, msg):
	send_to_group_script = f"""
        tell application "Messages"
	        send "{msg}" to chat "{chat_name}"
        end tell
    """

	return call_applescript(send_to_group_script)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--alias", nargs=2, metavar=('name, alias'), help="Adds a person from contacts to aliases. Takes a name, alias pair. Name is used to search contacts and alias is used to text.")
	parser.add_argument("--alias_group", nargs=2, metavar=('group_name, alias'), help="Adds a person from contacts to aliases. Takes a name, alias pair. Name is used to search contacts and alias is used to text.")

	parser.add_argument("--list", action="store_true", help="List all aliases")
	parser.add_argument("--update_contacts", action="store_true", help="Updates contacts file by pulling from mac. If true is passed after, delete previous contacts instead of adding to.")
	parser.add_argument("recipient", nargs="?", help="Alias of person to send text to")
	parser.add_argument("message", nargs=argparse.REMAINDER, help="Message to send to recipient")

	args = parser.parse_args()

	if args.alias:
		add_alias(*args.alias)
		exit(0)

	if args.alias_group:
		add_group_alias(*args.alias_group)
		exit(0)

	if args.list:
		print_aliases()
		exit(0)

	if args.update_contacts:
		generate_contacts()
		exit(0)



	if args.recipient and args.message:
		send_goal = get_send_goal(args.recipient)

		if send_goal:
			# Either send to group ot send to individual user
			if args.recipient[0] == ".":
				resp = send_message_to_group(send_goal, " ".join(args.message))
			else:
				resp = send_message_to_user(send_goal, " ".join(args.message))

			# Error case
			if resp['code'] != 0:
				print(f"Failed to send message, error code: {resp['code']}")

		else:
			print(f"Alias {args.recipient} could not be found. Run --alias to add an alias. Group aliases start with .")


# TODO:
# make it so you can't add duplicate aliases.
# Make a way to delete aliases.
# Get group chat names from most recent texts, filter out individual's names and then store groups

# separate group aliasing and regular aliasing