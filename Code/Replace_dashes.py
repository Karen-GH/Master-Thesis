import glob
import nltk
import re

def author_title(line):
	"""
	Extract the author and title from a line and return them
	"""
	
	author = "Unknown"
	title = "Unknown"
	index_dot = line.find(".")
	
	if not line.strip(" ").startswith("-"):
		list_dots = [m.start() for m in re.finditer("[.]", line)]
		for match in list_dots:
			if ":" in line[:match] and len(line[:match]) < 50:
				index_dot = match
				break
	
	title_part = line[:index_dot]
	if ":"in title_part:
		author = title_part.split(":")[0]
		title = title_part.split(":")[1]
	
	else:
		title = title_part
	
	return author, title

# Read the file with bibliographical entries
with open("../Data/Reformed_bib_entries_197101.txt", "r") as infile:
	lines_catalogue = infile.readlines()

new_lines = []
prev_author_title = ("Unknown", "Unknown")

for index_line, line in enumerate(lines_catalogue):
	if line == "\n":
		continue
	
	prev_author, prev_title = prev_author_title
	
	# Replace a dash with the correct author or first word of the title
	if line.strip(" ").startswith("-"):
		line_current = line.strip(" ").strip("-")
		current_author, current_title = author_title(line_current)
		if prev_author != "Unknown":
			author = prev_author
			if not line_current.strip(" ").startswith("en") and not line_current.startswith("[en]") and current_author == "Unknown":	
				line = author + ": " + line_current
			else:
				line = author + " " + line_current
		
		elif prev_title != "Unknown":
			first_word_prev_title = prev_title.split(" ")[0]
			line = prev_title.split(" ")[0] + " " + line.strip(" ").strip("-") 
	
	# Extract the author and title of the current line to be used for possible dashes in next lines
	if not line.strip(" ").startswith("-"):	
		if " Zie " in line and not ("fl." in line or "blz" in line or "p." in line or "No." in line or " f " in line):
			author = "Unknown"
			title = "Unknown"
			entry = line.split(" Zie ")[0]
			if "," in entry:
				author = entry
			else:
				title = entry
			prev_author_title = (author, title)
		
		else:
			author, title = author_title(line)
			prev_author_title = (author, title)

	new_lines.append(line + "\n")

# Write the bibliographical entries to a file
with open("../Data/Replaced_dashes_197101.txt", "w") as outfile:
	for line in new_lines:
		outfile.write(line)