timeTracker
===========

A Python 2.7 program that demonstrate the use of PyQt and Pyttsx

TimeTracker is a python 2.7 program that demonstrate the use of PyQt and pyttsx while creating a simply but unique application for everyday use. 
This application demonstrates the use of PyQt’s QDialog class, QSystem Tray Icon class, and also Multithreading. 
It also demonstrates the use of pyttsx which is a text to speech engine. 
Time Tracker is a simply application the runs three threads. 
The main thread is made up of the QSystemTrayIcon. The other secondary threads comes in when there is work to be done, or the user needs to make changes.
If you have ever used or seen the application “SAY THE TIME”, well timeTracker is just like it but will more features  like:  the ability of a user to change the default intervals at which the time is said and also the ability of the user to create reminders. 
Installation 
1.  You will need the following libraries installed 
	a.	Python 2.7 
		http://www.python.org/download/releases/2.7.5/
	b.	Pyttsx
		https://pypi.python.org/pypi/pyttsx
	c.	PyQt4
		http://www.riverbankcomputing.com/software/pyqt/download
		Remember to download Python 2.7 version
2.	Double click timeTracker.pyw to start the program 
3.	Click the system tray icon to make changes 
4.	If you will like it to run on startup, copy the content of src to the directory 
	C:\Users\<name>\AppData\Roaming\Microsoft\Windows\StartMenu\Programs\Startup

TODO:
1.	Make a standalone installer for windows and mac os 
2.	Recurring reminders 

If you have any feedback question or contractive criticism or a bug email me at otengKwaku@gmail.com 

