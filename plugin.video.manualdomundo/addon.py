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
versao = '1.0.1'

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir("Videos Recentes",'-',1,artfolder + 'icon.png')
	addDir("Receitas",'http://www.manualdomundo.com.br/category/receitas-faceis-para-criancas-fazer/',2,artfolder + 'cozinha.png')
	addDir('Experiências','http://www.manualdomundo.com.br/category/experiencias-e-experimentos/',2,artfolder + 'ciencia.png')
	addDir('Brinquedos','http://www.manualdomundo.com.br/category/como-fazer-brinquedos-simples-baratos/',2,artfolder + 'toys.png')
	addDir('Desafios','http://www.manualdomundo.com.br/category/desafios-charadas-enigmas/',2,artfolder + 'desafios.png')
	addDir('Pegadinhas','http://www.manualdomundo.com.br/category/pegadinhas-brincadeiras-para-fazer-com-amigos-escola/',2,artfolder + 'prank.png')
	addDir('Mágicas','http://www.manualdomundo.com.br/category/como-fazer-magicas-simples-gratis/',2,artfolder + 'magic.png')
	addDir('Sobrevivência','http://www.manualdomundo.com.br/category/dicas-caseiras/',2,artfolder + 'sobrevivencia.png')
	addDir('Origami e Papel','http://www.manualdomundo.com.br/category/origami-e-papel/',2,artfolder + 'origami.png')
	addDir('Blog','http://www.manualdomundo.com.br/category/blog/',2,artfolder + 'blog.png')
	addDir('Boravê','http://www.manualdomundo.com.br/category/lugares-proibidos/',2,artfolder + 'borave.png')
	addDir('Outros','http://www.manualdomundo.com.br/category/sem-categoria/',2,artfolder + 'other.png')

	addLink("",'','-')
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def recentes():
	addLink('[B][COLOR white]Últimos Posts[/COLOR][/B]','','-')
	codigo_fonte = abrir_url("http://www.manualdomundo.com.br")
	link = re.compile('<li class="thumbs-ultimos-artigos"><a href="(.+?)">').findall(codigo_fonte)
	titulo = re.compile('<h2 class="title-posts-thumbs">(.+?)</h2>').findall(codigo_fonte)
	img = re.compile('<div id="imagens-posts" class="large-12 medium-12 small-12 left"><img class="lazy compress-image" src=".+?" data-original="(.+?)"').findall(codigo_fonte)

	for x in range(0,len(link)):
		addDir(titulo[x],link[x],3,img[x])
	
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.manualdomundo/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.manualdomundo" name="Manual do Mundo" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match

def listar_videos(url):
	codigo_fonte = abrir_url(url)
	link = re.compile('<a href="(.+?)" id="imagens-posts" class="large-12 medium-12 small-12 left">').findall(codigo_fonte)
	img = re.compile('<img class="lazy-mansory compress-image"\s+src=".+?"\s+data-original="(.+?)"').findall(codigo_fonte)
	titulo = re.compile('<h1 class="title-posts-thumbs-categorias">(.+?)</h1>').findall(codigo_fonte)
	
	for x in range(0,len(link)):
		addDir(titulo[x],link[x],3,img[x])
   
def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
	try: id_video = re.compile('www.youtube.com/embed/(.+?)"').findall(codigo_fonte)
	except: 
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		return
	
	if len(id_video) == 0: addLink("Sem vídeos...","","-")
	for id in id_video:
		html = abrir_url('http://www.youtube.com/embed/' + id)
		img = re.compile('"iurl": "(.+?)"').findall(html)[0].replace('\\','')
		titulo = re.compile('"title": "(.+?)"').findall(html)[0]
		addDir(titulo.decode('unicode-escape').encode('utf-8'),'plugin://plugin.video.youtube/?action=play_video&videoid=' + id,4,img,False)

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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: recentes()
elif mode==2: listar_videos(url)
elif mode==3: encontrar_fontes(url)
elif mode==4: play(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
