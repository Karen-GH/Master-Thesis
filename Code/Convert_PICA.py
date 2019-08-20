# Read the file with the extracted metadata
with open("../Data/Extracted_metadata_1971.tsv", "r") as infile:
	lines = infile.readlines()

lines_to_write = []

for line in lines[1:]:
	line = line.strip("\n")
	elements = line.split("\t")
	
	# Set the variables with the correct metadata
	author = elements[0]
	title = elements[1]
	city = elements[2]
	publisher = elements[3]
	year = elements[4]
	pages = elements[5]
	size = elements[6]
	ISBN = elements[7]
	price = elements[8]
	prod_no = elements[9]
	
	surname = ""
	affixes = ""
	first_name = ""
	
	# Create a list of affixes in Dutch names
	affixed_list = ["van", "de", "der", "den"]
	
	if author != "Unknown":
		
		# Only take the first author
		if " [" in author:
			author = author.split(" [")[0]
		
		# Separate the surname from the rest of the name
		if "," in author:
			surname = author.split(",", 1)[0]
			first_affixes = author.split(",", 1)[1]
			if "," in first_affixes:
				first_affixes = first_affixes.split(",", 1)[0]
			first_affixes_list = first_affixes.split(" ")
			
			# Determine whether it is an affix or part of the first name
			for name in first_affixes_list:
				if name in affixed_list:
					affixes += name + " "
				else:
					first_name += name + " "
			affixes = affixes.strip(" ")
			first_name = first_name.strip(" ")
			
	if title != "Unknown":
		# Re-order titles where the article is not the first word of the title and add the @ in front of the main word
		if (", De," in title or ", Het," in title) and author == "Unknown":
				title = title[0].lower() + title[1:]
				if ", De," in title:
					title = title.replace(", De,", "")
					title = "De @" + title
				elif ", Het," in title:
					title = title.replace(", Het,", "")
					title = "Het @" + title
		elif title.startswith("De") or title.startswith("Het"):
			if title.startswith("De"):
				title = title.replace("De ", "De @")
			elif title.startswith("Het"):
				title = title.replace("Het ", "Het @")
		else:
			title = "@" + title
	
	# Form the PICA+ lines with the correct format
	ISBN_PICA = "004A "
	if ISBN	!= "N/A":
		ISBN_PICA += "$0" + ISBN
	if price != "Unknown":
		ISBN_PICA += "$f" + price
	if ISBN_PICA != "004A ":
		lines_to_write.append(ISBN_PICA)
	if prod_no != "Unknown":
		lines_to_write.append("006C $0B" + prod_no)
	if year != "Unknown":
		lines_to_write.append("011@ $a" + year)
	if title != "Unknown":
		lines_to_write.append("021A $a" + title)
	if author != "Unknown":
		author_PICA = "028A "
		if first_name != "":
			author_PICA += "$d" + first_name
		if affixes != "":
			author_PICA += "$c" + affixes
		if surname != "":
			author_PICA += "$a" + surname
		lines_to_write.append(author_PICA)
	city_PICA = "033A "
	if city != "Unknown":
		city_PICA += "$p" + city
	if publisher != "Unknown":
		city_PICA += "$n" + publisher
	if city_PICA != "033A ":
		lines_to_write.append(city_PICA)
	if pages != "Unknown":
		lines_to_write.append("034D $a" + pages)
	if size != "Unknown":
		lines_to_write.append("034I $a" + size)
	lines_to_write.append("")

# Write the data to a file
with open("../Data/Extracted_metadata_1971_PICA.txt", "w") as outfile:
	for line in lines_to_write:
		outfile.write(line + "\n")