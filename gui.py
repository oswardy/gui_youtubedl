import re #Using regular expressions to check valid YouTube URLs
import sys #Exit functions
import os #Current directory
import subprocess #Call system process
import requests #Verify YouTube URL link
import easygui as ez #ez
import youtube_dl #module to download app

#Define download format
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

def getUserInput():
	#Get user input
	url = ez.enterbox("Please enter a YouTube URL\n(Eg. https://www.youtube.com/watch?v=TPqTDtKiTIE)", "YouTube_dl GUI")
	'''
	1. First check: Check whether URL is null
	2. Second check: Check whether it's a valid YouTube URL
	3. Third check: Using requests library to send a HEAD request to check whether response code returns 200 OK
	'''
	if (url) and re.match("^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$", str(url)):
		r = requests.head(str(url))
		if r.status_code == 200:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				meta = ydl.extract_info(str(url), download=False)
				if ez.ccbox("Title: " + str(meta['title']) + "\nDuration: " + str(meta['duration']) + " seconds\nProceed to download?", "YouTube_dl GUI"):
						return url
				else: 
					sys.exit(0)
		else:
			ez.msgbox("This video doesn't exist, please try with another video")
			sys.exit(0)
	else:
		ez.msgbox("Sorry, the URL you input is invalid, please try with another URL", "YouTube_dl GUI")
		sys.exit(0)

def download_MP3(url):
	#Downloads the video URL as mp3 and save in current file destination
	subprocess.call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3',url], shell=True)
	ez.msgbox("Success! File is saved in " + os.getcwd(), "YouTube_dl GUI")

def download_mkv(url):
	#I gave up finding the option to trigger mkv file download
	subprocess.call(['youtube-dl', '--format', "bestvideo+bestaudio[ext=m4a]/bestvideo+bestaudio/best", url], shell=True)
	ez.msgbox("Success! File is saved in " + os.getcwd(), "YouTube_dl GUI")		

def main():
	repeat = True
	while repeat == True:
		do_what = ez.indexbox("Welcome to YouTube dl GUI!\nWhat would you like to do today?", "YouTube_dl GUI", choices=("Download MP3", "Download video", "Exit"))
		if do_what == 0:
			url = getUserInput()
			download_MP3(url)
		elif do_what == 1:
			url = getUserInput()
			download_mkv(url)
		else:
			sys.exit(0)
		repeat = ez.boolbox("Do you wish to start again?", "YouTube_dl GUI", ("Yes", "No"))
  
if __name__== "__main__":
  main()
