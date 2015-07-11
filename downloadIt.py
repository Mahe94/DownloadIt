from bs4 import BeautifulSoup
import requests
import os
import re

base_url = "http://www.gamethemesongs.com/"

url = raw_input("Enter a website to extract the URL's from:")

if("http://" not in url):
	r  = requests.get("http://" + url)
else:
	r  = requests.get(url)

data = r.text
soup = BeautifulSoup(data, "lxml")

album = raw_input("Enter the name of the game:")

album_folder = re.escape(album)

os.system("mkdir " + album_folder)

for sound in soup.find_all('a'):
	if(album in sound.get_text()):		
		r  = requests.get(sound.get("href"))
		
		new_data = r.text
		new_soup = BeautifulSoup(new_data, "lxml")
		
		download_link = new_soup.find_all("a", "download")[0].get("href")
		
		file_name = download_link.replace("download.php?f=", "")
		
		print(file_name)
		
		os.system("wget -O " + album_folder + "/" + file_name + " " + base_url + download_link)
		
print("------------COMPLETED-----------")

