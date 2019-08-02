# -*- coding: utf-8 -*-
import wx
import matplotlib
import pathlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas



import DBManager
import Plotter
import io


class UIConnector(wx.Frame):
	mAppName = 'O-Stats'
	mDBManager = None
	mPlotter = None

	mEventChosen =''
	fig = None

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title=self.mAppName, size=(820, 720))
		self.mDBManager = DBManager.DBManager()
		self.mPlotter = Plotter.Plotter(self.mDBManager)

		# Splitter window
		self.sp = wx.SplitterWindow(self)
		self.topPanel = wx.Panel(self.sp, style=wx.RAISED_BORDER)
		self.mainPanel = wx.Panel(self.sp)
		self.sp.SplitHorizontally(self.topPanel, self.mainPanel, 50)
		self.mainPanel.SetBackgroundColour(wx.WHITE)

		# Set the status bar
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText("")

		#create label
		text = wx.StaticText(self.topPanel, label='Events: ', pos=(0, 2))
		font = self.GetFont()
		font.SetPointSize(12)
		text.SetFont(font)

		# Create combo
		filesList = self.getFilesList(self.mDBManager.mRawDataPath)
		self.combo = wx.ComboBox(self.topPanel, style=wx.CB_READONLY, choices=filesList, pos=(60, 2))
		self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)

		# Crete buttons
		self.myButton = wx.Button(self.topPanel, -1, 'Plot', size=(45, 24), pos=(150, 2))
		self.myButton.Bind(wx.EVT_BUTTON, self.graphPlot)

	def OnCombo(self, event):
		self.mEventChosen = self.combo.GetValue()

	def graphPlot(self, event):
		# If we already have a figure in display, remove it
		if self.fig:
			self.fig.canvas.Destroy()

		# if an event was chosen, show its' plot
		if self.mEventChosen:
			csvFile = self.mDBManager.mDataPath + '/' + self.mEventChosen + '.csv'
			self.fig = self.mPlotter.plotLeagueCompetitionClubStats(csvFile)
			FigureCanvas(self.mainPanel, -1, self.fig)

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

