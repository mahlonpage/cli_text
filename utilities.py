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

	# Returns a 0-indexed value
	return user_choice - 1
"""
Convenient math function that splits a string as evenly as
possible weighted extra characters toward later pieces
string -- the string to split
pieces -- number of pieces to split into
"""
def split_string(string, pieces):
	string_len = len(string)

	smaller_piece_size = string_len % pieces
	larger_piece_size = string_len // pieces

	res = []
	for i in range(pieces - smaller_piece_size):
		res.append(string[i * larger_piece_size: (i + 1) * larger_piece_size])

	for i in range(smaller_piece_size):
		start = (pieces - smaller_piece_size) * larger_piece_size + i * (larger_piece_size + 1)
		end = (pieces - smaller_piece_size) * larger_piece_size + (i + 1) * (larger_piece_size + 1)
		res.append(string[start:end])

	return res

# Natural number definition for argparse types
def natural_number(i):
	value = int(i)
	if value < 1:
		print(f"{value} is not a natural number, must be a natural number >= 1")
		exit(1)
	return value