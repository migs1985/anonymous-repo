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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys

### Adicionar PDF Reader
try:
	addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
	sys.path.append(addon_pdf)
	from pdf import pdf
	pdf = pdf()
except:
	dialog = xbmcgui.Dialog()
	dialog.ok("Erro!","Não foi encontrado o add-on PDF Reader.","Por favor, instale-o.","Pode obtê-lo através do repositório Anonymous")
	xbmc.executebuiltin('XBMC.ActivateWindow(Home)')
###

h = HTMLParser.HTMLParser()
versao='1.0.0'
addon_id = 'plugin.image.hqonline'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'


################################################## 

#MENUS############################################

def CATEGORIES():
	pdf.clean_temp()
	addDir('Listagem','-',9,artfolder + 'todos.png')
	addDir('Home','http://hqonline.com.br',7,artfolder + 'home.png')
	addDir('Categorias','-',1,artfolder + 'categorias.png')
	addDir('Pesquisar','-',5,artfolder + 'search.png')
	addLink('','','-')
	addDir('[B][COLOR white]Definições [COLOR red]PDF Reader[/COLOR][/B]','-',8,artfolder + 'settings.png',False)
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.image.hqonline/addon.xml')
		match=re.compile('<addon id="plugin.image.hqonline" name="HQ Online" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
def todos():
	codigo_fonte = abrir_url('http://hqonline.com.br')
	match = re.compile('\t<li class="page_item page-item-.+?"><a href="(.+?)">(.+?)</a></li>').findall(codigo_fonte)
	for url, title in match:
		title = title.replace('&#8211;','-').replace('&#038;','&')
		addDir(title,url,3,artfolder + 'ima.png')
	
def home(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<h1><a title="Permanent Link to (.+?)" href="(.+?)" rel="bookmark">').findall(codigo_fonte)
	for title, n_url in match:
		if title == 'Ofertas Saraiva' or title == 'Informação': continue
		title = title.replace('&#8211;','-').replace('&#038;','&')
		addDir(title,n_url,6,artfolder + 'ima.png')
	try:
		page = re.compile('<a class="nextpostslink" href="(.+?)">»</a>').findall(codigo_fonte)[0]
		addDir('Página Seguinte >>',page,7,artfolder + 'next.png')
	except: pass
	
def pesquisar():
	keyb = xbmc.Keyboard('', 'Pesquisar')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://hqonline.com.br/index.php?s=' + str(parametro_pesquisa)
	else: return
	codigo_fonte = abrir_url(url)
	match = re.compile('<h1><a title="Permanent Link to (.+?)" href="(.+?)" rel="bookmark">').findall(codigo_fonte)
	for title, n_url in match:
		if title == 'Ofertas Saraiva' or title == 'Informação': continue
		title = title.replace('&#8211;','-').replace('&#038;','&')
		addDir(title,n_url,6,artfolder + 'ima.png')
	
def categorias():
	addDir('Dark Horse','http://hqonline.com.br/?page_id=1002',2,artfolder + 'darkhorse.png')
	addDir('DC','http://hqonline.com.br/?page_id=629',2,artfolder + 'dc.png')
	addDir('Image Comics','http://hqonline.com.br/?page_id=491',2,artfolder + 'imagecomics.png')
	addDir('Marvel','http://hqonline.com.br/?page_id=496',2,artfolder + 'marvel.png')
	addDir('Vertigo','http://hqonline.com.br/?page_id=2399',2,artfolder + 'vertigo.png')
	addDir('Kodansha','http://hqonline.com.br/?page_id=504',2,artfolder + 'kodansha.png')
	addDir('Wildstorm','http://hqonline.com.br/?page_id=12473',2,artfolder + 'wildstorm.png')

def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('href="(.+?)"><img title="(.+?)" .+? src="(.+?)" width=".+?" height=".+?" /></a></th>').findall(codigo_fonte)
	total = len(match)
	for n_url, titulo, img in match:
		titulo = titulo.replace('&amp;','&')
		addDir(titulo,n_url,3,img,True,total)
	
def listar_bd(url):
	codigo_fonte = abrir_url(url)
	match = re.findall('href="https://.+?.google.com/(.+?)".+?<img.+?title="(.+?)".+?src="(.+?)".+?/>',codigo_fonte,re.DOTALL)
	for n_url, titulo, img in match:
		titulo = titulo.replace('&amp;','&')
		id = n_url.replace('open?id=','').replace('file/d/','').replace('?usp=sharing','').replace('/edit','').replace('?pli=1','')
		try: id = re.compile('(.+?)"').findall(id)[0]
		except: pass
		url_final = 'https://docs.google.com/uc?authuser=0&id='+id+'&export=download'
		addDir(titulo,url_final,4,img,False)
###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
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
elif mode==1: categorias()
elif mode==2: encontrar_fontes(url)
elif mode==3: listar_bd(url)
elif mode==4: pdf.pdf_read(name,url)
elif mode==5: pesquisar()
elif mode==6:
	encontrar_fontes(url)
	listar_bd(url)
elif mode==7: home(url)
elif mode==8: pdf.open_settings()
elif mode==9: todos()
xbmcplugin.endOfDirectory(int(sys.argv[1]))