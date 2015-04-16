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