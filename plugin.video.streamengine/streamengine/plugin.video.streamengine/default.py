import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,base64,random,shutil
import datetime
import time
import urlresolver
from addon.common.addon import Addon
from threading import Timer
import json

PLUGIN = 'plugin.video.streamengine'
ADDON = xbmcaddon.Addon(id=PLUGIN)
ART = xbmc.translatePath(os.path.join('special://home/addons/' + PLUGIN + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + PLUGIN, 'icon.png'))
addon = Addon(PLUGIN, sys.argv)
baseurl = 'http://www.listenlive.eu'
############################################################################################################################
### ID LIKE TO SAY THAT THIS ADDON WOULD NOT OF BEEN POSSIBLE IF IT WASNT FOR THE WORK ALREADY DONE BY OTHER DEVELOPERS  ###
###     WITHOUT OUT THE GUIDE OF THEIR WORK TO HELP ME UNDERSTAND NONE OF THIS WOULD OF BEEN POSSIBLE SO I THANK YOU     ###
############################################################################################################################


def INDEX():
    link = OPEN_URL(U)
    fanart = re.compile('<fanart>(.+?)</fanart>').findall(link)[0]
    match = re.compile('<name>(.+?)</name>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
    addLink('[B][COLOR red]TWITTER>>[/COLOR][/B]','url',3,ART+'twitter.png',fanart)
    for name, url, iconimage in match:
        addDir('[B]%s[/B]' %name,url,1,iconimage,fanart,'','','')
    addDir('[B][COLOR white]RADIO[/COLOR][/B]',baseurl+'/uk.html',4,ART+'radio.png',fanart,'','','')
    
def TWITTER():
    text = ''
    twit = 'https://script.googleusercontent.com/macros/echo?user_content_key=rXU5694rJfWFhXFOXHDefjAraoscYkMEAPmdBxPOo-ohiVjjhciV8fgiD2lz9co-Z3fiMR_U05bmXbtq_6P95AQcp9aw6TsHm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnNCUu5a1B0gCRi0QD2WIIDr9ytRvHFpfmEF7NMAE6iMtxEG8qDxsuN80lJyPHV_vTU2r67oidbXqq0FrKMtrdDwPfGljarPsOUEGm5nigurI&lib=MXkI0j373OrefqLfXZ_5OzVHjKxKPCg9Y'
    link = OPEN_URL(twit)
    link = link.replace('/n','')
    link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
    match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
    for status, dte in match:
        status = status.encode('ascii', 'ignore')
        dte = dte[:-15]
        dte = '[COLOR red][B]'+dte+'[/B][/COLOR]'
        text = text+dte+'\n'+status+'\n'+'\n'
    showText('[COLOR red][B]@Stream[/B][/COLOR][B][COLOR white]Engine85[/B][/COLOR]', text)




def FETCH(url):
    link = OPEN_URL(url)
    fanart = re.compile('<fanart>(.+?)</fanart>').findall(link)[0]
    if '<name>' in link:
        LINK=link.split('<name')
        for p in LINK:
            try:
                name=re.compile('>(.+?)</name>').findall(p)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(p)[0]
                url=re.compile('<link>(.+?)</link>').findall(p)[0]
                addDir('[B]%s[/B]' %name,url,1,iconimage,fanart,'','','','')        
            except:pass
            
    if '<item>' in link:
        LINKS=link.split('<item>')
        for p in LINKS:
            try:
                name=re.compile('title>(.+?)<').findall(p)[0]
                iconimage=re.compile('thumbnail>(.+?)<').findall(p)[0]
                p=p.replace('\n','')
                url=re.compile('<link>(.+?)</link>').findall(p)[0]
                addDir('[B]%s[/B]' %name,url,2,iconimage,fanart,'','','','')
            except:pass
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )
    setView('movies', 'movie-view')
    

def RAD(url):
    link = OPEN_URL(url)
    requsted = 'https://pastebin.com/raw.php?i=izNG2Y7N'
    match=re.compile('<td><a href=".+?"><b>(.+?)</b></a></td>\n<td>(.+?)</td>\n<td><img src="mp3.gif" width="12" height="12" alt="MP3" /></td>\n<td><a href="(.+?)">(.+?)</a></td>\n<td>(.+?)</td>').findall(link)
    addDir('[B][COLOR red]CLICK HERE FOR REQUESTED STATIONS[/COLOR][/B]',requsted,1,iconimage,ART+'music.jpg','','','')
    for name,reg,url,qual,gen in match:
        name = name.replace('&amp;','&')
        addDir('[B][COLOR white]%s %s %s %s[/COLOR][/B]' %(name,gen,qual,reg),url,5,iconimage,ART+'music.jpg','','','')



def RESOLVE(name,url,iconimage):
    url1 = urlresolver.resolve(url)
    if url1:
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':description})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url1)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
    else:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def PLAYAUDIO(name,url,iconimage):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'audio')
        li = xbmcgui.ListItem('[COLOR red]PLAY[/COLOR] [COLOR white]%s[/COLOR]' %name, iconImage=iconimage, thumbnailImage=iconimage)
        li.setProperty('fanart_image', ART+'music.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

            
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addDir(name,url,mode,iconimage,fanart,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==2 :
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass


def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''

    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    #if addon.get_setting('auto-view') == 'true':

    #    print addon.get_setting(viewType)
    #    if addon.get_setting(viewType) == 'Info':
    #        VT = '515'
    #    elif addon.get_setting(viewType) == 'Wall':
    #        VT = '501'
    #    elif viewType == 'default-view':
    #        VT = addon.get_setting(viewType)

    #    print viewType
    #    print VT
        
    #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )


U=base64.decodestring('aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3LnBocD9pPTg2WEt3VzhQ')               
params=get_params()
url=None
name=None
mode=None
iconimage=None
date=None
description=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==1:
        FETCH(url)
        
elif mode==2:
        RESOLVE(name,url,iconimage)

elif mode==3:
        TWITTER()

elif mode==4:
        RAD(url)

elif mode==5:
        PLAYAUDIO(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
