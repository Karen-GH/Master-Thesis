from telwoord import cardinal

def check_line(length_line, first_word, previous_first_word, current_letter, previous_letter, string_item):
	"""
	Do checks to determine whether a new bibliographical entries should be started
	"""
	
	if first_word.startswith("-") and ("prod.nr" in string_item or "Zie" in string_item or string_item.endswith(".")):
		return True
	
	if "." in first_word or length_line == 1:
		return False
	
	first_letter = first_word[0]
	
	if first_letter.isupper() and first_letter == current_letter and first_letter > previous_letter:
		return True
	else:
		return False

# Read the file with letter annotations
with open("../Data/197101_letter_sections.txt", "r") as infile:
	lines_catalogue = infile.readlines()

# Initiate the variables
string_item = ""
current_letter = ""
previous_letter = ""
previous_first_word = "A"
counter_start = 0
items = []

for line in lines_catalogue:
	if chr(12) in line:
		line = line.replace(chr(12), "")
	
	if "\t" in line:
		line = line.replace("\t", " ")
		if line.strip("\n").replace(" ", "") == "":
			continue
	
	if line == "\n" or line == " " or line == "" or line == " \n":
		continue
	
	if "START" in line:
		counter_start += 1
		previous_letter = current_letter
		current_letter = line.split()[1]
		continue
	
	if counter_start == 0:
		continue
	
	elements_line = line.split()
	length_line = len(elements_line)
	first_word = line.split()[0]
	
	# Check the first word of the line on multiple aspects and change it if necessary
	if "'" in first_word and not first_word == "'":
		first_word = first_word.lstrip("'")
	if first_word != ",":
		first_word = first_word.strip(",")
	if "ij" in first_word or "IJ" in first_word:
		first_word = first_word.replace("ij", "y")
		first_word = first_word.replace("IJ", "Y")
	if not first_word.startswith("-"):
		first_word = first_word.replace("-", "")
	if first_word.isdigit():
		first_word = cardinal(int(first_word), friendly=False)
	if first_word.startswith("0") and current_letter == "O":
		first_word = first_word.replace("0", "O")
	if first_word.startswith("1") and current_letter == "I":
		first_word = first_word.replace("1", "I")
	if first_word == current_letter + ".":
		first_word = first_word.strip(".")
	
	# Check if a new bibliographical entry should be started or not
	check_result = check_line(length_line, first_word, previous_first_word, current_letter, previous_letter, string_item)
	
	# Either create a new entry or concatenate with the current one
	if check_result == True:
		previous_first_word = first_word
		items.append(string_item)
		string_item = line.strip("\n")
	elif check_result == False:
		string_item += line.strip("\n")
	
items.append(string_item)

# Write the bibliographical entries to a file
with open("../Data/Formed_bib_entries_197101.txt", "w") as outfile:
	for item in items:
		if item != "":
			outfile.write(item + "\n\n")