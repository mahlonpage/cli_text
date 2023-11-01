import os
from contact_manager import search_contacts

ALIAS_FILE = os.path.join(os.path.dirname(__file__), "files/aliases.txt")

"""

"""
def get_phone_number(search_term):
	search_term = search_term.lower().strip()
	with open(ALIAS_FILE, 'r+') as af:
		for line in af:
			alias, number = line.split(":")
			alias, number = alias.strip(), number.strip()
			if alias == search_term:
				return number
	print("No alias found")

"""
Queries the user to get which search contact they were looking for
options -- list of options to choose from
"""
def get_user_alias_choice(options):
	while True:
		pretty_print_list(options)
		user_choice = input("Which user would you like to select? (enter a 1-indexed number): ")
		if user_choice.isdigit():
			user_choice = int(user_choice)
			if 1 <= user_choice <= len(options):
				break
		print("Enter a valid 1-indexed number")

	return user_choice

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
		index = get_user_alias_choice(search_results)
		choice = search_results[index]

	# Add new alias, phone number pair
	phone_number = choice[1]
	with open(ALIAS_FILE, 'a') as af:
		af.write(f"{alias} : {phone_number}\n")

	print(f"Added alias: {alias} | {phone_number}")
	return

"""
Prints all aliases
"""
def print_aliases():
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
Pretty printing helper function
"""
def pretty_print_list(list):
	for i, item in enumerate(list):
		print(f"{i+1}. {item}")