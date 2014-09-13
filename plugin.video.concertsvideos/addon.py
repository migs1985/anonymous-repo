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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
h = HTMLParser.HTMLParser()


addon_id = 'plugin.video.concertsvideos'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
versao = '1.0.0'

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Artists','http://www.concertsvideos.com/artists',1,artfolder + 'artists.png')
	addDir('Top Concerts','http://www.concertsvideos.com/top-concerts',4,artfolder + 'top.png')
	addDir('New Concerts','http://www.concertsvideos.com/new-concerts',4,artfolder + 'new.png')
	addDir('Search','-',5,artfolder + 'search.png')
	addLink('','-','-')
	disponivel=versao_disponivel() # nas categorias
	if disponivel==versao: addLink('[B][COLOR white]Last version installed (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Error verifying the version!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]New version available ('+ disponivel + '). Please update![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.concertsvideos/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.concertsvideos" name="Concerts Videos" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Error verifying the version!'
	return match
	
def listar_artistas(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<span class="field-content"><a href="/artist/(.+?)">(.+?)</a></span>').findall(codigo_fonte)
	img = re.compile('<img src="(.+?)" width="150" height="100" alt=""').findall(codigo_fonte)
	
	img2 = []
	for temp in img:
		if 'banner125x125.jpg' in temp: continue
		img2.append(temp)
		
	a = []
	for x in range(0, len(match)):
		a.append([match[x][1],match[x][0],img2[x]]); #titulo url img
	
	for titulo, link, img in a:
		link = 'http://www.concertsvideos.com/artist/' + link
		addDir(titulo,link,2,img)
	
	page = re.compile('<li class="pager-next"><a title="Go to next page" href="(.+?)">next ›</a></li>').findall(codigo_fonte)
	try: addDir('Next Page >>','http://www.concertsvideos.com' + page[0],1,'')
	except: pass

def listar_videos(url):	
	codigo_fonte = abrir_url(url)
	match = re.compile('<div class="field-content"><a href="(.+?)"><img src="(.+?)" width="150" height="100" alt="" /></a></div>  </div>\s+  <div class="views-field views-field-title">        <span class="field-content"><a href=".+?">(.+?)</a>').findall(codigo_fonte)
	for link, img, titulo in match:
		link = 'http://www.concertsvideos.com' + link
		titulo = titulo.replace('&#039;', '\'') 
		titulo = titulo.replace('&quot;', '"') 
		titulo = titulo.replace('&amp;', '&') 
		addDir(titulo,link,3,img,False)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def listar_videos2(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<a href="(.+?)"><img src="(.+?)" width="80" height="60" alt="" /></a>          </td>\s+<td class="views-field views-field-title" >\s+<a href=".+?">(.+?)</a>').findall(codigo_fonte)
	for link, img, titulo in match:
		link = 'http://www.concertsvideos.com' + link
		titulo = titulo.replace('&#039;', '\'') 
		titulo = titulo.replace('&quot;', '"')
		titulo = titulo.replace('&amp;', '&') 
		addDir(titulo,link,3,img,False)
		
def pesquisa():
	keyb = xbmc.Keyboard('', 'Search') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://www.concertsvideos.com/search/node/' + str(parametro_pesquisa) #nova definicao de url. str força o parametro de pesquisa a ser uma string
		listar_pesquisa(url) #chama a função listar_videos com o url definido em cima
	
def listar_pesquisa(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<li class="search-result">\s+<h3 class="title">\s+<a href="(.+?)">(.+?)</a>').findall(codigo_fonte)
	for link, titulo in match:
		titulo = titulo.replace('&#039;', '\'') 
		titulo = titulo.replace('&quot;', '"')
		titulo = titulo.replace('&amp;', '&') 
		if 'artist' in link: addDir(titulo,link,2,'-')
		elif 'video' in link: addDir(titulo,link,3,'-',False)
	page = re.compile('<li class="pager-next"><a title="Go to next page" href="(.+?)">next ›</a></li>').findall(codigo_fonte)
	try: addDir('Next Page >>','http://www.concertsvideos.com' + page[0],6,'')
	except: pass
	
def play(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Concerts Videos', 'Resolving link','Please wait...')
	codigo_fonte = abrir_url(url)
	try: id = re.compile('http://www.youtube.com/v/(.+?)\?rel=1&amp;autoplay=0&amp;fs=1').findall(codigo_fonte)[0]
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		return
	url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + id
	mensagemprogresso.update(50)
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass
###################################################################################
#FUNCOES JÁ FEITAS


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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
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


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode==1:
	listar_artistas(url)

elif mode==2:
	listar_videos(url)

elif mode==3:
	play(url)
	
elif mode==4:
	listar_videos2(url)
	
elif mode==5:
	pesquisa()

elif mode==6:
	listar_pesquisa(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
