from telwoord import cardinal
import glob

def check_word(first_word):
	"""
	Check the first word of the line on multiple aspects and change it if necessary
	"""
	
	if "'" in first_word and not first_word == "'":
		first_word = first_word.lstrip("'")
	if "£" in first_word:
		first_word = first_word.replace("£", "f")
	if first_word != ",":
		first_word = first_word.strip(",")
	if first_word.startswith("mc"):
		first_word = first_word.replace("mc", "mac")
	if "ij" in first_word or "IJ" in first_word:
		first_word = first_word.replace("ij", "y")
		first_word = first_word.replace("IJ", "Y")
	if "-" in first_word and not first_word == "-":
		first_word = first_word.replace("-", "")
	if first_word.isdigit():
		first_word = cardinal(int(first_word), friendly=False)
	if first_word.startswith("0"):
		first_word = first_word.replace("0", "O")
	if first_word.startswith("1"):
		first_word = first_word.replace("1", "I")
	first_word = first_word.strip(".")
	return first_word

# Read the file with bibliographical entries
with open("../Data/Formed_bib_entries_197101.txt", "r") as infile:
	lines_catalogue = infile.readlines()

new_lines = [lines_catalogue[0]]
lines_remove = []
merged = False
merged_line = ""
stripe = False
first_word_prev = lines_catalogue[0].split()[0].strip(",").lower()
first_word_prev = check_word(first_word_prev)

for line in lines_catalogue[2:-2:2]:
	if line == "\n":
		continue
	
	# Set the current, previous and next line
	index_line = lines_catalogue.index(line)
	if merged == True:
		previous_line = merged_line
	else:	
		previous_line = lines_catalogue[index_line-2]
	next_line = lines_catalogue[index_line+2]
	
	# Set the previous first word
	if previous_line.strip(" ").startswith("-"):
		first_word_prev = first_word_prev	
	elif not previous_line.strip(" ").startswith("-"):
		first_word_prev = previous_line.split()[0].strip(",").lower()
	
	# Set the current first word
	if line.strip(" ").startswith("-"):
		first_word_current = first_word_prev
	elif not line.strip(" ").startswith("-"):
		first_word_current = line.split()[0].strip(",").lower()
	
	# Set the next first word
	if next_line.strip(" ").startswith("-"):
		first_word_next = first_word_current
	elif not next_line.strip(" ").startswith("-"):
		first_word_next = next_line.split()[0].strip(",").lower()
	
	# Check the first words if they need to be adapted before comparison
	first_word_prev = check_word(first_word_prev)
	first_word_current = check_word(first_word_current)
	first_word_next = check_word(first_word_next)
	
	# Never merge when the next line starts with a dash
	if (next_line.strip(" ").startswith("-")):
		new_lines.append(line)
		continue
	
	# Check if the words are in alphabetical order and if not merge the lines, and remove the original lines
	if (first_word_current < first_word_prev and next_line.strip(" ").startswith("-"))\
		or (first_word_current > first_word_prev and first_word_current > first_word_next and first_word_next >= first_word_prev)\
		or (first_word_current < first_word_prev and first_word_current < first_word_next and first_word_next >= first_word_prev):
		new_line = previous_line.strip("\n") + line
		merged_line = new_line
		merged = True
		lines_remove.append(previous_line)
		lines_remove.append(line)
	else:
		new_line = line
		merged = False
	new_lines.append(new_line)
	
new_lines.append(next_line)

# Remove the lines that have been merged with another line
for line in lines_remove:
	if line in new_lines:	
		new_lines.remove(line)

# Write the bibliographical entries to a file
with open("../Data/Reformed_bib_entries_197101.txt", "w") as outfile:
	for line in new_lines:
		outfile.write(line + "\n")