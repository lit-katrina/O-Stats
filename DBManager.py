import codecs
import pandas
from bs4 import BeautifulSoup
import csv
import os
import pathlib




def txtPrint(fileName, data):
	with open('DataTables/' + fileName + '.csv', 'w', newline='', encoding='utf-8') as writeFile:
		writer = csv.writer(writeFile, delimiter=',')
		writer.writerows(data)




class DBManager:
	lastUpdateDate = 0

	def createDB(self):
		# Get competitions list
		fileList = self.getCompetitionsFilesList()

		# Open the htm file and parse it
		for filePath in fileList:

			f = codecs.open(filePath, 'r', 'utf-8')
			doc = BeautifulSoup(f.read(), 'html.parser')
			# Find the results table
			table = doc.find('table', attrs={'id': 'ctl00_ContentPlaceHolder1_rGridLeagueResults_ctl00'})
			data = []
			# Parse tables' head
			table_head = table.find('thead')
			row = table_head.find_all('tr')
			cols = row[0].find_all('th')
			cols = [ele.text.strip() for ele in cols]
			cols[2] = cols[2][::-1]	 # Hebrew reverse
			cols.append('קטגוריה')
			cols.append('Gender')
			data.append(cols)

			# Parse tables' body
			table_body = table.find('tbody')
			rows = table_body.find_all('tr')
			category = ''
			for row in rows:
				cols = row.find_all('td')
				cols = [ele.text.strip() for ele in cols]
				#cols = [ele for ele in cols if ele]  # Get rid of empty values
				cols = [ele.replace('\r\n', ' ') for ele in cols]

				if len(cols) == 2:  # if it's a category column
					category = cols[1].replace('קטגוריה: ', '')
				else:
					if(cols[2]):
						cols[2] = cols[2][::-1]  # Hebrew reverse
					# Add category
					cols.append(category)
					# Add gender
					if category[0] == 'D':
						cols.append('D')
					elif category[0] == 'H':
						cols.append('H')
					else:
						cols.append('U')
					# Clean external participant brackets
					cols[1] = cols[1].replace(']', '')
					cols[1] = cols[1].replace('[ ', '')
					# Remove additional spaces
					cols = [' '.join(ele.split()) for ele in cols]

					data.append(cols)

			# Clean the data
			indexToRemove = 5 #data[0].index(4)
			for row in data:
				if len(row) > indexToRemove:
					row.pop(indexToRemove)

			fileName = filePath[filePath.rfind('\\') + 1: filePath.rfind('.')]
			txtPrint(fileName, data)


	def createMembersDB(self):
		header = pandas.DataFrame({'מספר חבר': [], 'שם פרטי': [], 'שם משפחה': []})
		header.to_csv(path_or_buf='members.csv', mode='w', index=False)

		path = pathlib.Path(__file__).parent / 'DataRaw/Members'
		files = []
		for f in os.walk(path):
			for file in f[2]:
				if '.csv' in file:
					files.append(file)
		for membersFile in files:
			fileName2 = 'DataRaw/Members/' + membersFile
			res = pandas.read_csv(fileName2, na_filter=False, header=0, usecols=[0,1,2])
			res.to_csv(path_or_buf='members.csv', mode='a', header=None, index=False)

		#members = pandas.read_csv('members.csv', na_filter=False, header=0)

	# ----------------------------- Private Functions -----------------------------------------
	def getCompetitionsFilesList(self):
		filesList = []
		for p in pathlib.Path('./DataRaw/2009-2010').iterdir():
			if p.is_file():
				filesList.append(str(p))
		return filesList


def main():
	dbManager = DBManager()
	dbManager.createDB()
	dbManager.createMembersDB()



if __name__ == '__main__':
	main()