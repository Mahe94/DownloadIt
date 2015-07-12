#!/usr/bin/env python

"""
Download-It
Author : Mahesh S.R
Email : mahepj94@gmail.com
"""

from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
from PyQt4 import QtGui
import urllib
import requests
import signal
import sys
import os
import re

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        url = QtGui.QLabel('Website')
        album = QtGui.QLabel('Album')
        
        self.result = QtGui.QLabel(self)
        
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

	grid.addWidget(self.result, 3, 1)
	
        grid.addWidget(self.okButton, 4, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Download-It')    
        self.show()
    	
    def start_download(self):
    
    	
	self.p = Process(target=self.download, args=())
	self.p.start()
	
	self.okButton.setText("Cancel Download")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.cancel_download)
	
	self.p.join()
		
	self.result.setText("Downloading complete")
		
	self.okButton.setText("OK")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.start_download)
	
		
    def cancel_download(self):
    	os.kill(self.p.pid, signal.SIGKILL)
    	
    	self.result.setText("Cancelled")
    	
	self.okButton.setText("OK")
	self.okButton.clicked.disconnect()
	self.okButton.clicked.connect(self.start_download)
        
    def download(self):
    	'''    
    	url = str(self.urlEdit.displayText())
    	album = str(self.albumEdit.displayText())
	'''

	url = "http://www.gamethemesongs.com/a-theme-songs.html"
	album = "Assassins Creed Unity"
	        
        base_url = "http://www.gamethemesongs.com/"

	if("http://" not in url):
		r  = requests.get("http://" + url)
	else:
		r  = requests.get(url)

	data = r.text
	soup = BeautifulSoup(data, "lxml")

	album_folder = re.escape(album)

	if not(os.path.isdir(album)):
		os.system("mkdir " + album_folder)
	
	for sound in soup.find_all('a'):
		if(album in sound.get_text()):		
			r  = requests.get(sound.get("href"))
		
			new_data = r.text
			new_soup = BeautifulSoup(new_data, "lxml")
		
			download_link = new_soup.find_all("a", "download")[0].get("href")
		
			file_name = download_link.replace("download.php?f=", "")
			
			urllib.urlretrieve(base_url + download_link, filename = album + "/" + file_name)
			'''
			os.system("wget -O " + album_folder + "/" + file_name + " " + base_url + download_link)
			'''
			break
	
		


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

