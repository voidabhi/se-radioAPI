

"""
	Python script for downloading latest podcast from http://se-radio.net and saving it to local directory.
"""

import os
import requests
from bs4 import BeautifulSoup

from constants import BASE_URL , DOWNLOAD_DIRECTORY

def get_podcast_links():
	"""
		Returns links of latest podcast in a list.
	"""
	r = requests.get(BASE_URL)
	soup = BeautifulSoup(r.text)
	anchors =  soup.find_all("a",{"class":"more-link","rel":"nofollow"})
	links = list()
	for link in anchors:
		links.append(link["href"])
	return links
	
def get_download_link(podcast_link):
	"""
		Returns podcast download link for a given podcast  link
	"""
	r = requests.get(podcast_link)
	soup = BeautifulSoup(r.text)
	download_anchor = soup.find_all("a",{"title":"Download"})
	download_link = download_anchor[0]["href"]
	return download_link
	
def download_file(url,filepath):
	"""
		Downloads file of given url at given filepath
	"""
	if os.path.exists(filepath):
		return
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(filepath, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()	
				
def show_counter():
	import time,sys
	for i in range(100):
		time.sleep(1)
		sys.stdout.write("\r%d%%" %i)
		sys.stdout.flush()

# fetching podcast links
print("Fetching podcast links...")
links = get_podcast_links()
print("Podcast links fetched...")

# fetching download link for each podcast and storing in dictionary with title
print("Fetching podcasts download links...")
podcasts = []
for link in links:
	download_link = get_download_link(link)
	title = link.split("/")[len(link.split("/"))-2]
	podcasts.append({"title":title,"download_link":download_link})
print("Podcast Download links fetched...")

# storing file at given download link in directory with name of title for each pocast
print("Making Directories...")
for podcast in podcasts:
	if  not os.path.exists(DOWNLOAD_DIRECTORY+podcast["title"]):
		os.makedirs(DOWNLOAD_DIRECTORY+podcast["title"])
print("Directories built...")

# downloading file into the directories
for podcast in podcasts:
	filepath = DOWNLOAD_DIRECTORY+podcast["title"]+"/"+podcast["download_link"].split("/")[-1]
	download_file(podcast["download_link"],filepath)
