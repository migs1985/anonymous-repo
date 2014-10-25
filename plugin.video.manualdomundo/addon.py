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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,xbmcvfs,time,os
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.manualdomundo'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
versao = '1.0.1'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
if xbmc.getCondVisibility('system.platform.windows'): pastaperfil = pastaperfil.replace('\\','/')

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
	link = re.compile('<div class="thumbs-content-categorias"><a href="(.+?)" id="imagens-posts" class="large-12 medium-12 small-12 left">').findall(codigo_fonte)
	try: nada = link[0]
	except: link = re.compile('<div class="thumbs-content-categorias">\s+<a href="(.+?)" id="imagens-posts" class="large-12 medium-12 small-12 left">').findall(codigo_fonte)
	img = re.compile('<img class="lazy-mansory compress-image"\s+src=".+?"\s+data-original="(.+?)"').findall(codigo_fonte)
	titulo = re.compile('<h1 class="title-posts-thumbs-categorias">(.+?)</h1>').findall(codigo_fonte)
	
	for x in range(0,len(link)):
		addDir(titulo[x],link[x],3,img[x])
   
def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
	id_video = re.compile('www.youtube.com/embed/(.+?)"').findall(codigo_fonte)
	try:
		texto = re.compile('<meta property="og:description" content="(.+?)"').findall(codigo_fonte)[0]
		try:
			txt = ''
			texto2 = re.findall('<div id="posts-conteudo" class="large-12 medium-12 small-12 columns">(.*?)<footer id="footer-posts" class="large-12 medium-12 small-12 left">',codigo_fonte,re.DOTALL)
			nada = texto2[0]
			texto2 = re.findall('<p>(.+?)</p>',codigo_fonte,re.DOTALL)
			nada = texto2[0]
			for t in texto2: 
				if 'href' in t or 'target' in t or 'src' in t: continue
				t = t.replace('<span style="font-size: 14px; line-height: 1.5em;">','').replace('</span>','').replace('&nbsp;','').replace('<sub>','').replace('</sub>','')
				t = t.replace('<strong>','').replace('</strong>','').replace('<span style="line-height: 1.5em;">','').replace('<br />','')
				txt += t + '\n\n'
			if txt.replace('\n','').replace(' ','') != '': texto = '[B][COLOR blue]Descrição:[/COLOR][/B]\n' + texto + '\n\n[B][COLOR blue]Texto:[/COLOR][/B]\n' + txt
		except: pass
		if texto != '': 
			addLink('[B][COLOR white]Descrição/Texto[/COLOR][/B]','','-')
			addDir('Descrição',texto,5,'-',False)
	except: pass
	
	if len(id_video) != 0: 
		addLink("","","-")
		addLink('[B][COLOR white]Vídeos[/COLOR][/B]','','-')
	for id in id_video:
		html = abrir_url('http://www.youtube.com/embed/' + id)
		img = re.compile('"iurl": "(.+?)"').findall(html)[0].replace('\\','')
		titulo = re.compile('"title": "(.+?)"').findall(html)[0]
		addDir(titulo.decode('unicode-escape').encode('utf-8'),'plugin://plugin.video.youtube/?action=play_video&videoid=' + id,4,img,False)

	images = re.compile('<meta property="og:image" content="(.+?)" />').findall(codigo_fonte)
	if len(images) <= 1: return
	addLink('','','-')
	addLink('[B][COLOR white]Imagens[/COLOR][/B]','','-')
	for x in range(0,len(images)):
		addDir('Imagem ' + str(x+1),images[x],6,images[x],False)

def playimage(url):
	if re.search('.gif',url):
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=url)
		player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		player.play(url,listitem)
		return
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	extensao = ['.jpg','.png','.gif','.bmp']
	extfic = ''
	for x in range(0,len(extensao)):
		if re.search(extensao[x],url): extfic='temp' + extensao[x]
	if extfic == '': return
	for ext in extensao:
		try:os.remove(os.path.join(pastaperfil,'temp'+ext))
		except:pass	
	mypath = os.path.join(pastaperfil,extfic)
	import requests
	with open(mypath, 'wb') as handle:
		response = requests.get(url, stream=True)
		if not response.ok: 
			print 'ERRO'
			xbmc.executebuiltin("Dialog.Close(busydialog)")
			return
		for block in response.iter_content(1024):
			if not block: break
			handle.write(block)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	xbmc.executebuiltin("SlideShow("+pastaperfil+")")
	
def texto(url):
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('Manual do Mundo','Descrição'))
        window.getControl(5).setText(url)
    except: pass
		
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

if mode==None or url==None or len(url)<1:
	if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
	CATEGORIES()
elif mode==1: recentes()
elif mode==2: listar_videos(url)
elif mode==3: encontrar_fontes(url)
elif mode==4: play(url)
elif mode==5: texto(url)
elif mode==6: playimage(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
