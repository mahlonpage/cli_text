import argparse
from alias_manager import add_alias, add_group_alias, remove_alias, print_aliases, get_send_target
from contact_manager import generate_contacts
from message_sender import send_messages
from utilities import natural_number, split_string


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	# Alias arguments
	parser.add_argument("--alias", nargs=2, metavar=('name, alias'), help="Adds a person from contacts to aliases. Takes a name, alias pair. Name is used to search contacts and alias is used to text.")
	parser.add_argument("--alias_group", nargs=2, metavar=('group_name, alias'), help="Adds a person from contacts to aliases. Takes a name, alias pair. Name is used to search contacts and alias is used to text.")
	parser.add_argument("--remove_alias", nargs=1, help="Removes an alias")
	parser.add_argument("--list", action="store_true", help="List all aliases")

	# Contacts arguments
	parser.add_argument("--update_contacts", action="store_true", help="Updates contacts file by pulling from mac. If true is passed after, delete previous contacts instead of adding to.")

	# Repeat
	parser.add_argument("-r", nargs=1, metavar="repeat_count", type=natural_number, help="Sends as many times as specified")

	# Split
	parser.add_argument("-s", nargs=1, metavar="number_of_pieces", type=natural_number, help="Splits the string to send into multiple separate texts of equal size")

	# Texting arguments
	parser.add_argument("recipient", nargs="?", help="Alias of person to send text to")
	parser.add_argument("message", nargs=argparse.REMAINDER, help="Message to send to recipient")

	args = parser.parse_args()

	if args.alias:
		add_alias(*args.alias)
		exit(0)

	if args.alias_group:
		add_group_alias(*args.alias_group)
		exit(0)

	if args.remove_alias:
		remove_alias(*args.remove_alias)
		exit(0)

	if args.list:
		print_aliases()
		exit(0)

	if args.update_contacts:
		generate_contacts()
		exit(0)

	# If no recipient or message, exit. Everything past here is send messages related
	if not args.recipient or not args.message:
		exit(0)

	message = " ".join(args.message)
	send_target = get_send_target(args.recipient)

	if not send_target:
		print(f"Alias {args.recipient} could not be found. Run --alias to add an alias. Group aliases start with .")
		exit(1)

	repeat_count = args.r[0] if args.r else 1

	if args.s:
		messages = split_string(message, args.s[0])
	else:
		messages = [message]

	send_messages(messages, [send_target], repeat_count)

