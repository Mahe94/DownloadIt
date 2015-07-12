# DownloadIt
Python script to download the complete audio files of any game present in http://www.gamethemesongs.com. This script is intented for Linux only.  

## Installation
Open the folder containing the downloadIt.py script. Open terminal and type the following command  
```
chmod +x downloadIt.py
```
This is to make the script executable.  

To run this script, simply type
```
./downloadIt.py
```

## How to use
Go to http://www.gamethemesongs.com. Choose the starting letter of the game. Copy the link address of this page and paste it into the edittext field Website.  
Copy the name of game from the list and paste it into the edittext field Album.  
Then press OK

## Troubleshoot
You require python to run this script.:P
```
sudo apt-get update
sudo apt-get install python2.7
```  

You may require to run these command if the script is not working properly
```
sudo apt-get install python-qt4 pyqt4-dev-tools
```
