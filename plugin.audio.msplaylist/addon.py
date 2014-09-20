#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,socket,time,os
socket.setdefaulttimeout( 10 )  # timeout in seconds
h = HTMLParser.HTMLParser()

versao = '1.0.7'
addon_id = 'plugin.audio.msplaylist'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
download_path = selfAddon.getSetting('download-folder')
playlist = selfAddon.getSetting('playlist') + 'playlist.txt'
autoplay = False
if selfAddon.getSetting('autoplay') == 'true': autoplay = True
prog_down = False
if selfAddon.getSetting('prog_down') == 'true': prog_down = True
traducaoma= selfAddon.getLocalizedString

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir(traducao(30056),'http://mp3skull.com/',2,artfolder + 'top.png')
	addDir(traducao(30000),'-',1,artfolder + 'Search.png')
	addDir(traducao(30057),'-',5,artfolder + 'Playlist.png',True,True)
	
	addLink('','-','-')
	addDir('[B][COLOR white]'+traducao(30001)+'[/COLOR][/B]','-',11,artfolder + 'aviso.png',False)
	addDir('[B][COLOR blue]'+traducao(30002)+'[/COLOR][/B]','-',9,artfolder + 'Settings.png',False)
	addLink('','-','-')
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]'+traducao(30003)+' (' + versao + ')[/COLOR][/B]','-',artfolder + 'versao.png')
	elif disponivel==traducao(30004): addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','-',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]'+traducao(30005)+' ('+ disponivel + '). '+traducao(30006)+'![/COLOR][/B]','-',artfolder + 'versao.png')
	
###################################################################################
#FUNCOES	

def listar_videos(name):
	name2 = name.replace(' - ',' ')
	name2 = urllib.quote(name2)
	url = 'https://www.youtube.com/results?search_query=' + name2 + '&lclk=video&filters=video'
	 
	codigo_fonte = abrir_url(url)
	try: 
		match1 = re.compile('data-context-item-id="(.+?)">').findall(codigo_fonte)
		match2 = re.compile('dir="ltr">(.+?)</a></h3><div class="yt-lockup-meta">').findall(codigo_fonte)
		
		match = []
		for x in range(0, len(match1)):
			temp = [match1[x],match2[x]]; 
			match.append(temp);
		
	except: 
		print "Erro ao obter video!"
		return
	for id, titulo in match:
		img = 'http://i1.ytimg.com/vi/' + id + '/mqdefault.jpg'
		titulo = titulo.replace('&#039;', '\'') 
		titulo = titulo.replace('&#39;', '\'') 
		titulo = titulo.replace('&quot;', '"') 
		titulo = titulo.replace('&amp;', '&') 
		addDir(titulo,'plugin://plugin.video.youtube/?action=play_video&videoid=' + id,16,img,False)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def play_youtube(url):
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass

def decode_car(titulo):
	titulo = titulo.replace('\xc3', "Ã").replace('\xd3', "Ó").replace('\xda', "Ú").replace('\xca', "Ê");
	titulo = titulo.replace('\xc9', "É").replace('\xc7', "Ç").replace('\xcd', "Í").replace('\xc2', "Â");
	titulo = titulo.replace('\xc1', "Á").replace('\xc0', "À").replace('\xe9', "é").replace('\xed', "í");
	titulo = titulo.replace('\xf3', "ó").replace('\xe7', "ç").replace('\xe3', "ã").replace('\xe2', "â");
	titulo = titulo.replace('\xea', "ê").replace('\xe1', "á").replace('\xfa', "ú").replace('\xe0', "à");
	titulo = titulo.replace('\xf4', 'ô').replace("\xba", "º").replace("\xf5", "õ");
	return titulo
	
def procura_letra(name):
	name2 = name.replace(' - ',' ')
	name2 = urllib.quote(name2 + ' vagalume')
	url = 'http://www.google.com/search?ie=UTF-8&oe=UTF-8&sourceid=navclient&gfns=1&q=' + name2
	codigo_fonte = abrir_url(url)
	try:
		letra = re.findall('<div itemprop=description>(.+?)</div>',codigo_fonte,re.DOTALL)[0]
		letra = letra.replace('<br/>','\n')
		letra = decode_car(letra)
		xbmc.executebuiltin("ActivateWindow(10147)")
		window = xbmcgui.Window(10147)
		xbmc.sleep(100)
		window.getControl(1).setLabel( "%s - %s" % (traducao(30007),name))
		window.getControl(5).setText(traducao(30008)+' "' + name + '" (Vagalume):\n' + letra)
	except:
		dialog = xbmcgui.Dialog()
		if dialog.yesno(traducao(30009),traducao(30010)):
			keyb = xbmc.Keyboard('',traducao(30000)) #Chama o keyboard do XBMC com a frase indicada
			keyb.doModal() #Espera ate que seja confirmada uma determinada string
			if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
				search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
				procura_letra(search)

def listar_musicas(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<div id="topright"><a href="(.+?)" title=".+?">(.+?)</a>').findall(codigo_fonte)
	for url,titulo in match:
		titulo = titulo.replace('Mp3','')
		addDir(titulo,'http://mp3skull.com'+url,7,artfolder + 'music.png')

def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.audio.msplaylist/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.audio.msplaylist" name="Mp3 Skull Playlist" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match=traducao(30004)
	return match
	
def pesquisa():
	keyb = xbmc.Keyboard('',traducao(30000)) #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		search = search.replace(' ','_')
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://mp3skull.com/mp3/' + str(parametro_pesquisa) + '.html' #nova definicao de url. str força o parametro de pesquisa a ser uma string
		encontrar_fontes(url) #chama a função listar_videos com o url definido em cima

def encontrar_fontes(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Mp3 Skull Playlist', traducao(30011),traducao(30012))
	mensagemprogresso.update(50)
	codigo_fonte = abrir_url(url)
	mp3 = re.compile('<div style="float:left;"><a href="(.+?)"').findall(codigo_fonte)
	titulo = re.compile('<div style="font-size:15px;"><b>(.+?) mp3</b>').findall(codigo_fonte)
	mensagemprogresso.update(100)
	mensagemprogresso.close()
		
	for x in range(0,len(mp3)):
		try:
			mp3[x] = mp3[x].replace(' ','%20')
			titulo[x] = titulo[x].replace('&','and').replace('\x00','')
			addMusica(titulo[x],mp3[x],3,'DefaultAudio.png')
		except: pass
		
	if len(mp3)==0:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30022),traducao(30061))
		url_sug = 'http://ac1.mp3skull.com/autocomplete/get.php?q=' + url.replace('http://mp3skull.com/mp3/','').replace('.html','')
		sug = abrir_url(url_sug)
		sugestoes = re.findall("'(.+?)'",sug,re.DOTALL)
		if len(sugestoes)<=1: return
		addLink('[COLOR white][B]'+traducao(30062)+'[/B][/COLOR]','',artfolder + 'sug.png')
		addLink('','','')
		for x in range(1,len(sugestoes)):
			nsearch = sugestoes[x].replace(' ','_')
			nsearch=urllib.quote(nsearch)
			nsearch = 'http://mp3skull.com/mp3/' + str(nsearch) + '.html'
			addDir(sugestoes[x],nsearch,7,artfolder + 'music.png')
			
def play(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Mp3 Skull Playlist',traducao(30013),traducao(30012))
	try: mp3file = urllib2.urlopen(url)
	except: 
		mensagemprogresso.close()
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014),traducao(30015))
		return
	mensagemprogresso.update(50)
	playlst = xbmc.PlayList(1)
	playlst.clear()
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'audio/mpeg')
	listitem.setProperty('IsPlayable', 'true')
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014),traducao(30015))
		pass
		
def download(name,url):
	if download_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014),traducao(30016),traducao(30017))
		selfAddon.openSettings()
		return
	try:
		name = name.replace('/', '-')
		name = name.replace('\\', '-')
		name = name.replace(':', '-')
		name = name.replace('*', '')
		name = name.replace('"', '')
		name = name.replace('?', '')
		name = name.replace('>', '')
		name = name.replace('<', '')
		name = name.replace('|', '-')
		
		mypath = download_path + name + '.mp3'
		
		if os.path.isfile(mypath) is True:
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(30014),traducao(30060))
			return
				  
		if prog_down:
			dp = xbmcgui.DialogProgress()
			dp.create(traducao(30038))
			start_time = time.time()
			try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
			except:
				while os.path.exists(mypath): 
					try: os.remove(mypath); break 
					except: pass
				dp.close()
				return
			dp.close()
		else:
			f = urllib2.urlopen(url)
			with open(mypath, "wb") as code:
				code.write(f.read())
				
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30038),traducao(30018))
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014),traducao(30019))

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(30063) + ' %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)
	  
def mensagemaviso():
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % (traducao(30020),'Mp3 Skull Playlist',))
        window.getControl(5).setText("[COLOR red][B]"+traducao(30040)+":[/B][/COLOR]\n"+traducao(30041)+"\n\n"+traducao(30042)+"\n\n[COLOR red][B]"+traducao(30043)+"[/B][/COLOR]\n"+traducao(30044)+"\n\n"+traducao(30045)+"\n\n"+traducao(30046)+"\n\n[COLOR red][B]"+traducao(30047)+"[/B][/COLOR]\n"+traducao(30048)+"\n\n"+traducao(30049)+"\n\n"+traducao(30050))
    except: pass
	
############################################## PLAYLIST #################################
def pesquisa_playlist():
	if verifica_path(): return
	keyb = xbmc.Keyboard('',traducao(30000)) #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		search = search.replace(' ','').replace('\'','').replace('-','').replace('/','').replace('\\','').lower()
	else: return
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: return
	for line in lines:
		match = re.compile('name="(.+?)" url="(.+?)"').findall(line)
		titulo = match[0][0].replace(' ','').replace('-','').replace('\'','').replace('/','').replace('\\','').lower()
		if titulo.find(search) != -1 : 
			if autoplay: addMusicaPlaylist(match[0][0],match[0][1],'DefaultAudio.png')
			else:addMusica(match[0][0],match[0][1],3,'DefaultAudio.png')
	
def verifica_path():
	if playlist == 'playlist.txt': 
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014),traducao(30021))
		selfAddon.openSettings()
		return True
	else: return False
	
def importar():
	if verifica_path(): return
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
		if lines:
			dialog = xbmcgui.Dialog()
			if not dialog.yesno(traducao(30022),traducao(30023),traducao(30024)): return
	except: pass
	dialog = xbmcgui.Dialog()
	file = dialog.browse(1,traducao(30025),"myprograms")
	if not file: return
	if 'playlist.txt' not in file:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014), traducao(30026))
		return
	lines = []
	try:
		f = open(file,"r")
		lines = f.readlines()
		f.close()
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014), traducao(30027))
		return
	f = open(playlist,"w")
	for line in lines:
		try:
			match = re.compile('name="(.+?)" url="(.+?)"').findall(line)
			f.write('name="' + match[0][0] + '" url="' + match[0][1] + '"\n')
		except: pass
	f.close()
	dialog = xbmcgui.Dialog()
	dialog.ok(traducao(30022), traducao(30028))
	
def exportar():
	if verifica_path(): return
	dialog = xbmcgui.Dialog()
	dir = dialog.browse(0,traducao(30029),"myprograms")
	if not dir: return
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
		f = open(dir + 'playlist.txt',"w")
		for line in lines:
			f.write(line)
		f.close()
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30022),traducao(30030))
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(30014), traducao(30031),traducao(30032))
	
	
def save(name,url):
	if verifica_path(): return
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: 
		try:open(playlist, 'a').close()
		except:
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(30014),traducao(30031),traducao(30033))
			return
	
	flag = True
	f = open(playlist,"w")
	name = name.replace('"','\'')
	for line in lines:
		if line == 'name="' + name + '" url="' + url + '"\n': flag = False
		f.write(line)
	if flag: f.write('name="' + name + '" url="' + url + '"\n')
	f.close()

def remove(name,url):
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: pass
	
	try: f = open(playlist,"w")
	except: return
	for line in lines:
		if line != str('name="' + name + '" url="' + url + '"\n'): f.write(line)
	f.close()
	xbmc.executebuiltin("Container.Refresh")
	
def le_playlist():
	if verifica_path(): return
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: pass
	if len(lines)==0: return
	addDir('[B][COLOR white]'+traducao(30058)+'[/B][/COLOR]','-',17,artfolder + 'Search.png')
	#addDir('[B][COLOR white]'+traducao(30034)+'[/B][/COLOR]','-',10,artfolder + 'delete.png')
	addLink('','','-')
	for line in lines:
		match = re.compile('name="(.+?)" url="(.+?)"').findall(line)
		if autoplay: addMusicaPlaylist(match[0][0],match[0][1],'DefaultAudio.png')
		else:addMusica(match[0][0],match[0][1],3,'DefaultAudio.png',True)
		
def apaga_playlist():
	dialog = xbmcgui.Dialog()
	if dialog.yesno(traducao(30022),traducao(30035)):
		try: 
			f = open(playlist,"w")
			f.close()
		except: return
	else: return

###################################################################################
#FUNCOES JÁ FEITAS

def addMusicaPlaylist(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	cm = []
	cm.append((traducao(30037), 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30038), 'XBMC.RunPlugin(%s?mode=8&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30039), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30055),  'XBMC.Container.Update(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
	return ok

def addMusica(name,url,mode,iconimage,playlist_dir = False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
	cm = []
	if playlist_dir: cm.append((traducao(30037), 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	else: cm.append((traducao(30036), 'XBMC.RunPlugin(%s?mode=4&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30038), 'XBMC.RunPlugin(%s?mode=8&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30039), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append((traducao(30055),  'XBMC.Container.Update(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	cm = []
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,playlist_dir = False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	cm = []
	if playlist_dir:
		cm.append((traducao(30029), 'XBMC.RunPlugin(%s?mode=12&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append((traducao(30025), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append((traducao(30034), 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
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

params=get_params()
url=None
name=None
mode=None
iconimage=None

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
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: pesquisa()	
elif mode==2: listar_musicas(url)
elif mode==3: play(url)
elif mode==4: save(name,url)
elif mode==5: le_playlist()
elif mode==6: remove(name,url)
elif mode==7: encontrar_fontes(url)
elif mode==8: download(name,url)
elif mode==9: selfAddon.openSettings()
elif mode==10: apaga_playlist()
elif mode==11: mensagemaviso()
elif mode==12: exportar()
elif mode==13: importar()
elif mode==14: procura_letra(name)
elif mode==15: listar_videos(name)
elif mode==16: play_youtube(url)
elif mode==17: pesquisa_playlist()
xbmcplugin.endOfDirectory(int(sys.argv[1]))