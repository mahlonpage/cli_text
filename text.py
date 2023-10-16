import argparse
import os

from subprocess import Popen, PIPE

ALIAS_FILE = os.path.join(os.path.dirname(__file__), "aliases.txt")

def call_applescript(script):
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    return {"output": stdout, "error": stderr, "code": p.returncode}

def send_message_to_user(contact, msg):
    send_to_user = f"""
        tell application "Messages"
	        set targetService to 1st account whose service type = iMessage
	        set targetCell to participant "{contact}" of targetService
	        send "{msg}" to targetCell
        end tell
    """

    return call_applescript(send_to_user)

def parse_aliases():
	if not os.path.isfile(ALIAS_FILE): 
		with open(ALIAS_FILE, 'w+') as af: pass
	with open(os.path.join(os.path.dirname(__file__), "aliases.txt"), 'r+') as af:
		return {
			alias.split("|")[0].strip(): alias.split("|")[1].strip() 
			for alias in af.readlines()
		}

def add_alias(name, number):
	active = parse_aliases()
	alias = name.lower().strip()
	active[alias] = number

	with open(ALIAS_FILE, 'w+') as af:
		for k, v in sorted(active.items()):
			af.write(f"{k}|{v}\n")

	print(f"Added alias: {alias}|{number}!")

if __name__ == "__main__":
	parser = argparse.ArgumentParser() 
	
	parser.add_argument("recipient", nargs="?", help="Alias to send text")
	parser.add_argument("--alias", nargs=2, metavar=('name', 'number'), help="Alias k-v pair to add")
	parser.add_argument("--list", action="store_true", help="List all aliases")
	parser.add_argument("message", nargs=argparse.REMAINDER)

	args = parser.parse_args()
	if args.alias:
		add_alias(*args.alias)

	aliases = parse_aliases()
	if args.list:
		for name, number in sorted(aliases.items()):
			print(f"{name}\t{number}")

		exit(0)

	if args.recipient and args.message:
		to = args.recipient.lower()
		if to in aliases:		
			resp = send_message_to_user(
				aliases[to], " ".join(args.message)
			)

			if resp['code'] != 0: 
				print("Failed to send message!")
			else:
				print("Message sent!")
		else:
			print(f"Alias {to} could not be located; try adding one with --alias!")