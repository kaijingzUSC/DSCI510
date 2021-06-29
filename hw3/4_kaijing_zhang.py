class message():
	def __init__(self, mail=None, week=None):
	# Initial attributes
		self.mail = mail
		self.week = week

	def __str__(self):
		return (f"From {self.mail} on {self.week}")
	# Help user to print the information they want to get

	def changemail(self, new):
	# If mail is wrong, we can fix it.
		self.mail = new

	def changeweek(self, new):
	# If week is wrong, we can fix it.
		self.week = new

class mailbox():
	def __init__(self, path=None):
		if path == None:
			filename = input("Please enter a file name: ")
		else:
			filename = path
		self.list = list()
		try:
		# Make sure user input a vaild path
			with open(filename, 'r') as file:
			# Open file
				for line in file:
					line = line.split()
					if line != [] and line[0] == "From":
						self.list.append(message(line[1],line[2]))
				# Put mail and week as an oject in file into the list
		except FileNotFoundError:
			print("The path you input is not found!")

	def __getitem__(self, index):
	# Return the value in the list with index or two indices.
		try:
			return (self.list[index].mail, self.list[index].week)
		except IndexError:
			print("Error! Return None!")
			return None

	def delmessage(self, index):
	# Remove a message from list with index
		self.list.pop(index)

	def addmessage(self, msg):
	# Add message out of class
		self.list.append(msg)

	def print_q1(self):
	# Similar with part of Q1 to print the week in file.
		res = dict()
		for item in self.list:
			week = item.week
			if week not in res.keys():
				res[week] = 1
			else:
				res[week] += 1
		if self.list != []:
		# Make sure this class object created successfully
			print(res)

	def print_q2(self):
	# Similar with part of Q2 to print the week in file.
		mail = dict()
		for item in self.list:
			from_ = item.mail
			if from_ not in mail.keys():
				mail[from_] = 1
			else:
				mail[from_] += 1
		large = -float('inf')
		res = dict()
		for key, value in mail.items():
			if value not in res.keys():
				res[value] = list()
			res[value].append(key)
			if value > large:
				large = value
		if self.list != []:
		# Make sure this class object created successfully
			for item in res[large]:
				print(item, end=' ')
			print(large)
