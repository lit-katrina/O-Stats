# -*- coding: utf-8 -*-
import codecs
import pandas
import csv
import os
import pathlib
from bs4 import BeautifulSoup

class DBManager:
	mLastUpdateDate = 0
	mRawDataPath = './DataRaw/2009-2010'
	mDataPath = 'DataTables'
	mCATEGORY_ROW = 2
	mPARTICIPANT = 1
	mCLUB = 2


	def createDB(self):
		# Get competitions list
		fileList = self.getCompetitionsFilesList(self.mRawDataPath)

		# Open the html file and parse it
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
				cols = [ele.replace('\r\n', ' ') for ele in cols]
				# Remove additional spaces
				cols = [' '.join(ele.split()) for ele in cols]

				if len(cols) == self.mCATEGORY_ROW:  # if it's a category row
					category = cols[1].replace('קטגוריה: ', '')
				else:
					if cols[self.mCLUB]: # if a competitor is in the club
						cols[self.mCLUB] = cols[self.mCLUB][::-1]  # Hebrew reverse

					# Add category
					cols.append(category)
					# Add gender
					self.addGender(cols, category)
					# Clean external participant brackets
					cols[self.mPARTICIPANT] = cols[self.mPARTICIPANT].replace(']', '')
					cols[self.mPARTICIPANT] = cols[self.mPARTICIPANT].replace('[ ', '')

					data.append(cols)

			# Remove not relevant cols
			colToRemove = 5
			for col in data:
				if len(col) > colToRemove:
					col.pop(colToRemove)

			fileName = filePath[filePath.rfind('\\') + 1: filePath.rfind('.')]
			self.saveToFile(fileName, self.mDataPath, data)

	# Not in use yet
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
	def getCompetitionsFilesList(self, path):
		filesList = []
		try:
			for p in pathlib.Path(path).iterdir():
				if p.is_file():
					p = str(p)
					if p.find('html'):
						filesList.append(str(p))
			return filesList
		except FileNotFoundError:
			return []

	def addGender(self, cols, category):
		if category[0] == 'D' or category == 'ילדות':
			cols.append('Woman')
		elif category[0] == 'H' or category == 'ילדים':
			cols.append('Man')
		else:
			cols.append('Unknown')

	def saveToFile(self, fileName, filePath, data):
		with open(filePath + '/' + fileName + '.csv', 'w', newline='', encoding='utf-8') as writeFile:
			writer = csv.writer(writeFile, delimiter=',')
			writer.writerows(data)

def main():
	dbManager = DBManager()
	dbManager.createDB()
	dbManager.createMembersDB()



if __name__ == '__main__':
	main()