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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,os,json
h = HTMLParser.HTMLParser()

versao = '1.0.4'
addon_id = 'plugin.video.tugafilmes'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
down_path = selfAddon.getSetting('download-folder')
subs = selfAddon.getSetting('subs')

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Categorias','-',1,artfolder + 'categorias.png')
	addDir('Filmes 2014','http://www.tuga-filmes.info/search/label/-%20Filmes%202013',2,artfolder + 'categorias.png')
	addDir('Destaques','http://www.tuga-filmes.info/search/label/destaque',2,artfolder + 'destaques.png')
	addDir('Pesquisar','-',3,artfolder + 'pesquisar.png')
	
	addLink("",'',artfolder + '-')
	addDir('[B][COLOR blue]Definições do Add-on[/COLOR][/B]','-',7,artfolder + 'definicoes.png',False)
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")


###################################################################################
#FUNCOES
def categorias():
	addDir('Acção','http://www.tuga-filmes.info/search/label/Ac%C3%A7%C3%A3o',2,artfolder + 'categorias.png')
	addDir('Comédia','http://www.tuga-filmes.info/search/label/com%C3%A9dia',2,artfolder + 'categorias.png')
	addDir('Drama','http://www.tuga-filmes.info/search/label/Drama',2,artfolder + 'categorias.png')
	addDir('Romance','http://www.tuga-filmes.info/search/label/Romance',2,artfolder + 'categorias.png')
	addDir('Guerra','http://www.tuga-filmes.info/search/label/Guerra',2,artfolder + 'categorias.png')
	addDir('Terror','http://www.tuga-filmes.info/search/label/Terror',2,artfolder + 'categorias.png')
	addDir('Ficção','http://www.tuga-filmes.info/search/label/fic%C3%A7%C3%A3o-cientifica',2,artfolder + 'categorias.png')
	addDir('Aventura','http://www.tuga-filmes.info/search/label/Aventura',2,artfolder + 'categorias.png')
	addDir('Animação','http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o',2,artfolder + 'categorias.png')
	addDir('Documentário','http://www.tuga-filmes.info/search/label/Document%C3%A1rio',2,artfolder + 'categorias.png')
	
def download(name,url):
	if down_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", "Por favor defina a pasta de Download!")
		selfAddon.openSettings()
		return
	name = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',name)
	mypath=os.path.join(down_path,name+'.mp4')
	mypath_legendas=os.path.join(down_path,name+'.srt')
	
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Tuga-Filmes', 'A resolver link','Por favor aguarde...')
	mensagemprogresso.update(33)
	
	matriz = []
	codigo_fonte = abrir_url(url)
	
	try:  
		matriz = videomega_resolver(url)
		url_video = 'nada'
	except:
		try: url_video = re.compile('frameborder=".+?" height=".+?" scrolling=".+?" src="(.+?)"').findall(codigo_fonte)[0]
		except: 
			try: url_video = re.compile("width='.+?' height='.+?' scrolling='.+?' frameborder='.+?' src='(.+?)'").findall(codigo_fonte)[0]
			except:
				try: url_video = re.compile('width=".+?" height=".+?".+?frameborder=".+?" src="(.+?)"').findall(codigo_fonte)[0]
				except: return

	mensagemprogresso.update(66)
	
	if url_video == 'nada': pass
	elif 'dropvideo' in url_video: matriz = obtem_url_dropvideo(url_video)
	elif 'videowood' in url_video: matriz = videowood(url_video)
	else: return
	
	url = matriz[0]
	if url=='-': return
	legendas = matriz[1]
	
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	if os.path.isfile(mypath) is True:
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro','Já existe um ficheiro com o mesmo nome')
		return
			  
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()
	try:
		if legendas != '-': urllib.urlretrieve(legendas, mypath_legendas, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
		urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return
	dp.close()
	
def dialogdown(numblocks, blocksize, filesize, dp, start_time):
	try:
		percent = min(numblocks * blocksize * 100 / filesize, 100)
		print percent
		currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
		kbps_speed = numblocks * blocksize / (time.time() - start_time) 
		if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
		else: eta = 0 
		kbps_speed = kbps_speed / 1024 
		total = float(filesize) / (1024 * 1024) 
		mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
		e = ' (%.0f Kb/s) ' % kbps_speed 
		tempo = 'Tempo estimado:' + ' %02d:%02d' % divmod(eta, 60) 
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
	  
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.tugafilmes/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.tugafilmes" name="Tuga Filmes" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile("<a href='(.+?)' title='(.+?)'><div style='.+?'>.+?</div>.+?<div id='.+?'></div></a>").findall(codigo_fonte) 
	img = re.compile('<img alt="" border="0" src="(.+?)"').findall(codigo_fonte) #<div style="text-align: center;"><img alt="" border="0" src="(.+?)"

	a = [] # url titulo img
	for x in range(0, len(match)):
		temp = [match[x][0],match[x][1],img[x]]; 
		a.append(temp);
	
	total = len(a)
	for url2, titulo, img in a:
		titulo = titulo.replace('&#39;',"'")
		
		if selfAddon.getSetting('fanart') == 'true':
			user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
			txheaders= {'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
			tmdbim='http://d3gtl9l2a4fn1j.cloudfront.net/t/p/'
			try:
				t = titulo
				request='http://api.themoviedb.org/3/search/movie?api_key=eee9ac1822295afd8dadb555a0cc4ea8&order=asc&query=%s&per_page=1'%(urllib.quote_plus(t))
				req = urllib2.Request(request,None,txheaders)
				response=load_json(urllib2.urlopen(req).read())
				fanart = tmdbim + 'w780' + response['results'][0]['backdrop_path']
			except:
				try:
					t = file_name(url2).replace(".html","").replace("-"," ")
					request='http://api.themoviedb.org/3/search/movie?api_key=eee9ac1822295afd8dadb555a0cc4ea8&order=asc&query=%s&per_page=1'%(urllib.quote_plus(t))
					req = urllib2.Request(request,None,txheaders)
					response=load_json(urllib2.urlopen(req).read())
					fanart = tmdbim + 'w780' + response['results'][0]['backdrop_path']
				except: 
					try:
						t = file_name(url2).replace(".html","").replace("-"," ")
						t = ''.join(i for i in t if not i.isdigit())
						t = t.replace("(","").replace(")","")
						request='http://api.themoviedb.org/3/search/movie?api_key=eee9ac1822295afd8dadb555a0cc4ea8&order=asc&query=%s&per_page=1'%(urllib.quote_plus(t))
						req = urllib2.Request(request,None,txheaders)
						response=load_json(urllib2.urlopen(req).read())
						fanart = tmdbim + 'w780' + response['results'][0]['backdrop_path']
					except:fanart = ''
		else: fanart = ''
		addDirPlayer(titulo,url2,4,img,total,fanart)
		
	page = re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(codigo_fonte)
	try: addDir('Página Seguinte >>',page[0],2,artfolder + 'proxpagina.png')
	except: pass
	xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	if selfAddon.getSetting('fanart') == 'true': xbmc.executebuiltin("Container.SetViewMode(515)")
	else: xbmc.executebuiltin("Container.SetViewMode(50)")
	
def file_name(path):
	import ntpath
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)
		
def load_json(data):
	def to_utf8(dct):
		rdct = {}
		for k, v in dct.items() :
			if isinstance(v, (str, unicode)): rdct[k] = v.encode('utf8', 'ignore')
			else: rdct[k] = v
		return rdct
	try :        
		from lib import simplejson
		json_data = simplejson.loads(data, object_hook=to_utf8)
		return json_data
	except:
		try:
			import json
			json_data = json.loads(data, object_hook=to_utf8)
			return json_data
		except:
			import sys
			for line in sys.exc_info(): print "%s" % line
	return None
		
def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url)
	try: url_video = re.compile('var vurl = "(.+?)";').findall(codigo_fonte)[0]
	except: url_video = '-'
	try: url_legendas =	re.compile('var vsubtitle = "(.+?)";').findall(codigo_fonte)[0]
	except: url_legendas = '-'
	return [url_video,url_legendas]
	
def obtem_url_videomega(url):
	codigo_fonte = abrir_url(url)
	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(codigo_fonte)
	texto = urllib.unquote(code[0])
	try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
	except: url_video = '-'
	try: url_legendas = re.compile('http://videomega.tv/servesrt.php\?s=(.+?).srt').findall(texto)[0] + '.srt'
	except: url_legendas = '-'
	return [url_video,url_legendas]

def videowood(url):
	if not "embed" in url: url = 'http://videowood.tv/embed/' + re.compile('src="http://videowood.tv/embed/(.+?)"').findall(abrir_url(url))[0]
	codigo_fonte = abrir_url(url)
	file = re.compile('file: "(.+?)"').findall(codigo_fonte)[0]
	#swf = re.compile('flashplayer: "(.+?)"').findall(codigo_fonte)[0]
	srt = re.compile("addSubtitles\('(.+?)'").findall(codigo_fonte)[0]
	return [file,srt]
	
def abrir_url_tommy(url,referencia,form_data=None,erro=True):
	print "A fazer request tommy de: " + url
	from t0mm0.common.net import Net
	net = Net()
	try:
		if form_data==None:link = net.http_GET(url,referencia).content
		else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
		return link

	except urllib2.HTTPError, e:
		return "Erro"
	except urllib2.URLError, e:
		return "Erro"
	
def videomega_resolver(referer):
	html = abrir_url(referer)
	if re.search('http://videomega.tv/iframe.js',html):
		lines = html.splitlines()
		aux = ''
		for line in lines:
			if re.search('http://videomega.tv/iframe.js',line):
				aux = line
				break;
		ref = re.compile('ref="(.+?)"').findall(line)[0]
	else:
		try:
			hash = re.compile('"http://videomega.tv/validatehash.php\?hashkey\=(.+?)"').findall(html)[0]
			ref = re.compile('ref="(.+?)"').findall(abrir_url("http://videomega.tv/validatehash.php?hashkey="+hash))[0]
		except:
			try:
				hash = re.compile("'http://videomega.tv/validatehash.php\?hashkey\=(.+?)'").findall(html)[0]
				ref = re.compile('ref="(.+?)"').findall(abrir_url("http://videomega.tv/validatehash.php?hashkey="+hash))[0]
			except:
				iframe = re.compile('"http://videomega.tv/iframe.php\?(.+?)"').findall(html)[0] + '&'
				ref = re.compile('ref=(.+?)&').findall(iframe)[0]
	
	ref_data={'Host':'videomega.tv',
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'Referer':referer}
	url = 'http://videomega.tv/iframe.php?ref=' + ref
	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(abrir_url_tommy(url,ref_data))
	texto = urllib.unquote(code[0])
	try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
	except: url_video = '-'
	try: url_legendas = re.compile('http://videomega.tv/servesrt.php\?s=(.+?).srt').findall(texto)[0] + '.srt'
	except: url_legendas = '-'
	return [url_video,url_legendas]
	
def player(name,url,iconimage):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Tuga-Filmes', 'A resolver link','Por favor aguarde...')
	mensagemprogresso.update(33)
	
	matriz = []
	codigo_fonte = abrir_url(url)
	
	try:  
		matriz = videomega_resolver(url)
		url_video = 'nada'
	except:
		try: url_video = re.compile('frameborder=".+?" height=".+?" scrolling=".+?" src="(.+?)"').findall(codigo_fonte)[0]
		except: 
			try: url_video = re.compile("width='.+?' height='.+?' scrolling='.+?' frameborder='.+?' src='(.+?)'").findall(codigo_fonte)[0]
			except:
				try: url_video = re.compile('width=".+?" height=".+?".+?frameborder=".+?" src="(.+?)"').findall(codigo_fonte)[0]
				except: return

	mensagemprogresso.update(66)
	
	if url_video == 'nada': pass
	elif 'dropvideo' in url_video: matriz = obtem_url_dropvideo(url_video)
	elif 'videowood' in url_video: matriz = videowood(url_video)
	else: return
	
	url = matriz[0]
	if url=='-': return
	legendas = matriz[1]
	
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url,listitem)
		while not xbmcPlayer.isPlaying(): xbmc.sleep(500)
		if subs == 'true' and legendas != '-': xbmcPlayer.setSubtitles(legendas)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass
	
def pesquisa():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://www.tuga-filmes.info/search?q=' + str(parametro_pesquisa) #nova definicao de url. str força o parametro de pesquisa a ser uma string
		listar_videos(url) #chama a função listar_videos com o url definido em cima

		###################################################################################

def addDirPlayer(name,url,mode,iconimage,total,fnart=fanart):
	if fnart == '': fnart = fanart
	codigo_fonte = abrir_url(url)
	
	try: plot = re.compile('<b>SINOPSE:.+?</b><span style=".+?">(.+?)</span>').findall(codigo_fonte)[0]
	except: plot = 'Sem sinopse...'
	
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fnart)
	liz.setInfo( type="Video", infoLabels= { "Title": name,
											 "OriginalTitle": name,
											 "Plot": plot 
											 } )
	cm = []
	cm.append(('Sinopse', 'XBMC.Action(Info)'))
	cm.append(('Download', 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems = total)
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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True):
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


if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: categorias()
elif mode==2: listar_videos(url)
elif mode==3: pesquisa()
elif mode==4: player(name,url,iconimage)
elif mode==5: listar_videos_M18(url)
elif mode==6: download(name,url)
elif mode==7: selfAddon.openSettings()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
