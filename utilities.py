"""
Pretty printing helper function
"""
def pretty_print_list(list):
	for i, item in enumerate(list):
		print(f"{i+1}. {item}")

"""
Queries the user to select an item from a list.
options -- list of options to choose from
"""
def get_user_selection(options):
	while True:
		pretty_print_list(options)
		user_choice = input("Which option would you like to select? (enter a 1-indexed number): ")
		if user_choice.isdigit():
			user_choice = int(user_choice)
			if 1 <= user_choice <= len(options):
				break
		print("Enter a valid 1-indexed number")

	return user_choice