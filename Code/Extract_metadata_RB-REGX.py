import glob
import re

# Read the file with bibliographical entries
with open("../Data/Replaced_dashes_197101.txt", "r") as infile:
	lines = infile.readlines()

# Set file header
lines_to_write = ["Author\tTitle\tCity\tPublisher\tYear\tPages\tSize\tISBN\tPrice\tProduct number\n"]

for line in lines:
	# Skip lines that refer to full entries and empty lines
	if line == "\n" or " Zie " in line[:100]:
		continue
	
	# Initiate the variables
	author = "Unknown"
	title = "Unknown"
	city = "Unknown"
	publisher = "Unknown"
	year = "Unknown"
	pages = "Unknown"
	size = "Unknown"
	ISBN = "N/A"
	price = "Unknown"
	prod_no = "Unknown"
	author_split = ""
	after_title = ""
	remainder = ""
	
	
	line = line.strip("\n")
	
	# Extract the author by splitting on a colon
	author_split = line.split(": ", 1)
	author_part = author_split[0]
	if len(author_split) > 1:
		from_author = author_split[1]
	
	if len(author_part) < 60:
		author = author_part.strip(" ")
	
	# Extract the author by splitting on a full stop, either after the author or the first one in the line
	if author != "Unknown":
		title = from_author.split(".", 1)[0]
		if len(from_author.split(".")) > 1:	
			remainder = from_author.split(".", 1)[1]
	elif author == "Unknown":
		title = line.split(".", 1)[0]
		if len(line.split(".")) > 1:	
			remainder = line.split(".", 1)[1]
	
	# Extract the city_of_publication and the publisher by looking for a comma and splitting on it
	if remainder != "":
		if "," in remainder and not ".," in remainder:
			city_part = remainder.split(",", 1)[0]
			publisher_part = remainder.split(",", 1)[1]
			city = city_part.split(".")[-1].strip(" ")
			publisher = publisher_part.split(".")[0].lstrip(" ")
		elif ".," in remainder:
			city_part = remainder.split(".,", 1)[0]
			publisher_part = remainder.split(".,", 1)[1]
			city = city_part.split(".")[-1].strip(" ")
			publisher = publisher_part.split(".")[0].lstrip(" ")
	
	# Extract the ISBN_number using a regular expression
	ISBN_list = re.findall("ISBN.\d{2}.\d{3}.\d{4}..", line)
	if ISBN_list != []:
		ISBN = ISBN_list[0].strip("ISBN").replace(" ", "")
	
	# Extract the price_of_book using a regular expression
	price_list = re.findall(" f[.] \d*[.]\d*|fl[.] \d*[.]\d*", line)
	if price_list != []:
		price = price_list[-1].strip(".").strip(" ")
	
	# Extract the number_of_pages using a regular expression
	pages_list = re.findall("\d+.blz", line)
	if pages_list != []:
		pages = pages_list[0].strip(".").strip("blz").strip(" ")
	
	# Extract the size_of_book using a regular expression
	size_list = re.findall("\d+.x.\d+|\d+.X.\d+", line)
	if size_list != []:
		size = size_list[0].strip(" ")
	
	# Extract the year_of_publication using a regular expression
	year_list = re.findall(" [[]\d{4}[]][.]| \d{4}[.]| 1\d{4}1[.]| \d{4}1[.]", line)
	if year_list != []:
		year = year_list[0].strip(" ").strip(".").strip("[").strip("]")
		if len(year) == 5:
			year = year.rstrip("1")
		elif len(year) == 6:
			year = year[1:-1]
	
	# Extract the production_number using a regular expression
	prod_no_list = re.findall("\d{7}", line)
	if prod_no_list != []:
		if prod_no_list[0].startswith("71"):
			prod_no = prod_no_list[0].replace(" ", "")
	
	line_write = "\t".join([author, title, city, publisher, year, pages, size, ISBN, price, prod_no]) + "\n"
	lines_to_write.append(line_write)
	
	city = "Unknown"
	publisher = "Unknown"
	remainder = ""

# Write the data to a file
with open("../Data/Extracted_metadata_1971.tsv", "w") as outfile:
	for line in lines_to_write:
		outfile.write(line)