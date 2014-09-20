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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,sys
h = HTMLParser.HTMLParser()

versao = '1.0.3'
addon_id = 'plugin.audio.rcpodcast'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
autoplay = False
if selfAddon.getSetting('autoplay') == 'true': autoplay = True
base_url = "http://radiocomercial.iol.pt"
mensagemok = xbmcgui.Dialog().ok

################################################## 

#MENUS############################################

def CATEGORIES():
	try:
		codigo_fonte = abrir_url("http://radiocomercial.iol.pt/player/podcasts.aspx")
	except: codigo_fonte = ""
	if codigo_fonte:
		match = re.findall('<div class="well" style="margin: 0px 0px 30px 0px;">(.*?)/h3>.+?</div>', codigo_fonte, re.DOTALL)
		print match[0]
		for podcast in match:
			url = re.compile('a href="(.+?)">').findall(podcast)
			img = re.compile('<img class.+?src="(.+?)"').findall(podcast)
			titulo = re.compile('class="uppercase">(.+?)<').findall(podcast)
			try:
				addDir(limpar_texto(titulo[0]),base_url + url[0],1,base_url + img[0])	
			except: pass
	addDir("Mixórdia de Temáticas - Série Ribeiro","http://radiocomercial.iol.pt/player/mixordia_de_tematicas.aspx?cid=36&sid=24",1,"http://radiocomercial.iol.pt/player/images/programas/rap.png")
	addLink('','','-')
	addDir('[B][COLOR blue]Definições[/COLOR][/B]','-',3,'-',False)
	disponivel=versao_disponivel() # nas categorias
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.audio.rcpodcast/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.audio.rcpodcast" name="Radio Comercial Podcast" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match

def limpar_texto(texto):
	return texto.replace("\xba","º").replace("\xda","Ú").replace("\xe9","é").replace("\xe1","á").replace("\xf3","ó").replace("\xca","Ê").replace("\xe3","ã").replace("\xed","í").replace("\xea","ê").replace("\xe7","ç").replace("\xf5","õ").replace('\xe2','â').replace('\xf4','ô')

def listar_videos(url,iconimage):
	try:
		codigo_fonte = abrir_url(url)
	except: codigo_fonte = ''
	if codigo_fonte:
		a = []
		match = re.compile('rel="(.+?)" href=".+?"><i class="fa fa-play" style="padding: 0px 20px 0px 15px;"></i>(.+?)</a></div>.+?\n.+?<div class="date.+?title="Data">(.+?)</div>').findall(codigo_fonte)
		if not match:
			match = re.compile('rel="(.+?)" href=".+?"><i class="fa fa-play" style="padding: 0px 20px 0px 15px;"></i>.+?\n.+?  (.+?)</a></div>.+?\n.+?<div class="date.+?title="Data">(.+?)</div>').findall(codigo_fonte)
		print match
		for mp3,titulo,data in match:
			temp = [titulo,data,url]
			a.append(temp)
			addLink('[B][COLOR blue]' + data + '[/B][/COLOR] - ' + limpar_texto(titulo),mp3,iconimage)

	else:
		mensagemok("Rádio Comercial Podcast","Impossível abrir url")
		sys.exit(0)
	
def play(url):
	try: mp3file = urllib2.urlopen(url)
	except: 
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir música! ")
		return
	playlst = xbmc.PlayList(1)
	playlst.clear()
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'audio/mpeg')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir música! ")
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
	liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
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
	print ""
	listar_videos(url,iconimage)

elif mode==2:
	print ""
	play(url)

elif mode==3:
	selfAddon.openSettings()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
