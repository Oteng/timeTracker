import ast
import pyttsx
from datetime import date
from PyQt4.QtCore import *
import time
from PyQt4.QtGui import * 
import re


class settFileProcessor(object):
	"""this file contains function for working on the settings 
		file that contains the intervals for each call to pttsx to say
		the time"""
	def __init__(self):
		super(settFileProcessor, self).__init__()
		""" self.interval: lsit of asseptabel intervals 
			self.minuts: int interval in minuts """
		self.intervals = [None,'5','10','15','20','25','30','35','40','45','50','55','60']
		self.minuts = self.loadSett()

	def writeMinut(self):
		""" create settings file and save the new 
			minuts """
		try:
			if self.minuts != None:
				f = file('settings', 'w')
				f.write(str(self.minuts))
			else:
				raise ValueError
		except IOError, e:
			print e
		except TypeError, e:
			print e
		finally:
			f.close()

	def loadSett(self):
		""" load content of settings and return as int 
			content: str of minuts"""
		try:
			f = file('settings', 'r')
			content = f.read()
		except IOError, e:
			print e
			return None
		finally:
			f.close()
		return int(content)

	def setMinut(self, index):
		""" set minuts to new minuts at index 
			index: int """
		self.minuts = self.intervals[index]

	def getMinut(self):
		""" return minuts """ 
		return self.minuts



class remFileProcessor(object):
	""" content function for processing the reminder file"""
	def __init__(self):
		super(remFileProcessor, self).__init__()
		
	def getData(self):
		""" returns the data of reminder as a list of dics 
			content: list of dic of reminders"""
		content = []
		try:
			f = file('reminder','r')
			for i in f.readlines():
				content.append(ast.literal_eval(i))
				f.close()
		except IOError, e:
			print e
			return None
		except Exception, e:
			f.close()
			print e
			return None

		return content

	def writeData(self, listofdic):
		""" write dic of reminder to reminder file
			listofdic: list """
		if len(listofdic) == 0:
			try:
				f = file('reminder', 'w')
				f.write('')
			except IOError, e:
				print e
				return None
			finally:
				f.close()

		else:
			try:
				f = file('reminder', 'w')
				for i in listofdic:
					f.write(str(i)+'\n')
			except IOError, e:
				print e
				return None
			except Exception, e:
				print e
				return False
			finally:
				f.close()
			return True

class timeTracker(object):
	"""contents the logic for cal the time and saying it"""
	def __init__(self, arg):
		super(timeTracker, self).__init__()
		self.arg = arg
		self.speak = pyttsx.init()

	def getTime(self):
		""" using time.localtime(), return the string represenatation 
			of the current time """
		hour = time.localtime().tm_hour % 12
		if hour == 0:
			hour = 12

		if time.localtime().tm_min == 0 and time.localtime().tm_hour == 0:
			return 'the time is 12 midnite'
		elif time.localtime().tm_min == 0 and time.localtime().tm_hour == 12:
			return 'the time is 12 noon'
		elif time.localtime().tm_hour < 12:
			if time.localtime().tm_min != 0:
				return 'the time is %d:%dam' %(hour, time.localtime().tm_min)
			else:
				return 'the time is %d oklok am' %(hour)
		elif time.localtime().tm_hour == 12:
			return 'the time is %d: %d pm' %(time.localtime().tm_hour, time.localtime().tm_min)
		elif time.localtime().tm_hour > 12:
			if time.localtime().tm_min != 0:
				return 'the time is %d: %d pm' %(hour, time.localtime().tm_min) 
			else:
				return 'the time is %d oklok pm' %(hour)

	def getDate(self, day):
		""" returns string representation of today"""
		today = date.today()
		if day == 1:
			return 'today is %s, the %sst of %s %s' %(today.strftime(
				'%A'), day, today.strftime('%B %Y and '),self.getTime())
		elif day == 2:
			return 'today is %s, the %snd of %s %s' %(today.strftime(
				'%A'), day, today.strftime('%B %Y and '),self.getTime())
		elif day == 3:
			return 'today is %s, the %srd of %s %s' %(today.strftime(
				'%A'), day, today.strftime('%B %Y and '),self.getTime())
		else:
			return 'today is %s, the %sth of %s %s' %(today.strftime(
				'%A'), day, today.strftime('%B %Y and '),self.getTime())
	
	def sayTime(self, minut):
		""" set loop for saying the time """
		self.minut = minut
		self.speak.setProperty('rate', 100)
		day = time.localtime().tm_mday
		startDay = 0
		while True:
			if startDay != time.localtime().tm_mday:
				self.speak.say(self.getDate(time.localtime().tm_mday))
				self.speak.runAndWait()
				startDay = time.localtime().tm_mday
				self.arg.emit(SIGNAL('newDay'))
			elif time.localtime().tm_min % self.minut == 0:
				self.speak.say(self.getTime())
				self.speak.runAndWait()
			time.sleep(((self.minut - (time.localtime().tm_min % self.minut)) * 60))

class settDl(QDialog):
	"""content codes for rendering the setting dialog box"""
	def __init__(self, parent=None):
		super(settDl, self).__init__(parent)
		self.sett = settFileProcessor()
		layout = QVBoxLayout()
		minut = (str(self.sett.getMinut())+' min','5 min','10 min','15 min','20 min','25 min',
				'30 min','35 min','40 min','45 min','50 min','55 min','60 min')
		settLabel = QLabel('Say the time every:')
		minutInterval = QComboBox()
		minutInterval.addItems(minut)
		btn = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		layout.addWidget(settLabel)
		layout.addWidget(minutInterval)
		layout.addWidget(btn)

		self.setWindowTitle('Settings - Time Tracker')
		self.setLayout(layout)
		self.connect(minutInterval, SIGNAL('currentIndexChanged(int)'), lambda arg=minutInterval: self.sett.setMinut(arg))
		self.connect(btn, SIGNAL('accepted()'), self.accept)
		self.connect(btn, SIGNAL('rejected()'), self.close)
		self.setMaximumWidth(90)

	def accept(self):
		self.sett.writeMinut()
		self.emit(SIGNAL('settingsUpdated'))
		self.close()


class Reminder(QDialog):
	"""content codes for rendering the reminder dialog box"""
	def __init__(self, parent=None):
		super(Reminder, self).__init__(parent)
		self.remProcessor = remFileProcessor()
		self.remData = self.remProcessor.getData()
		self.deleteList = []

		self.titleBox = QLineEdit('Title')
		self.titleBox.selectAll()
		self.noteBox = QTextEdit('Note')
		self.noteBox.setMaximumHeight(90)
		self.dateAndTime = QDateTimeEdit()
		self.dateAndTime.setCalendarPopup(True)
		self.dateAndTime.setDisplayFormat('d/M/yyyy h:mm:ss AP')

		self.btn1 = QPushButton('Ok')
		self.btn2 = QPushButton('Cencel')
		self.btn3 = QPushButton('Reset')

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		line2 = QFrame()
		line2.setFrameShape(QFrame.HLine)
		line2.setFrameShadow(QFrame.Sunken)

		Vlayout = QVBoxLayout()
		Vlayout.addWidget(self.titleBox)
		Vlayout.addWidget(self.noteBox)
		Vlayout.addWidget(self.dateAndTime)
		Vlayout.addWidget(line)

		self.remDataLayout = QGridLayout()
		self.buildRemDisplay()

		Vlayout.addLayout(self.remDataLayout)
		Vlayout.addWidget(line2)

		Hlayout = QHBoxLayout()
		Hlayout.addWidget(self.btn1)
		Hlayout.addWidget(self.btn2)
		Hlayout.addWidget(self.btn3)

		Vlayout.addLayout(Hlayout)

		self.setLayout(Vlayout)

		self.connect(self.btn1, SIGNAL('clicked()'), self.ok)
		self.connect(self.btn2, SIGNAL('clicked()'), self.close)
		self.connect(self.btn3, SIGNAL('clicked()'), self.reset)
		if self.count != None:
			for i in xrange(self.count):
				self.connect(eval('self.remdel%d' %i), SIGNAL('clicked()'), self.delList)

	def ok(self):

		if self.titleBox.text() == 'Title' or self.noteBox.toPlainText() == 'Note':
			if len(self.deleteList) != 0:
				self.delete()
				self.remProcessor.writeData(self.remData)
				self.emit(SIGNAL('reminderUpdated'))
			self.close()
			return

		elif self.titleBox.text() == '' or self.noteBox.toPlainText() == '':
			self.reset()
			self.noteBox.setText('Fileds not set')
			return

		elif self.titleBox.text() == ' ' or self.noteBox.toPlainText() == ' ':
			self.reset()
			self.noteBox.setText('Invalide Charactors')
			return

		elif QDate.currentDate().getDate() == self.dateAndTime.date().getDate():
			c_t = (QTime.currentTime().hour(),QTime.currentTime().minute())
			s_t = (self.dateAndTime.time().hour(),self.dateAndTime.time().minute())
			if c_t > s_t:
				self.reset()
				self.noteBox.setText("Time passed")
				return
			
		elif QDate.currentDate().getDate() > self.dateAndTime.date().getDate():
			self.reset()
			self.noteBox.setText('Date passed')
			return

		dataStr = '{"title":"%s", "time":"%s", "date":"%s", "note":"%s", "dateStr":"%s"}'%(self.titleBox.text(),self.dateAndTime.time().toString(), 
						unicode(self.dateAndTime.date().getDate()), self.removeSp(self.noteBox.toPlainText()), self.dateAndTime.date().toString())
		data = ast.literal_eval(dataStr)
		if len(self.deleteList) != 0:
			self.delete()
		self.remData.append(data)
		self.remProcessor.writeData(self.remData)
		self.emit(SIGNAL('reminderUpdated'))
		self.close()
		return
		

	def buildRemDisplay(self):
		if self.remData == None or len(self.remData) == 0:
			remLabel = QLabel('NO reminder')
			self.remDataLayout.addWidget(remLabel,0,0)
			self.count = None
		else:
			self.count = 0
			for i in self.remData:
				remTitle = QLabel(QString(i['title']))
				remDate = QLabel(QString(i['dateStr']))
				remTime = QLabel(self.buildTime(i['time']))
				exec('self.remdel%d = QRadioButton("Delete")' %(self.count))
				eval('self.remdel%d.setAutoExclusive(False)' %self.count)
				self.remDataLayout.addWidget(remTitle,self.count,0)
				self.remDataLayout.addWidget(remDate,self.count,1)
				self.remDataLayout.addWidget(remTime,self.count,2)
				self.remDataLayout.addWidget(eval('self.remdel%d' %self.count),self.count,3)
				self.count += 1
	def buildTime(self, remTime ):
		time = ''
		a = 'midnite'
		t = int(remTime[:2])
		if t == 12:
			a = 'noon'
		if t == 0:
			t = 12
		if t > 12:
			t = t % 12
			a = 'pm'
		elif t < 12:
			a = 'am'
		time += (str(t)+':')
		time += str(int(remTime[3:5]))
		
		time += a
		return time

	def delList(self):
		if self.count != None:
			self.deleteList = []
			for i in xrange(self.count):
				if eval('self.remdel%d' %i).isChecked():
					self.deleteList.append(i)

	def delete(self):
		remData = self.remData[:]
		for i in self.deleteList:
			remData.remove(self.remData[i])
		self.remData = remData
		self.deleteList = []

	def reset(self):
		time = QTime(12,0,0)
		date = QDate()
		self.titleBox.setText('')
		self.noteBox.setText('')
		self.dateAndTime.setDate(date)
		self.dateAndTime.setTime(time)

	def removeSp(self, str_):
		sp = re.compile('\n|\t')
		return re.sub(sp, ' ',unicode(str_) )


class mainWindow(QDialog):
	"""docstring for mainWindow"""
	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)
		self.createActions()
		self.createSysTrayIcon()
		self.remProcessor = remFileProcessor()
		self.messagebox = QMessageBox(self)
		self.setWindowIcon(QIcon('icon.png'))
		self.runTimeThread()

	
	def createActions(self):
		self.settings = QAction('Settings', self, triggered=self.setting)
		self.rem = QAction('Reminders', self, triggered=self.reminders)
		self.qut = QAction('Quit', self, triggered=self.quit_)
		self.feedback = QAction('feedback', self, triggered=self.feedBack)
		self.abt = QAction('About', self, triggered=self.about)

	def createSysTrayIcon(self):
		self.sysTrayMenu = QMenu(self)
		self.sysTrayMenu.addAction(self.settings)
		self.sysTrayMenu.addAction(self.rem)
		self.sysTrayMenu.addAction(self.feedback)
		self.sysTrayMenu.addAction(self.abt)
		self.sysTrayMenu.addSeparator()
		self.sysTrayMenu.addAction(self.qut)

		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setIcon(QIcon('icon.png'))
		self.trayIcon.setContextMenu(self.sysTrayMenu)
		self.trayIcon.show()
		self.welcome()

	def feedBack(self):
		self.messagebox.setText(QString('This application is made for you and the developer is ever ready to costomize it to meet your needs. Email him at <font color="blue">otengkwaku@gmail.com</font>'))
		self.messagebox.setWindowTitle(QString('Feedback - Time Tracker' ))
		self.messagebox.show()

	def about(self):
		self.messagebox.setText(QString(' Have you ever found yourself so busy with your PC that you loose track of time? Well Time Tracker is here to help. Time Tracker is a light weight application that keep track of time and reminds you of the time intermittently.<br/>The interval defaults to 15 minits although it can be changed in the settings panel. This App is written with Python 2.7 by Oteng Kwaku a young guy who works as an IT instractor at Ghana Education Services<br/>The scoures code is a valable at <font color="blue">https://github.com/Oteng/timeTracker</font><br/>version 1.0.0'))
		self.messagebox.setWindowTitle("About - Time Tracker")
		self.messagebox.show()
		
	def welcome(self):
		self.trayIcon.showMessage("Welcome - Time Tracker", "click me to change the default settings and also create reminders")

	def runTimeThread(self):
		sett = settFileProcessor()
		self.minut = sett.getMinut()
		self.timeThread = timeTrackerThread(self.minut, self)
		self.timeThread.connect(self.timeThread, SIGNAL('newDay'), self.runRemThread)
		if self.timeThread.isRunning():
			self.timeThread.arg.speak.stop()
			self.timeThread.terminate()
			self.timeThread.start()
		else:
			self.timeThread.start()

	def setting(self):
		sett = settDl(self)
		sett.connect(sett, SIGNAL('settingsUpdated'), self.runTimeThread)
		sett.show()

	def reminders(self):
		rem = Reminder(self)
		rem.connect(rem, SIGNAL('reminderUpdated'), self.runRemThread)
		rem.show()

	def runRemThread(self):
		self.runRem = remThread(self) 
		self.runRem.connect(self.runRem, SIGNAL('remUsed'), self.displayRem)
		self.runRem.remInfoList = self.getRemInforList()
		self.runRem.remInfo = self.remInfo
		if not self.runRem.isRunning():
			self.runRem.start()
		else:
			self.runRem.terminate()
			self.runRem.start()

	def getRemInforList(self):
		date = []
		self.remInfo = self.remProcessor.getData()
		index = 0
		if self.remInfo != None and len(self.remInfo) != 0:
			for i in self.remInfo:
				date.append((eval(i['date']), (int(i['time'][:2]), int(i['time'][3:5])), index))
				index += 1
			date.sort()
			return date
		else:
			return None

	def displayRem(self, indexContent, remInfo):
		if len(remInfo) != 0 :
			self.remProcessor.writeData(remInfo)
		else:
			self.remProcessor.writeData('')
		self.messagebox.setText(QString('<b>Title: </b> %s<br/><b>Note: </b>%s<br/><b>Date: </b>%s <br/><b>Time: </b>%s' %(indexContent['title'], indexContent['note'], indexContent['dateStr'], indexContent['time'])))
		self.messagebox.setWindowTitle('Reminder - Time Tracker')
		self.messagebox.show()

	def quit_(self):
		self.timeThread.arg.speak.stop()
		self.timeThread.terminate()
		if self.runRem.isRunning():
			self.runRem.terminate()
		qApp.quit()


class timeTrackerThread(QThread):
	"""docstring for timeTrackerThread"""
	def __init__(self, minut, parent=None):
		super(timeTrackerThread, self).__init__(parent)
		self.arg = timeTracker(self)
		self.minut = minut

	def run(self):
		self.arg.sayTime(self.minut)


class remThread(QThread):
	"""docstring for remThread"""
	def __init__(self, parent=None):
		super(remThread, self).__init__(parent)
		self.remInfoList = None
		self.remInfo = None

	def run(self):
		
		if self.remInfoList != None:
			remData =self.remInfoList.pop(0)
			remDate = remData[0]
			remTime = remData[1]
			index = remData[2]
			if remDate == QDate.currentDate().getDate():
				while True:
					if (QTime.currentTime().hour() == remTime[0]) and (remTime[1] <= QTime.currentTime().minute()):
						indexContent = self.remInfo.pop(index)
						self.emit(SIGNAL('remUsed'), indexContent, self.remInfo)
						return None
					elif (QTime.currentTime().hour() == remTime[0]) and (remTime[1] > QTime.currentTime().minute()): 
						time.sleep((remTime[1] - QTime.currentTime().minute()) * 60)

					elif QTime.currentTime().hour() < remTime[0]:
						time.sleep((remTime[0] - QTime.currentTime().hour()) * 3600)

			elif remDate < QDate.currentDate().getDate():
				indexContent = self.remInfo.pop(index)
				self.emit(SIGNAL('remUsed'), indexContent, self.remInfo)
				return None

		else:
			return None


import sys
app = QApplication(sys.argv)
spl_pix = QPixmap('splash.png')
spl = QSplashScreen(spl_pix, Qt.WindowStaysOnTopHint)
spl.setMask(spl_pix.mask())
spl.show()
app.processEvents()
time.sleep(1)

QApplication.setQuitOnLastWindowClosed(False) # this make show that systray works and show menu even with out call to show on the object
window = mainWindow()
spl.finish(window)
app.exec_()
