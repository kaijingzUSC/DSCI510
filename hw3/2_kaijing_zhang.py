def question2():
	filename = input("Please enter a file name: ")
	# Prompt user to input a file name
	mail = dict()
	try:
	# Make sure user input a vaild path
		with open(filename, 'r') as file:
		# Open file
			for line in file:
			# Read each line in file
				line = line.split()
				# Pick each word in line, then put in a list
				if line != [] and line[0] == "From":
				# Make sure the line is expected, which means it start from "From"
					week = line[1]
					# Pick the e-mail address
					if week not in mail.keys():
						mail[week] = 1
					else:
						mail[week] += 1
					# Put the word in a dictionary
	except FileNotFoundError:
		print("The path you input is not found!")
		return
	large = -float('inf')
	# Default the largest count
	res = dict()
	for key, value in mail.items():
	# Make a new dictionary with key and value, occur times and e-mail address
		if value not in res.keys():
			res[value] = list()
		res[value].append(key)
		if value > large:
			large = value
	for item in res[large]:
	# Print all e-mails which occur in same times.
		print(item, end=' ')
	print(large)
