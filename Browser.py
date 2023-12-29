'''
                    MIT License

            Copyright (c) 2023 Nandhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

                Creator: Nandhan K
                Github: @github.com/Nandhan-KA
'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class BrowserTab(QWebEngineView):
    def __init__(self):
        super(BrowserTab, self).__init__()
        self.setUrl(QUrl('http://google.com'))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # navbar
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Only one QLineEdit for url_bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        self.add_new_tab(QUrl('http://google.com'), 'Homepage')
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.current_browser.back)
        self.navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.current_browser.forward)
        self.navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.current_browser.reload)
        self.navbar.addAction(reload_btn)

        stop_btn = QAction('Stop', self)
        stop_btn.triggered.connect(self.current_browser.stop)
        self.navbar.addAction(stop_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        self.navbar.addAction(new_tab_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.progress_bar.setValue(0)
        self.navbar.addWidget(self.progress_bar)

        # Initialize the current_browser attribute
        self.current_browser = self.tabs.currentWidget()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://google.com')
        elif isinstance(qurl, str):  # Check if qurl is a string
            qurl = QUrl.fromUserInput(qurl)

        browser = BrowserTab()
        if isinstance(qurl, QUrl):
            browser.setUrl(qurl)
        else:
            browser.setUrl(QUrl('http://google.com'))

        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))
        browser.loadProgress.connect(self.update_progress)
        browser.titleChanged.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
        # Update the current_browser attribute
        self.current_browser = self.tabs.currentWidget()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - Python Browser" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_progress(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.progress_bar.setMaximum(browser.page().totalBytes())
        self.progress_bar.setValue(q)


app = QApplication(sys.argv)
QApplication.setApplicationName('Tabbed Browser')
window = MainWindow()
window.showMaximized()
app.exec_()
