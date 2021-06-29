def question1():
	filename = input("Please enter a file name: ")
	# Prompt user to input a file name
	res = dict()
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
					week = line[2]
					# Pick the week
					if week not in res.keys():
						res[week] = 1
					else:
						res[week] += 1
					# Put the word in result dictionary
	except FileNotFoundError:
		print("The path you input is not found!")
		return
	print(res)
