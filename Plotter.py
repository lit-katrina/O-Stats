# -*- coding: utf-8 -*-
"""
This unit is responsible for creating diagrams, using the database manager
"""

import pandas as pd
import matplotlib.pyplot as plt

import DBManager


class Plotter:
	dataFrame = None

	def __init__(self, dbManager):
		self.database = dbManager

	# API functions
	# This function creates a plot of participants grouped by clubs and gender
	def plotLeagueCompetitionClubStats(self, fileName):
		try:
			self.dataFrame = pd.read_csv(fileName, na_filter=False, index_col=0, header=0)
		except FileNotFoundError:
			self.database.createDB()
			self.dataFrame = pd.read_csv(fileName, na_filter=False, index_col=0, header=0)

		club = 'מועדון'[::-1] # Hebrew reverse
		# Plot the graph
		myPlt = self.dataFrame.groupby([club, 'Gender'])['שם'].nunique().unstack()
		colors = ['xkcd:blue', 'xkcd:orangered', 'xkcd:silver']
		myPlt = myPlt.plot(kind='bar', stacked=True, title="Partisipants in the event", color = colors, figsize=(8, 6))
		# correcting legend place
		myPlt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
		# To show all the graph
		plt.tight_layout()
		# Make y axes from 0 to 90
		axes = plt.gca()
		axes.set_ylim([0, 90])

		return myPlt.get_figure()

def main():
	dbManager = DBManager.DBManager()
	plotter = Plotter(dbManager)
	p = plotter.plotLeagueCompetitionClubStats('DataTables/07.11.2009.csv')
	plt.show()


if __name__ == '__main__':
	main()