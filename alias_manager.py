import os
from contact_manager import search_contacts

ALIAS_FILE = os.path.join(os.path.dirname(__file__), "files/aliases.txt")

"""
Finds the group chat name / phone number of the recipient our alias is looking for
search_term -- Alias to look for in our files
"""
def get_send_goal(search_term):
	search_term = search_term.lower().strip()
	with open(ALIAS_FILE, 'r+') as af:
		for line in af:
			alias, send_goal = line.split(":")
			alias, send_goal = alias.strip(), send_goal.strip()
			if alias == search_term:
				return send_goal
	print("No alias found")

"""
Function to add a new alias for texting
name -- item to search in contacts for
alias -- alias by which to text the phone number associated with the name
"""
def add_alias(name, alias):
	alias = alias.lower().strip()

	name = name.lower().strip()
	search_results = search_contacts(name)
	if not search_results:
		print(f"No contacts found match this search input: {name}")
		return

	# Select the correct relevant option from our search
	choice = search_results[0]
	if len(search_results) != 1:
		index = get_user_selection(search_results)
		choice = search_results[index]

	# Add new alias, phone number pair
	phone_number = choice[1]
	with open(ALIAS_FILE, 'a') as af:
		af.write(f"{alias} : {phone_number}\n")

	print(f"Added alias: {alias} : {phone_number}")
	return

"""
Function to add a new alias for a group to text.
Note, all group aliases are appended by a '.'
group_name -- exact group name to text
alias -- alias by which to text the group
"""
def add_group_alias(group_name, alias):
	alias = alias.lower().strip()
	alias = "~" + alias

	with open(ALIAS_FILE, 'a') as af:
		af.write(f"{alias} : {group_name}\n")

	print(f"Added alias {alias} : {group_name}")
	return

"""
Gets all aliases as a list
"""
def get_alias_list():
    if not os.path.isfile(ALIAS_FILE):
        with open(ALIAS_FILE, 'w+'):
            pass

    aliases = []
    with open(ALIAS_FILE, 'r+') as af:
        for line in af:
            line = line.strip()
            aliases.append((line))

    pretty_print_list(aliases)
    return

"""
Prints all aliases
"""
def print_aliases():
	aliases = get_alias_list()
	pretty_print_list(aliases)
	return

"""
Pretty printing helper function
"""
def pretty_print_list(list):
	for i, item in enumerate(list):
		print(f"{i+1}. {item}")

"""
Queries the user to get which search contact they were looking for of the found aliases
options -- list of options to choose from
"""
def get_user_selection(options):
	while True:
		pretty_print_list(options)
		user_choice = input("Which user would you like to select? (enter a 1-indexed number): ")
		if user_choice.isdigit():
			user_choice = int(user_choice)
			if 1 <= user_choice <= len(options):
				break
		print("Enter a valid 1-indexed number")

	return user_choice