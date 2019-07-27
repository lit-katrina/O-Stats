'''
This unit is responsible for creating diagrams,using the database manager
'''
import pandas
import matplotlib.pyplot as plt

import DBManager


class Plotter:

	def __init__(self, dbManager):
		self.database = dbManager

	# API functions
	def plotLeagueCompetitionClubStats(self, fileName):
		dataFrame = pandas.read_csv(fileName, na_filter=False, index_col=0, header=0)
		club = 'מועדון'[::-1] # Hebrew reverse
		myPlt = dataFrame.groupby([club, 'Gender'])['שם'].nunique().unstack().plot(kind='bar', stacked=True, title="Partisipants in the event")
		plt.tight_layout()  # To show all the graph

		return myPlt.get_figure()

def main():
	dbManager = DBManager.DBManager()

	plotter = Plotter(dbManager)
	fig = plotter.plotLeagueCompetitionClubStats()
	plt.show()


if __name__ == '__main__':
	main()