"""
    Plugin for watching Youtube vidoes based on your Last.fm account
"""
#thanks to Tim Bormans for opening up the api to me (tv.timbormans.com)

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import access
import sys
import re
import urllib
import urllib2

__plugin__ = "LastTube"
__author__ = "rwparris2,dahool"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/LastTube"
__credits__ = "Team XBMC"
__version__ = "1.0.0"
__settings__ = xbmcaddon.Addon(id='plugin.video.lasttube.fm')
__language__ = __settings__.getLocalizedString

def main():
    if ( __name__ == "__main__" ):

        class MyPlayer( xbmc.Player ) :            
            def __init__ ( self ):
                xbmc.Player.__init__( self )
                
            def onPlayBackStarted(self):
                global apiURL
                global genre
                print 'LastTube --> playback started'
                addToQueue()
                while (True):#self.isPlaying()
                    if self.isPlaying():
                        xbmc.sleep(100)
                    else:
                        print 'LastTube --> broke out of loop'
                        addToQueue()                 
                        break

            def onPlayBackStopped(self):
                print "LastTube --> onPlayBackStopped"
                return True

            def onPlayBackEnded(self):
                print "LastTube --> onPlayBackEnded"
                
        def addToQueue():
            global apiURL
            print apiURL
            info=access.getVideoInfo(apiURL)
            url=info[0]
            artist=info[1]
            title=info[2]
            thumb=info[3]
            queueVid(url,artist,title,thumb)

        def queueVid(url,artist,title,thumb):
            global genre
            
            playlist = xbmc.PlayList(1)
            listitem = xbmcgui.ListItem(artist+" - "+str(title), thumbnailImage=thumb)
            listitem.setInfo('video', {'Title': artist+" - "+str(title), 'Genre': genre+' radio on LastTube'})
            listitem.setProperty('startedBy','LastTube')
            playlist.add(url, listitem)

            print 'item queued'
            #xbmcgui.Dialog().ok('','item got queued')
                
        def startPlayback(term,mode):
            global genre

            dialog = xbmcgui.DialogProgress()

            if mode==1:
                global apiURL
                apiURL='/user/'+term+'/topartists.xml'
                genre=dUser+'\'s'
            if mode==2:
                apiURL='/user/'+term+'/topartists.xml'
                genre=term+'\'s'
            if mode==3:
                apiURL='/artist/'+term+'/similar.xml'
                genre=term+'\'s similar artists'
            if mode==4:
                apiURL='/user/'+term+'/topartists.xml'
                genre=term
            
            info=access.getVideoInfo(apiURL)
            url=info[0]
            artist=info[1]
            title=info[2]
            thumb=info[3]

            objPL=xbmc.PlayList(1)
            objPL.clear()
            queueVid(url,artist,title,thumb)
            p.play(objPL)
            p.onPlayBackStarted()

        def search(title, mode):
            keyb = xbmc.Keyboard('', title)
            keyb.doModal()
            if (keyb.isConfirmed()):
                term = keyb.getText()
                startPlayback(term, mode)

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


        def addDir(name,url,mode,thumbnail):
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
            return ok

        def showCats():
            addDir("1. "+dUser+__language__(30000),"blah",1,"")
            addDir("2. "+__language__(30001),"blah",2,"")
            addDir("3. "+__language__(30002),"blah",3,"")
            addDir("4. "+__language__(30003),"blah",4,"")
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


        def showCatsNoUser():
            addDir("1. "+__language__(30001),"blah",2,"")
            addDir("2. "+__language__(30002),"blah",3,"")
            addDir("3. "+__language__(30003),"blah",4,"")
            xbmcplugin.endOfDirectory(int(sys.argv[1]))


        def getLastFMUserName():
            try:
                dUser=xbmc.executehttpapi('GetGuiSetting(3;scrobbler.lastfmusername)')
                p=re.compile('<li>(.*)')
                match=p.findall(dUser)
                for dUser in match:
                    return dUser
            except:
                return ""

        ############ MAIN ###########

        p=MyPlayer()
        params=get_params()

        url=None
        name=None
        mode=None
        apiURL=None
        genre=None
        dUser=getLastFMUserName()
        y=1

        try:
            url=urllib.unquote_plus(params["url"]) 
        except:
            pass
        try:
            name=urllib.unquote_plus(params["name"])
        except:
            pass
        try:
            mode=int(params["mode"])
        except:
            pass

        if mode==None and dUser=="":
            showCatsNoUser()
        elif mode==None or url==None:
            showCats()
        elif mode==1:
            startPlayback(dUser,mode)
        elif mode==2:
            search(__language__(30001),mode)
        elif mode==3:
            search(__language__(30002),mode)
        elif mode==4:
            search(__language__(30003),mode)

if __name__ == '__main__':
    main()
