#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2014 - Anonymous

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
down_path = selfAddon.getSetting('download-folder')
mensagemprogresso = xbmcgui.DialogProgress()
main_url = 'http://www.boafoda.com'

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################
def menu():
	addDir(traducao(2052),'http://www.boafoda.com/videos/',512,artfolder + 'videos.png')
	addDir(traducao(2019),'recentes',511,artfolder + 'videos.png')
	addDir(traducao(2021),'favoritos',501,artfolder + 'fav.png')
	addDir(traducao(2049),'pornstars',501,artfolder + 'pstars.png')
	addDir(traducao(2029),'-',505,artfolder + 'pstars.png')
	addDir(traducao(2031),'-',508,artfolder + 'estudios.png')
	addDir(traducao(2022),'-',504,artfolder + 'search.png')
	addDir(traducao(2028)+' A-Z','-',507,artfolder + 'cat.png')
	addDir(traducao(2003),'-',513,artfolder + 'settings.png',pasta=False)
	
def estudios():
	addDir(traducao(2051),'-',510,'-')
	html = re.findall('<span>Os Estúdios de A a Z</span>(.*?)<div id="container_studios" class="main-wrapper">'.decode('utf-8'),abrir_url('http://www.boafoda.com/studios/'),re.DOTALL)[0]
	match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
	for link, letra in match:
		addDir(letra,main_url+link,509,'-')
	
def videos_recentes(offset):
	referer = 'http://www.boafoda.com/videos/'
	url = 'http://www.boafoda.com/videos/fetch'
	limit=60
	
	form_values={'type':'channel_videos',
				 'order':'published_date',
				 'period':'all',
				 'offset':str(offset),
				 'limit':str(limit),
				 'channels_amount':'3'}
				 
	codigo_fonte = post(url,referer,form_values).decode("unicode_escape").encode('utf-8').replace('\\','')
	match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(codigo_fonte)
	for link,title,img in match:
		addDir(title,link,502,img,pasta=False)
	if len(match)==limit: addDir(traducao(2050),'-',511,artfolder + 'next.png',offset=offset+len(match))
	
def listar_estudios2(offset):
	referer = 'http://www.boafoda.com/studios/'
	url = 'http://www.boafoda.com/studios/fetch'
	limit=60
	
	if selfAddon.getSetting('order') == 'rating': order='rating'
	elif selfAddon.getSetting('order') == 'views': order='video_views'
	elif selfAddon.getSetting('order') == 'published_date': order='date'
	else: order='rating'  #'video_rating'
	
	form_values={'type':'default',
				 'order':order,
				 'offset':str(offset),
				 'limit':str(limit)}
	
	codigo_fonte = post(url,referer,form_values).decode("unicode_escape").encode('utf-8').replace('\\','')
	match = re.compile('<a href="(.+?)">\s+<img src="(.+?)" alt="(.+?)"').findall(codigo_fonte)
	for link,img,title in match:
		addDir(title,link,515,img)
	if len(match)==limit: addDir(traducao(2050),'-',510,artfolder + 'next.png',offset=offset+len(match))
		
def listar_videos_estudios(url,offset):
	id = re.compile('http://www.boafoda.com/studios/(.+?)/').findall(url)[0]
	url2 = 'http://www.boafoda.com/videos/fetch'
	limit=60
	
	form_values={'type':'studio_videos',
				 'order':selfAddon.getSetting('order'),
				 'period':'all',
				 'offset':str(offset),
				 'limit':str(limit),
				 'id':id}

	codigo_fonte = post(url2,url,form_values).decode("unicode_escape").encode('utf-8').replace('\\','')
	match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(codigo_fonte)
	for link,title,img in match:
		addDir(title,link,502,img,pasta=False)
	if len(match)==limit: addDir(traducao(2050),url,515,artfolder + 'next.png',offset=offset+len(match))
		
def settings():
	order = ['rating','views','published_date','length']
	index = xbmcgui.Dialog().select(traducao(2053), [traducao(2054),traducao(2055),traducao(2056),traducao(2057)])
	if index != -1: selfAddon.setSetting('order',value=order[index])
		
def listar_estudios(url):
	html = re.findall('<span>Top Estúdios</span>(.*?)<div class="bottom">'.decode('utf-8'),abrir_url(url),re.DOTALL)[0]
	match = re.compile('<a href="(.+?)">\s+<img src="(.+?)" alt="(.+?)"').findall(html)
	for link,img,title in match:
		addDir(title.decode("latin-1").encode("utf-8"),link,503,img)
	
def cat():
	codigo_fonte=abrir_url('http://www.boafoda.com/pornstars/')
	html = re.findall('<div class="menu-content-links" id="left_menuAZ_cotent">(.*?)</div>',codigo_fonte,re.DOTALL)[0]
	match = re.compile('<a href="(.+?)" title="(.+?)">').findall(html)
	for link,title in match:
		addDir(title.decode("latin-1").encode("utf-8"),link,512,'-')
	if selfAddon.getSetting('gay') == 'false':
		addDir('','-',599,'-',pasta=False)
		html = re.findall('<div class="menu-content-links filtered_cats">(.*?)</div>',codigo_fonte,re.DOTALL)[0]
		match = re.compile('<a href="(.+?)" title="(.+?)">').findall(html)
		for link,title in match:
			addDir(title.decode("latin-1").encode("utf-8"),link,512,'-')
		
def listar_videos2(url,offset):
	try: ch = re.compile('http://www.boafoda.com/channels/(.+?)/').findall(url)[0]
	except: ch = 'erro'
	url2 = 'http://www.boafoda.com/videos/fetch'
	limit=60
	
	form_values={'type':'channel_videos',
				 'order':selfAddon.getSetting('order'),
				 'period':'all',
				 'offset':str(offset),
				 'limit':str(limit),
				 'channels_amount':'3'}
	if ch != 'erro': form_values['channels[]']=ch

	codigo_fonte = post(url2,url,form_values).decode("unicode_escape").encode('utf-8').replace('\\','')
	match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(codigo_fonte)
	for link,title,img in match:
		addDir(title,link,502,img,pasta=False)
	if len(match)==limit: addDir(traducao(2050),url,512,artfolder + 'next.png',offset=offset+len(match))
	
def pornstars():
	html = re.findall('<div class="letter">(.*?)</div>',abrir_url('http://www.boafoda.com/pornstars/'),re.DOTALL)[0]
	match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
	for link, letra in match:
		addDir(letra,main_url+link,506,'-',letra=letra)
	
def pesquisa():
	keyb = xbmc.Keyboard('', traducao(2022)+':')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://www.boafoda.com/search/videos/' + str(parametro_pesquisa)
		listar_videos(url)
	
def recentes(url):
	codigo_fonte = abrir_url('http://www.boafoda.com/')
	'''
	if url=='recentes': 
		html = re.findall('<span>Os mais recentes</span>(.*?)<div class="bottom">',codigo_fonte,re.DOTALL)[0]
		match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(html)
		for link,title,img in match:
			addDir(title.decode("latin-1").encode("utf-8"),link,502,img,pasta=False)
	'''
	if url=='favoritos': 
		html = re.findall('<span>Top Favoritos</span>(.*?)<div class="bottom">',codigo_fonte,re.DOTALL)[0]
		match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(html)
		for link,title,img in match:
			addDir(title.decode("latin-1").encode("utf-8"),link,502,img,pasta=False)
	if url=='pornstars': 
		html = re.findall('<span>Top Estrelas Porno</span>(.*?)<div class="bottom">',codigo_fonte,re.DOTALL)[0]
		match = re.compile('<a href="(.+?)">\s+<img src="(.+?)" alt="(.+?)"').findall(html)
		for link,img,title in match:
			addDir(title.decode("latin-1").encode("utf-8"),link,503,img)
	else: return
	
def listar_pornstars(name,url,offset,letra):
	letra = letra.lower()
	limit = 60
	url2 = url.replace('/'+letra+'/','/fetch')
	form_values={'type':'pornstars',
				 'sort':'score',
				 'letter':letra,
				 'offset':str(offset),
				 'limit':str(limit)}
	
	codigo_fonte = post(url2,url,form_values).encode('utf-8')
	match = re.compile('<a href="(.+?)">\s+<img src="(.+?)" alt="(.+?)"').findall(codigo_fonte)
	for link,img,title in match:
		addDir(title.decode("latin-1").encode("utf-8"),link,514,img)
	if len(match)==limit: addDir(traducao(2050),url,506,artfolder + 'next.png',offset=offset+len(match),letra=letra)
		
def listar_videos_pornstars(url,offset):
	id = re.compile('http://www.boafoda.com/pornstars/(.+?)/').findall(url)[0]
	url2 = 'http://www.boafoda.com/videos/fetch'
	limit=60
	
	form_values={'type':'pornstar_videos',
				 'order':selfAddon.getSetting('order'),
				 'period':'all',
				 'offset':str(offset),
				 'limit':str(limit),
				 'id':id}

	codigo_fonte = post(url2,url,form_values).decode("unicode_escape").encode('utf-8').replace('\\','')
	match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(codigo_fonte)
	for link,title,img in match:
		addDir(title,link,502,img,pasta=False)
	if len(match)==limit: addDir(traducao(2050),url,514,artfolder + 'next.png',offset=offset+len(match))
		
def post(url,referer,form_values):
	headers={'Host':'www.boafoda.com',
			 'Connection':'keep-alive',
			 'Accept':'*/*',
			 'Origin':'Origin: http://www.boafoda.com',
			 'X-Requested-With': 'XMLHttpRequest',
			 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
			 'Referer':referer,
			 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			 'Accept-Encoding':'gzip,deflate',
			 'Accept-Language':'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4'}
	
	from t0mm0.common.net import Net
	net = Net()
	return net.http_POST(url, form_data=form_values,headers=headers).content
		
def listar_videos(url):
	codigo_fonte=abrir_url(url)
	try: html = re.findall('<head>(.*?)<span>A ser visto</span>',codigo_fonte,re.DOTALL)[0]
	except: html = codigo_fonte
	match = re.compile('<a href="(.+?)" target="_self" title="(.+?)">\s+<img\s+id=".+?"\s+class="normal js_thumb"\s+src="(.+?)"').findall(html)
	for link,title,img in match:
		addDir(title.decode("latin-1").encode("utf-8"),link,502,img,pasta=False)
	
def listar_fontes(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	url_vid = 'http://videos.boafoda.com/player/' + re.compile('src="http://videos.boafoda.com/player/(.+?)"').findall(abrir_url(url))[0]
	ref_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
				'Host': 'videos.boafoda.com',
				'Referer': url,
				'Connection': 'Keep-Alive'}
	match = re.compile('file:"(.+?)",type:".+?"').findall(abrir_url_tommy(url_vid,ref_data))
	type = []
	link = []
	for m in match:
		if '.mp4' in m:
			link.append(m)
			type.append('mp4')
		elif '.m3u8':
			link.append(m)
			type.append('m3u8')
	if len(link)==0: return
	index = xbmcgui.Dialog().select(traducao(2048), type)
	if index == -1: return
	if type[index]=='mp4': play(name,link[index],iconimage)
	elif type[index]=='m3u8':
		streamurl = m3u8(link[index])
		play(name,streamurl,iconimage)

def m3u8(m3u):
	try:
		inf = abrir_url(m3u).splitlines()
		qualidade = []
		qualidade_str = []
		for line in inf:
			line=line.strip()
			if line.startswith('#EXT-X-STREAM-INF'): 
				qualidade.append(str_int(line.split('#EXT-X-STREAM-INF')[1].split('BANDWIDTH=')[1]))
				qualidade_str.append('%s kbps' % (str_int(line.split('#EXT-X-STREAM-INF')[1].split('BANDWIDTH=')[1])/1000))
		m3u8=''
		if selfAddon.getSetting('max_qual')=='true': qualidade_escolhida = str(max(qualidade))
		else:
			index = xbmcgui.Dialog().select(traducao(2012), qualidade_str)
			if index == -1: return
			qualidade_escolhida = str(qualidade[index])
		for x in range(0,len(inf)):
			if 'BANDWIDTH='+qualidade_escolhida in inf[x]:
				m3u8 = inf[x+1]
				break
		m3u8 = m3u.replace(file_name(m3u),m3u8)
		return m3u8
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"
	
def str_int(str):
	try: int(str[0])
	except: return -1
	for x in range(0,len(str)):
		try: int(str[x])
		except: return int(str[0:x])
	return int(str)
	
def file_name(path):
	import ntpath
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)
	
def play(name,streamurl,iconimage = "DefaultVideo.png"):
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(streamurl,listitem)
	
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
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,total=1,pasta = True,video=False,offset=0,letra=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&offset="+str(offset)+"&letra="+str(letra)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	if video: 
		cm.append(('Download', 'XBMC.RunPlugin(%s?mode=307&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		liz.addContextMenuItems(cm, replaceItems=True) 	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok