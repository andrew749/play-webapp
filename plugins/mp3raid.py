import  imports
url="http://www.mp3raid.ca/download/"
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
def getMP3RaidSongs(songName):
    end=songName.replace(" ","_")+".html"
    concaturl=url+end
    page=requests.get(concaturl,headers=header)
    tree=html.fromstring(page.text)
    elements=tree.xpath("//*[@class='index1']//a[@class='dl']")
    songArray=[]
    for song in elements:
        nexturl="http://www.mp3raid.ca/search/ddl/"+song.xpath("@id")[0]+"/"+end
        page2=requests.get(nexturl,headers=header)
        tree2=html.fromstring(page2.text)
        songName=tree2.xpath("//table/tr/*[2]/text()")[0]
        #print(songName)
        songURL=tree2.xpath("//table/tr/*[2]/text()")[1]
        #print(songURL)
        songArray.append({songName:songURL})
    return songArray