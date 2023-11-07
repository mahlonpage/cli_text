import os
from contact_manager import search_contacts
from utilities import pretty_print_list, get_user_selection

ALIAS_FILE = os.path.join(os.path.dirname(__file__), "files/aliases.txt")

"""
Finds the group chat name / phone number of the recipient our alias is looking for
search_term -- Alias to look for in our files
"""
def get_send_target(search_term):
	print(search_term)
	search_term = search_term.lower().strip()
	with open(ALIAS_FILE, 'r+') as af:
		for line in af:
			alias, send_target = line.split(":")
			alias, send_target = alias.strip(), send_target.strip()
			if alias == search_term:
				return send_target
	print("No alias found")

"""
Function to add a new alias for texting
name -- item to search in contacts for
alias -- alias by which to text the phone number associated with the name
"""
def add_alias(name, alias):
	alias = alias.lower().strip()
	if _alias_exists(alias):
		print(f"Alias: {alias}, already exists")
		return

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

	_sort_alias_file()

	print(f"Added alias for {choice[0]}: {alias} : {phone_number}")
	return

"""
Function to add a new alias for a group to text.
Note, all group aliases are appended by a '.'
group_name -- exact group name to text
alias -- alias by which to text the group
"""
def add_group_alias(group_name, alias):
	alias = alias.lower().strip()
	alias = "." + alias

	if _alias_exists(alias):
		print(f"Alias: {alias}, already exists")
		return

	with open(ALIAS_FILE, 'a') as af:
		af.write(f"{alias} : {group_name}\n")

	_sort_alias_file()

	print(f"Added alias {alias} : {group_name}")
	return

"""
Removes a given alias
alias -- alias to remove
"""
def remove_alias(alias):
	if not _alias_exists(alias):
		print (f"Alias {alias} does not exist.")
		return

	lines = _get_alias_list()
	with open(ALIAS_FILE, 'w+') as af:
		for line in lines:
			curr_alias, _ = line.split(":")
			curr_alias = curr_alias.strip().lower()
			if alias != curr_alias:
				af.write(f"{line}\n")
	return

"""
Prints all aliases
"""
def print_aliases():
	aliases = _get_alias_list()
	pretty_print_list(aliases)
	return

"""
Returns a bool representing if an alias already exists
"""
def _alias_exists(alias):
	lines = _get_alias_list()
	for line in lines:
		key = line.split(":")[0]
		key = key.lower().strip()
		if key == alias: return True

	return False

"""
Gets all aliases as a list
"""
def _get_alias_list():
    if not os.path.isfile(ALIAS_FILE):
        with open(ALIAS_FILE, 'w+'):
            pass

    aliases = []
    with open(ALIAS_FILE, 'r+') as af:
        for line in af:
            line = line.strip()
            aliases.append((line))

    return aliases

"""
Sorts the alias file.
"""
def _sort_alias_file():
	aliases = _get_alias_list()
	aliases.sort()
	with open (ALIAS_FILE, 'w+') as af:
		for alias in aliases:
			af.write(f"{alias}\n")