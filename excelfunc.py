import xlsxwriter

def passwordtoexcel(passwords,usernames):
	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('passwords.xlsx')
	worksheet = workbook.add_worksheet()

	row = 2
	col = 1

	# Iterate over the data and write it out row by row.
	for passw in passwords:
		worksheet.write(row, col, passw)
		row += 1

	# Iterate over the data and write it out row by row.
	row = 2
	col = 0
	for users in usernames:
		worksheet.write(row, col, users+'@iitg.ernet.in')
		row+=1

	# Number of Users for script
	worksheet.write(0, 0, 'Number of Users')
	worksheet.write(0, 1, len(usernames))

	workbook.close()

def votestoexcel(text, certi, publickey, verified, result):
	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('votes.xlsx')
	worksheet = workbook.add_worksheet()
	boolname = 'False'

	row = 2
	worksheet.write(row, 0, 'Plain Text')
	worksheet.write(row, 1, 'Certificate')
	worksheet.write(row, 2, 'Public Key')
	worksheet.write(row, 3, 'Vote Verification')

	row = 3
	col = 0

	# Iterate over the data and write it out row by row.
	for item in text:
		worksheet.write(row, col, item)
		row += 1

	row = 3
	col = 1

	# Iterate over the data and write it out row by row.
	for item in certi:
		worksheet.write(row, col, item)
		row += 1

	row = 3
	col = 2

	# Iterate over the data and write it out row by row.
	for item in publickey:
		worksheet.write(row, col, item)
		row += 1

	row = 3
	col = 3

	# Iterate over the data and write it out row by row.
	for item in verified:
		if (item == 1):
			boolname = 'True'
		else:
			boolname = 'False'
		worksheet.write(row, col, boolname)
		row += 1

	# Number of Users for script
		if (result == 1):
			boolname = 'True'
		else:
			boolname = 'False'
	worksheet.write(0, 0, 'Final Result: All Votes Passed')
	worksheet.write(0, 1, boolname)

	workbook.close()