class base_message():
	def __init__(self, week=None, name=None, date=None):
	# Initial attributes. All attributes are what should have in basic message I think.
		self.week = week
		self.name = name
		self.date = date

	def __str__(self):
		return (f"Week:{self.week}; Name: {self.name}; Date: {self.date}")
		# print what basic data saved

	def changeweek(self, new):
		self.week = new


class email_message(base_message):
	def __init__(self, mail=None, week=None, name=None, date=None):
		super().__init__(week, name, date)
		self.mail = mail
		# email specific

	def __str__(self):
		return (f"Name: {self.name}; E-mail Address: {self.mail}; Week:{self.week}; Date: {self.date}")
		# print what basic data saved

	def changemail(self, new):
		self.mail = new

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
						self.list.append(email_message(line[1],line[2]))
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
