#!/usr/bin/env python

"""
Download-It
Author : Mahesh S.R
Email : mahepj94@gmail.com
"""

from bs4 import BeautifulSoup
from PyQt4 import QtGui
import requests
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

        grid.addWidget(self.okButton, 3, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Download-It')    
        self.show()
    	
    def start_download(self):
    	newpid = os.fork()
	if newpid != 0:
		self.okButton.setText("Cancel Download")
	else:
		self.download()
        
    def download(self):
    
    	url = str(self.urlEdit.displayText())
    	album = str(self.albumEdit.displayText())
        
        base_url = "http://www.gamethemesongs.com/"


	if("http://" not in url):
		r  = requests.get("http://" + url)
	else:
		r  = requests.get(url)

	data = r.text
	soup = BeautifulSoup(data, "lxml")

	album_folder = re.escape(album)

	os.system("mkdir " + album_folder)

	for sound in soup.find_all('a'):
		if(album in sound.get_text()):		
			r  = requests.get(sound.get("href"))
		
			new_data = r.text
			new_soup = BeautifulSoup(new_data, "lxml")
		
			download_link = new_soup.find_all("a", "download")[0].get("href")
		
			file_name = download_link.replace("download.php?f=", "")
		
			os.system("wget -O " + album_folder + "/" + file_name + " " + base_url + download_link)
		


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

