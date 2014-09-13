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


addon_id = 'plugin.video.manualdomundo'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
versao = '1.0.0'


################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Vídeos Novos','http://www.manualdomundo.com.br',2,artfolder + 'videos.png')
	addDir('Experiências','http://www.manualdomundo.com.br/category/experiencias/',2,artfolder + 'ciencia.png')
	addDir('Mágicas','http://www.manualdomundo.com.br/category/magica/',2,artfolder + 'magic.png')
	addDir('Pegadinhas','http://www.manualdomundo.com.br/category/pegadinhas/',2,artfolder + 'prank.png')
	addDir('Vlog','http://www.manualdomundo.com.br/category/vlog/',2,artfolder + 'vlog.png')
	addDir('Origami e Papel','http://www.manualdomundo.com.br/category/origami/',2,artfolder + 'origami.png')
	addDir('Receitas','http://www.manualdomundo.com.br/category/receitas-cozinha/',2,artfolder + 'cozinha.png')
	addDir('Desafios','http://www.manualdomundo.com.br/category/desafios/',2,artfolder + 'desafios.png')
	addDir('Brinquedos','http://www.manualdomundo.com.br/category/como-fazer-brinquedos-simples-baratos/',2,artfolder + 'toys.png')
	addDir('Camping e Aventura','http://www.manualdomundo.com.br/category/acampamento/',2,artfolder + 'camping.png')
	addDir('Casa e Carro','http://www.manualdomundo.com.br/category/casa/',2,artfolder + 'home.png')
	addDir('Música','http://www.manualdomundo.com.br/category/musicas/',2,artfolder + 'music.png')
	addDir('Outros','http://www.manualdomundo.com.br/category/sem-categoria/',2,artfolder + 'other.png')

	addLink("",'','-')
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.manualdomundo/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.manualdomundo" name="Manual do Mundo" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match

def listar_videos(url):
	codigo_fonte = abrir_url(url)
	img = re.compile("<img src='(.+?)' title=").findall(codigo_fonte)
	match = re.compile('<a href="(.+?)" rel="bookmark" title="Permanent Link: (.+?)">.+?</a>').findall(codigo_fonte)
	if len(match)!=len(img): # algumas postagens nao tem imagem
		a = re.compile("<a href='(.+?)'><img src='(.+?)' title='(.+?)'").findall(codigo_fonte)
		for x in range(0, len(match)):
			flag = True
			for j in range(0, len(a)):
				if match[x][0] == a[j][0]:
					#a[j][2] = match[x][1] # altera o título, pois o de match é mais correcto
					flag = False
			if flag: a.append([match[x][0],'-',match[x][1]])
	else:
		a = []
		for x in range(0, len(match)):
			temp = [match[x][0],img[x],match[x][1]]; 
			a.append(temp)
			
	for url,img,titulo in a:
		titulo = titulo.replace('&#8211;', '')
		addDir(titulo,url,3,img)
	
	try: 
		page =  re.compile("<link rel='next' href='(.+?)'").findall(codigo_fonte)[0]
		addDir('Página Seguinte >>',page,2,'')
	except: pass
   
def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
	try: id_video = re.compile('www.youtube.com/embed/(.+?)"').findall(codigo_fonte)
	except: 
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		return
		
	i = 1
	for id in id_video:
		addDir('Vídeo ' + str(i),'plugin://plugin.video.youtube/?action=play_video&videoid=' + id,4,'DefaultVideo.png',False)
		i = i + 1


def play(url):
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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder = pasta)
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
	
elif mode==2:
	print ""
	listar_videos(url)

elif mode==3:
	print ""
	encontrar_fontes(url)
	
elif mode==4:
	print ""
	play(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
