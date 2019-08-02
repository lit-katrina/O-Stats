import unittest
import os.path
import sys
import csv

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

from DBManager import DBManager

class TestDBManager(unittest.TestCase):

	def test_getFilesList(self):
		# Path not found
		res = DBManager().getCompetitionsFilesList('../Data')
		self.assertEqual(res, [], "Should be empty list []")
		# Have a result
		res = DBManager().getCompetitionsFilesList('../DataRaw/2009-2010')
		self.assertNotEqual(res, [], "Should not be an empty list")
		# All the entries are files of html type
		for file in res:
			self.assertNotEqual(file.find('.html'), -1, file + " should  be a html")

	def test_saveToFile(self):
		fileName = 'test'
		filePath = '.'
		formatted = filePath + '/' + fileName +'.csv'
		data = [['1'], ['2'], ['3'], ['4']]

		# Create a file and check its' contents
		DBManager().saveToFile(fileName, filePath, data)
		with open(formatted) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			i = 0
			for row in csv_reader:
				self.assertEqual(row, data[i])
				i = i + 1

		# Remove the file
		os.remove(formatted)

if __name__ == '__main__':
	unittest.main()