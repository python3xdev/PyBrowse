import os
import sys
import time
from datetime import datetime
# from win10toast import ToastNotifier

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

#importing the calculator
from calculator import calculator

class AboutDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(AboutDialog, self).__init__(*args, **kwargs)

		QBtn = QDialogButtonBox.Ok  # No cancel
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.setWindowTitle("About PyBrowse™")

		layout = QVBoxLayout()

		title = QLabel("PyBrowse™")
		font = title.font()
		font.setPointSize(20)
		title.setFont(font)
		layout.addWidget(title)


		logo = QLabel()
		logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
		layout.addWidget(logo)


		version = QLabel("Version 4.1 (Official Build)")
		font = version.font()
		font.setPointSize(13)
		version.setFont(font)
		layout.addWidget(version)

		layout.addWidget(QLabel(f"All Rights Reserved 2021-{datetime.now().year} PyBrowse™"))
		for i in range(0, layout.count()):
			layout.itemAt(i).setAlignment(Qt.AlignHCenter)

		layout.addWidget(self.buttonBox)

		self.setLayout(layout)
		self.setFixedWidth(220)


# main window
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		#self.setWindowFlags(Qt.FramelessWindowHint)

		width = 600
		height = 400
  
		# setting the minimum size 
		self.setMinimumSize(width, height)

		# on open, the software will be Maximized
		self.showMaximized()

		#start the webview
		self.browser = QWebEngineView()

		# creating a tab widget
		self.tabs = QTabWidget()

		# making document mode true
		self.tabs.setDocumentMode(True)

		# adding action when double clicked
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

		# adding action when tab is changed
		self.tabs.currentChanged.connect(self.current_tab_changed)

		# making tabs closeable
		self.tabs.setTabsClosable(True)

		# making the tabs movable
		self.tabs.tabBar().setMovable(True)

		# adding action when tab close is requested
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		# making tabs as central widget
		self.setCentralWidget(self.tabs)


		# creating a status bar
		self.status = QStatusBar()

		# setting status bar to the main window
		self.setStatusBar(self.status)

		self.statusBar().setStyleSheet("background-color: rgb(34, 34, 34); color: white;") 

		# creating a tool bar for navigation
		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(18, 18))

		# adding tool bar to the main window
		self.addToolBar(navtb)

		back_btn = QAction(QIcon(os.path.join('images', 'left-arrow.png')), "Go Back To The Previos Page", self)
		back_btn.setStatusTip("Go Back To The Previos Page")
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		# similarly adding next button
		next_btn = QAction(QIcon(os.path.join('images', 'right-arrow.png')), "Go Forward To The Next Page", self)
		next_btn.setStatusTip("Go Forward To The Next Page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		# similarly adding reload button
		reload_btn = QAction(QIcon(os.path.join('images', 'refresh180.png')), "Reload The Current Page", self)
		reload_btn.setStatusTip("Reload The Current Page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		# creating home action
		home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "PyBrowse™ Homepage", self)
		home_btn.setStatusTip("PyBrowse™ Homepage")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		# adding a separator
		navtb.addSeparator()

		#ssl check
		self.httpsicon = QLabel()
		self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'padlock_unsecure.png')))
		navtb.addWidget(self.httpsicon)

		# creating a line edit widget for URL
		self.urlbar = QLineEdit()

		self.urlbar.setStyleSheet("margin-left: 5px; margin-right: 5px; border: 1px solid black; height: 22px; font: 14px; border-radius: 2px; padding-left: 5px; padding-right: 5px;")

		self.urlbar.setPlaceholderText("Type/Paste In An Address...")


		#CHANGES THE SIZE OF THE URL BAR
		#self.urlbar.setFixedWidth(400)


		# lets you click and drag text or a link up to the urlbar
		self.urlbar.setDragEnabled(True)

		# adding action to line edit when return key is pressed
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding line edit to tool bar
		navtb.addWidget(self.urlbar)

		# creating the progress bar to display page loads
		self.page_load_progress_bar = QProgressBar()

		self.page_load_progress_bar.setStatusTip("Displays how much of the current page has loaded.")

		# adding styling to the progress bar
		self.page_load_progress_bar.setStyleSheet("margin-right: 5px; max-width: 100px; font: 14px; text-align: center; border: 1px solid black; height: 22px;")

		# adding the progress bar to the navtb
		navtb.addWidget(self.page_load_progress_bar)

		#add new tab button   # method for adding new tab
		new_tab_btn = QAction(QIcon(os.path.join('images', 'plus.png')), "Create A New Tab", self)
		new_tab_btn.setStatusTip("Create A New Tab")
		new_tab_btn.triggered.connect(lambda: self.add_new_tab())
		navtb.addAction(new_tab_btn)

		#divider
		navtb.addSeparator()

		clear_btn = QAction(QIcon(os.path.join('images', 'eraser.png')), "Clear The Address/URL Bar", self)
		clear_btn.setStatusTip("Clear The Address/URL Bar")
		clear_btn.triggered.connect(lambda: self.urlbar.clear())
		navtb.addAction(clear_btn)

		# similarly adding stop action
		stop_btn = QAction(QIcon(os.path.join('images', 'cross_circle_bold.png')), "Stop Loading Current Page", self)
		stop_btn.setStatusTip("Stop Loading Current Page")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		# this a a variable that holds the file path for the default page for every new tab
		default_page_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "default_search_page/search.html"))

		# creating first tab
		self.add_new_tab(QUrl.fromLocalFile(default_page_path), 'Homepage')

		# showing all the components
		self.show()

		#window icon
		self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

		# setting window title
		self.setWindowTitle("PyBrowse™")

#---------------------------------------------------------MENU BAR---------------------------------------------------------------------#
		menubar = self.menuBar()
#-----------------------------------------------------------FILE-----------------------------------------------------------------------#
		
		fileMenu = menubar.addMenu('&File')

		open_new_tab = QAction(QIcon(os.path.join('images','plus.png')), "New Tab", self)
		open_new_tab.setShortcut('Ctrl+T')
		open_new_tab.setStatusTip("Open A New Tab")
		open_new_tab.triggered.connect(lambda: self.add_new_tab())
		fileMenu.addAction(open_new_tab)


		reload_btn_action = QAction(QIcon(os.path.join('images', 'refresh180.png')), "Reload", self)
		reload_btn_action.setStatusTip("Reload Current Page")
		reload_btn_action.setShortcut('F5')
		reload_btn_action.triggered.connect(lambda: self.tabs.currentWidget().reload())
		fileMenu.addAction(reload_btn_action)


		# home_action = QAction(QIcon(os.path.join('images', 'home.png')), "PyBrowse™ Homeage", self)
		# home_action.setStatusTip("PyBrowse™ Homepage")
		# home_action.setShortcut('Alt+Home')
		# home_action.triggered.connect(self.navigate_home)
		# fileMenu.addAction(home_action)

		fileMenu.addSeparator()

		open_file_action = QAction(QIcon(os.path.join('images','open.png')), "Open File...", self)
		open_file_action.setShortcut('Ctrl+O')
		open_file_action.setStatusTip("Open from file")
		open_file_action.triggered.connect(lambda: self.open_file())
		fileMenu.addAction(open_file_action)


		save_file_action = QAction(QIcon(os.path.join('images','save_as.png')), "Save Page As...", self)
		save_file_action.setShortcut('Ctrl+S')
		save_file_action.setStatusTip("Save current page to file")
		save_file_action.triggered.connect(lambda: self.save_file())
		fileMenu.addAction(save_file_action)

		fileMenu.addSeparator()

		exitAct = QAction(QIcon(os.path.join('images', 'exit.png')), '&Exit', self)
		exitAct.setShortcut('Ctrl+Shift+Q')
		exitAct.setStatusTip('Exit Application')
		exitAct.triggered.connect(qApp.quit)
		fileMenu.addAction(exitAct)

#-----------------------------------------------------------EDIT-----------------------------------------------------------------------#
		
		editMenu = menubar.addMenu('&Edit')


#-----------------------------------------------------------VIEW-----------------------------------------------------------------------#

		viewMenu = menubar.addMenu('&View')

		viewStatAct = QAction('View Statusbar', self, checkable=True)
		viewStatAct.setStatusTip('View Statusbar')
		viewStatAct.setChecked(True)
		viewStatAct.triggered.connect(self.toggleStatusBar)
		viewMenu.addAction(viewStatAct)

#-----------------------------------------------------------TOOLS----------------------------------------------------------------------#

		toolsMenu = menubar.addMenu('&Tools')

		toolsCalculator = QAction(QIcon(os.path.join('images', 'calculator.png')), "Calculator", self)
		toolsCalculator.setShortcut('Ctrl+Shift+C')
		toolsCalculator.setStatusTip("Use The Built In Calculator.")
		toolsCalculator.triggered.connect(lambda: self.calculator_tool())
		toolsMenu.addAction(toolsCalculator)

#-----------------------------------------------------------HELP-----------------------------------------------------------------------#
		
		helpMenu = menubar.addMenu('&Help')

		# visit PyBrowse™ Homepage
		pybrowse_btn = QAction(QIcon(os.path.join('images', 'icon.png')), "PyBrowse™ Website", self)
		pybrowse_btn.setStatusTip("PyBrowse™ Website")
		pybrowse_btn.triggered.connect(self.navigate_pybrowse)
		helpMenu.addAction(pybrowse_btn)


		# ABOUT (run the about class)
		about_btn = QAction(QIcon(os.path.join('images', 'question.png')), "About PyBrowse™", self)
		about_btn.setStatusTip("About PyBrowse™")
		about_btn.triggered.connect(lambda: self.about())
		helpMenu.addAction(about_btn)


#--------------------------------------------------------------------------------------------------------------------------------------#

	# def notification(self):
	# 	toaster = ToastNotifier()

	# 	toaster.show_toast("PyBrowse", "Loading finished. Happy browsing!", threaded=True, icon_path='images/icon.ico', duration=3)

	# 	while toaster.notification_active():
	# 		time.sleep(0.1)

	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
						"Hypertext Markup Language (*.htm *.html);;"
						"All files (*.*)")

		if filename:
			with open(filename, 'r', encoding = 'utf-8') as f:
				html = f.read()

			self.browser.setHtml(html)
			self.urlbar.setText(filename)
			self.navigate_to_url()

	def save_file(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
				"Hypertext Markup Language (*.htm *html);;"
				"All files (*.*)")

		if filename:
			html = self.browser.page().toHtml()
			with open(filename, 'w') as f:
				f.write(html)


	def add_new_tab(self, qurl=None, label="Loading..."):

		# if url is blank
		if qurl is None:
			# creating a duckduckgo url
			qurl = QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "default_search_page/search.html")))

			# creating a QWebEngineView object
		browser = QWebEngineView()

		# setting url to browser
		browser.setUrl(qurl)

		# setting tab index
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		# adding action to the browser when url is changed
		# update the url
		browser.urlChanged.connect(lambda qurl, browser=browser:
								   self.update_urlbar(qurl, browser))

		# adding action to the browser when loading is finished
		# set the tab title
		browser.loadFinished.connect(lambda _, i=i, browser=browser:
									 self.tabs.setTabText(i, browser.page().title()[:30] + "..." if len(browser.page().title()) >= 30 else browser.page().title())) # make 30 character tab text length

		browser.iconChanged.connect(lambda: self.update_favicon())

		browser.loadProgress.connect(self.update_progress_bar)

		# send the user a notification that PyBrowse™ has finished loading !!!DOES NOT WORK!!!
		# browser.loadFinished.connect(lambda: self.notification())

	def update_progress_bar(self, prog):
		self.page_load_progress_bar.setValue(prog)

	def tab_open_doubleclick(self, i):

		# checking index i.e
		# No tab under the click
		if i == -1:
			# creating a new tab
			self.add_new_tab()

			# wen tab is changed

	def current_tab_changed(self, i):

		# get the curl
		if self.tabs.count() >= 1:
			qurl = self.tabs.currentWidget().url()

		# update the url
			self.update_urlbar(qurl, self.tabs.currentWidget())

		# update the title
			self.update_title(self.tabs.currentWidget())

		# update the favicon
			self.update_favicon()




	def close_current_tab(self, i):

		# if there is only one tab
		if self.tabs.count() < 2:
			# do nothing
			window.close()

		# else remove the tab
		self.tabs.removeTab(i)

		# method for updating the title

	def update_title(self, browser):

		# if signal is not from the current tab
		if browser != self.tabs.currentWidget():
			# do nothing
			return

		# get the page title
		title = self.tabs.currentWidget().page().title()

		# set the window title
		self.setWindowTitle("% s - PyBrowse™" % title)

	def update_favicon(self):

		# load the favicon
		q = QUrl(self.urlbar.text())

		if q == QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "default_search_page/search.html"))):
			tab_index = self.tabs.currentIndex()
			self.tabs.setTabIcon(tab_index, QIcon('images/icon.png'))
			self.tabs.setIconSize(QSize(20, 20))

		elif q.scheme() == 'file': #if it is a computer file then the favicon will be the default file.png
			tab_index = self.tabs.currentIndex()
			self.tabs.setTabIcon(tab_index, QIcon('images/file.png'))
			self.tabs.setIconSize(QSize(20, 20))

		else: 
			icon = self.tabs.currentWidget().page().icon()
			tab_index = self.tabs.currentIndex()
			self.tabs.setTabIcon(tab_index, QIcon(icon))
			self.tabs.setIconSize(QSize(20, 20))



	def navigate_pybrowse(self):
		#self.tabs.currentWidget().setUrl(QUrl("http://pybrowse.com")) ----- This line of code opens pybrowse.com in the current tab that the user is on.
		self.add_new_tab(QUrl('http://pybrowse.com')) # ----- This line of code opens a new tab for pybrowse.com.

	def about(self):
		dlg = AboutDialog()
		dlg.exec_()

	def calculator_tool(self):
		calculator.main()

	def navigate_home(self):

		# go to PyBrowse search page
		self.tabs.currentWidget().setUrl(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "default_search_page/search.html"))))

		# method for navigate to url

	def navigate_to_url(self):

		# get the line edit text
		# convert it to QUrl object
		q = QUrl(self.urlbar.text())

		# if scheme is blank
		if q.scheme() == "":
			# set scheme
			q.setScheme("http")

			# set the url
		self.tabs.currentWidget().setUrl(q)

		# method to update the url

	def update_urlbar(self, q, browser=None):

		if q.scheme() == 'https':
			# Secure padlock icon
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'padlock_secure.png')))
			self.httpsicon.setStatusTip("Secure Website")

		elif q.scheme() == 'file':
			# Secure padlock icon
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'file.png')))
			self.httpsicon.setStatusTip("This Page Is Located On Your Computer.")
		else:
			# Insecure padlock icon
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'padlock_unsecure.png')))
			self.httpsicon.setStatusTip("Insecure Website")

		self.httpsicon.setStyleSheet("margin-left: 5px;")

		# If this signal is not from the current tab, ignore
		if browser != self.tabs.currentWidget():
			return

		# set text to the url bar
		self.urlbar.setText(q.toString())

		# set cursor position
		self.urlbar.setCursorPosition(0)

	def toggleStatusBar(self, state):
		if state:
			self.status.show()
		else:
			self.status.hide()


app = QApplication(sys.argv)
app.setApplicationName("PyBrowse™")
app.setOrganizationName("PyBrowse™")
app.setOrganizationDomain("pybrowse.com")

window = MainWindow()

app.setStyleSheet("""

QTabBar::close-button{
background-image:url('images/close_current_tab.png')
}

QTabBar::close-button:!selected{
background-image:url('images/close_other_tab.png');
}


QTabWidget::pane {
	border: 1px solid black;
	background: white;
}

QTabWidget::tab-bar:top {
	top: 1px;
}

QTabWidget::tab-bar:bottom {
	bottom: 1px;
}

QTabWidget::tab-bar:left {
	right: 1px;
}

QTabWidget::tab-bar:right {
	left: 1px;
}

QTabBar::tab {
	border: 1px solid black;
}

QTabBar::tab:selected {
	background: #ffffff;
	border-color: #ffffff;
	border-bottom-color: #C2C7CB;
	border-top-color: #e82d02;
}

QTabBar::tab:!selected {
	background: silver;
}

QTabBar::tab:!selected:hover {
	background: #e1e1e1;
	border-top-color: #02a1fb
}

QTabBar::tab:top:!selected {
	margin-top: 3px;
}

QTabBar::tab:bottom:!selected {
	margin-bottom: 3px;
}

QTabBar::tab:top, QTabBar::tab:bottom {
	min-width: 8ex;
	margin-right: -1px;
	padding: 5px 10px 5px 10px;
}

QTabBar::tab:top:selected {
	border-bottom-color: none;
}

QTabBar::tab:bottom:selected {
	border-top-color: none;
}

QTabBar::tab:top:last, QTabBar::tab:bottom:last,
QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
	margin-right: 0;
}

QTabBar::tab:left:!selected {
	margin-right: 3px;
}

QTabBar::tab:right:!selected {
	margin-left: 3px;
}

QTabBar::tab:left, QTabBar::tab:right {
	min-height: 8ex;
	margin-bottom: -1px;
	padding: 10px 5px 10px 5px;
}

QTabBar::tab:left:selected {
	border-left-color: none;
}

QTabBar::tab:right:selected {
	border-right-color: none;
}

QTabBar::tab:left:last, QTabBar::tab:right:last,
QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
	margin-bottom: 0;
}
	""")

app.exec_()