from __future__ import unicode_literals #encoding issues
import re #Using regular expressions to check valid YouTube URLs
import sys #Exit functions
import os #Current directory
import subprocess #Call system process

try:
	import requests #Verify YouTube URL link
	import easygui as ez #ez
	import youtube_dl #module to download app
except ImportError:
	for req in ["requests", "easygui", "youtube_dl"]:
		subprocess.call([sys.executable, '-m', 'pip', 'install', req])

'''
requirements.txt contents
requests
easygui
youtube_dl
'''

#Define download format
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

ez.msgbox("Welcome to YouTube dl GUI!")

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
			if ez.ccbox("Title: " + str(meta['title']) + "\nDuration: " + str(meta['duration']) + " seconds\nProceed to download?", "GUI Dl"):
					pass
			else: 
				sys.exit(0)
	else:
		ez.msgbox("This video doesn't exist, please try with another video")
		sys.exit(0)
else:
	ez.msgbox("Sorry, the URL you input is invalid, please try with another URL", "YouTube_dl GUI")
	sys.exit(0)

#Downloads the video URL as mp3 and save in current file destination
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	meta = ydl.extract_info(str(url), download=True)
	ez.msgbox("Success! File is saved in " + os.getcwd(), "YouTube_dl GUI")

'''
TODO
1. Download mp4 function
2. Save in chosen directory

References 
https://stackoverflow.com/questions/22188128/how-to-gather-string-form-easygui-enterbox
http://easygui.sourceforge.net/tutorial.html#using-buttonboxes
https://stackoverflow.com/questions/19377262/regex-for-youtube-url
https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
https://stackoverflow.com/questions/44210656/how-to-check-if-a-module-is-installed-in-python-and-if-not-install-it-within-t
'''
