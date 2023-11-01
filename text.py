import argparse
from subprocess import Popen, PIPE

from alias_manager import add_alias, print_aliases, get_phone_number
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--alias", nargs=2, metavar=('name, alias'), help="Adds a person from contacts to aliases. Takes a name, alias pair. Name is used to search contacts and alias is used to text.")
	parser.add_argument("--list", action="store_true", help="List all aliases")
	parser.add_argument("--update_contacts", nargs="?", help="Updates contacts file by pulling from mac. If true is passed after, delete previous contacts instead of adding to.")
	parser.add_argument("recipient", nargs="?", help="Alias of person to send text to")
	parser.add_argument("message", nargs=argparse.REMAINDER, help="Message to send to recipient")

	args = parser.parse_args()

	if args.alias:
		add_alias(*args.alias)
		exit(0)

	if args.list:
		print_aliases()
		exit(0)

	if args.update_contacts:
		contact_args = args.update_contacts
		if len(contact_args) == 2 and contact_args[2].strip().lower() == "true":
			generate_contacts(True)
		generate_contacts(False)



	if args.recipient and args.message:
		phone_number = get_phone_number(args.recipient)
		if phone_number:
			resp = send_message_to_user(
				phone_number, " ".join(args.message)
			)
			if resp['code'] != 0:
				print(f"Failed to send message, error code: {resp['code']}")

		else:
			print(f"Alias {args.recipient} could not be found. Run --alias to add an alias.")


# TODO:
# make it so you can't add duplicate aliases. Make a way to delete aliases.