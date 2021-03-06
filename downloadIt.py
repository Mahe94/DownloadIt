#!/usr/bin/env python

"""
Download-It
Author : Mahesh S.R
Email : mahepj94@gmail.com
"""

from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
from PyQt4 import QtGui, QtCore
import urllib
import requests
import signal
import sys
import os
import re

base_url = "http://www.gamethemesongs.com/"

class DownloadThread(QtCore.QThread):
        def __init__(self,  url = "", album = "", parent = None):
                QtCore.QThread.__init__(self, parent)
                self.url = url
                self.album = album
                
       	def __del__(self):
  		self.wait()
 
        def run(self):
        
        	message = "Download will start in a moment"
        	self.emit( QtCore.SIGNAL('update(QString)'), message )

		if("http://" not in self.url):
			r  = requests.get("http://" + self.url)
		else:
			r  = requests.get(self.url)

		data = r.text
		soup = BeautifulSoup(data, "lxml")

		album_folder = re.escape(self.album)

		if not(os.path.isdir(self.album)):
			os.system("mkdir " + album_folder)
	
		for sound in soup.find_all('a'):
			if(self.album in sound.get_text()):		
				r  = requests.get(sound.get("href"))
		
				new_data = r.text
				new_soup = BeautifulSoup(new_data, "lxml")
		
				download_link = new_soup.find_all("a", "download")[0].get("href")
		
				file_name = download_link.replace("download.php?f=", "")
				
				self.emit( QtCore.SIGNAL('update(QString)'), "Downloading: " + file_name )
				
				urllib.urlretrieve(base_url + download_link, filename = self.album + "/" + file_name)
				'''
				os.system("wget -O " + album_folder + "/" + file_name + " " + base_url + download_link)
				'''
				
		self.emit( QtCore.SIGNAL('finish()'))
		                

class DownloadIt(QtGui.QWidget):
    
    def __init__(self):
        super(DownloadIt, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        url = QtGui.QLabel('Website')
        album = QtGui.QLabel('Album')
        
        self.downloadThread = DownloadThread()
	self.connect( self.downloadThread, QtCore.SIGNAL("update(QString)"), self.add )
	self.connect( self.downloadThread, QtCore.SIGNAL("finish()"), self.download_completed )
        
        self.listwidget = QtGui.QListWidget(self)
        
        self.okButton = QtGui.QPushButton("OK")
        self.okButton.clicked.connect(self.start_download)
        
        self.urlEdit = QtGui.QLineEdit()
        self.albumEdit = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(url, 1, 0)
        grid.addWidget(self.urlEdit, 1, 1)

        grid.addWidget(album, 2, 0)
        grid.addWidget(self.albumEdit, 2, 1)

	grid.addWidget(self.listwidget, 3, 1)
	
        grid.addWidget(self.okButton, 4, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Download-It')    
        self.show()
    	
    def start_download(self):  
    	self.listwidget.clear()
    	 
    	url = str(self.urlEdit.displayText())
    	album = str(self.albumEdit.displayText())
    	
    	if(base_url not in url):
    		self.add("Enter a valid site from " + base_url)
    		return
    		
    	if(not(album)):
    		self.add("Enter a name")
    		return
	
	self.downloadThread.url = url
	self.downloadThread.album = album
        self.downloadThread.start()
	
	self.okButton.setText("Cancel Download")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.cancel_download)
	
    def add(self, text):
    	self.listwidget.addItem(text)
	
	
    def download_completed(self):
    
    	self.listwidget.addItem("Download Completed")
    		
	self.okButton.setText("OK")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.start_download)
	
		
    def cancel_download(self):
    	self.downloadThread.terminate()
    	
    	self.listwidget.addItem("Download Cancelled")
    	
	self.okButton.setText("OK")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.start_download)
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DownloadIt()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

