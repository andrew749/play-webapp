import requests
url="http://beemp3s.org/index.php?q="
def getSongs(songName):
    concaturl=url+songName.replace(" ","+")



