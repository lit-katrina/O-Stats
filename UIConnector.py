import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pip._vendor import colorama
import pathlib

import DBManager
import Plotter
import io


class UIConnector(wx.Frame):
	mAppName = 'O-Stats'
	mEventChosen =''

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title=self.mAppName, size=(700, 700))
		#text = wx.StaticText(self, label='Hello')

		# Splitter window
		self.sp = wx.SplitterWindow(self)
		self.topPanel = wx.Panel(self.sp, style=wx.RAISED_BORDER)
		self.mainPanel = wx.Panel(self.sp)
		self.sp.SplitHorizontally(self.topPanel, self.mainPanel, 100)

		self.mainPanel.SetBackgroundColour(wx.WHITE)

		# Set the status bar
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText("hola")

		# Crete buttons
		self.myButton = wx.Button(self.topPanel, -1, 'Plot', size=(40, 20), pos=(100, 2))
		self.myButton.Bind(wx.EVT_BUTTON, self.graphPlot)

		# Create combo
		filesList = self.getFilesList('./DataRaw/2009-2010')
		self.combo = wx.ComboBox(self.topPanel, style=wx.CB_READONLY, choices=filesList)
		self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)


		#self.Refresh()
	def OnCombo(self, event):
		#self.label.SetLabel("selected " + self.combo.GetValue() + " from Combobox")
		self.mEventChosen = self.combo.GetValue()

	def graphPlot(self, event):
		dbManager = DBManager.DBManager()
		plotter = Plotter.Plotter(dbManager)

		if self.mEventChosen:
			fig = plotter.plotLeagueCompetitionClubStats('DataTables/' + self.mEventChosen + '.csv')
			canvas = FigureCanvas(self.mainPanel, -1, fig)

			self.statusbar.SetStatusText("yes")

	def getFilesList(self, path):
		filesList = []
		for p in pathlib.Path(path).iterdir():
			if p.is_file():
				p = str(p)
				fileName = p[p.rfind('\\') + 1: p.rfind('.')]
				filesList.append(fileName)
		return filesList

def main():
	app = wx.App(redirect=False)
	frame = UIConnector(None)
	frame.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()

