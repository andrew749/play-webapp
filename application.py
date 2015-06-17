from flask import Flask, url_for, request, render_template
import requests
from lxml import html
import lxml
import json
from lxml import etree
from Song import *
from urllib.parse import quote
import pdb
from urllib.request import urlopen,Request
import mp3skull
import DownloadNL
import YouTube
import mp3raid
import time
import _thread
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
savedSearches=[]
#topHits=[]
app=Flask(__name__)
#Seaches the site and returns an array of linksmum
#TODO implement groove shark
#TODO implement goear
#TODO implement yourlisten
#method to search local datastore and see if there is a verified link
def getVerifiedLinks(songName):
    return False;
class SearchResult:
    def __init__(self, name="unknown",songs=None):
        self.name=name
        self.songs=songs
"""
This function get the top 100 list from iTunes.
"""
def getTopHits():
    url="https://itunes.apple.com/us/rss/topsongs/limit=100/xml"
    namespaces={'im':'http://itunes.apple.com/rss','xmlns':"http://www.w3.org/2005/Atom"}
    data={}
    try:
        with open('hits','r') as f:
            data=json.loads(f.read())
        if(time.time()*1000-data['time']<86400000):
            return JsonToSongs(data['data'])
    except Exception:
        pass
    songArray=[]
    page=requests.get(url,headers=header)
    tree=etree.fromstring(page.content)
    for x in tree.findall('xmlns:entry',namespaces):
        s=Song(x.find('im:name',namespaces).text)
        s.setArtist(x.find('im:artist',namespaces).text)
        s.setAlbumArtURL(x.find('im:image[@height="170"]',namespaces).text)
        songArray.append(s)
    f=open('hits','w')
    json.dump({'time':int(time.time()*1000),'data':allSongsToJson(songArray)},f)
    topHits=songArray
    return songArray
@app.route('/top')
def getTop():
    elements=getTopHits()
    return (allSongsToJson(elements))

@app.route('/landing')
def serveLanding():
    return render_template('landingpage.html')

@app.route('/')
def serveGUI():
    elements=getTopHits()
    return render_template('index.html',elements=elements)

@app.route('/search')
def searchForSongs():
    name = request.args.get('songname')
    return search(name)
def search(name):
    name.replace("'","\'");
    links=[]
    for x in savedSearches:
        if(x.name==name):
            print("getting cached result")
            return allSongsToJson(x.songs)
    links_mp3skull=mp3skull.searchMP3Skull(name)
    links_downloadnl=DownloadNL.searchDownloadNL(name)
    links_mp3raid=mp3raid.getMP3RaidSongs(name)
    if(links_mp3skull is not None):
        links+=links_mp3skull
    if(links_downloadnl is not None):
        links+=links_downloadnl
    if(links_mp3raid is not None):
        links+=links_mp3raid
    if(links is None):
        links_youtube=YouTube.searchYouTube(name)
        links+=links_youtube
    savedSearches.append(SearchResult(name,links))
    print ("done searching for ",name)
    return (allSongsToJson(links))
@app.route('/callback')
def handleCallback():
    pdb.set_trace()
#download data for all of the sources

def initialize():
    topHits=getTopHits()
    i=0
    for x in topHits:
        print("Searching for ",x.title)
        #_thread.start_new_thread(search,(x.title,))
        search(x.title+" "+x.artist)
        if i==10:
            break
        else:
            i+=1
if __name__ == '__main__':
    _thread.start_new_thread(initialize,())
    app.run(debug=True)
