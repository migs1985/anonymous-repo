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

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

def menu():
	addDir(traducao(2019),'http://www.ero-tik.com/newvideos.html',602,artfolder + 'videos.png',offset=234)
	addDir(traducao(2021),'http://www.ero-tik.com/topvideos.html',602,artfolder + 'fav.png',offset=288)
	addDir(traducao(2074),'-',603,artfolder + 'random.png',False)
	addDir(traducao(2028),'-',604,artfolder + 'cat.png')
	addDir(traducao(2022),'-',605,artfolder + 'search.png')
	
def pesquisa():
	keyb = xbmc.Keyboard('', traducao(2022)+':')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://www.ero-tik.com/search.php?keywords=' + str(parametro_pesquisa)
		listar_videos(url,145)
	
def cat():
	html = abrir_url('http://www.ero-tik.com/')
	match = re.compile('<li class=""><a href="(.+?)" class="">(.+?)</a></li>').findall(html)
	for url, name in match:
		addDir(name,url,602,artfolder + 'cat.png',offset=145)
	
def random_video():
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	html =  abrir_url('http://www.ero-tik.com/randomizer.php')
	img = re.compile('<meta property="og:image" content="(.+?)"').findall(html)[0]
	url = re.compile('<meta property="og:url" content="(.+?)"').findall(html)[0]
	title = re.compile('<meta property="og:title" content="(.+?)"').findall(html)[0]
	playvideo(title,url,img,1)
	
def listar_videos(url,offset):
	html = abrir_url(url)
	offset = re.compile('class="pm-thumb-fix pm-thumb-(.+?)">').findall(html)[0]
	match = re.compile('<a href="(.+?)" class="pm-thumb-fix pm-thumb-'+str(offset)+'"><span class="pm-thumb-fix-clip"><img src="(.+?)" alt="(.+?)"').findall(html)
	for link, img, title in match:
		addDir(title,link,601,img,False)
	try:
		nextpage = re.compile('<a href="(.+?)">&raquo;</a>').findall(html)[0]
		if not re.search('http://',nextpage): nextpage = 'http://www.ero-tik.com/' + nextpage
		addDir(traducao(2050),nextpage,602,artfolder + 'next.png',offset=offset)
	except: pass
	
def playvideo(name,url,iconimage,offset=0):
	if not offset: mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	url_video = videomega_resolver(url)
	mensagemprogresso.close()
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(url_video,liz)
	
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
			iframe = re.compile('"http://videomega.tv/iframe.php\?(.+?)"').findall(html)[0] + '&'
			ref = re.compile('ref=(.+?)&').findall(iframe)[0]
	
	ref_data={'Host':'videomega.tv',
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'Referer':referer}
	url = 'http://videomega.tv/iframe.php?ref=' + ref
	#url = 'http://videomega.tv/cdn.php?ref='+ref+'&width=638&height=431&val=1'
	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(abrir_url_tommy(url,ref_data))
	texto = urllib.unquote(code[0])
	try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
	except: url_video = '-'
	#try: url_legendas = re.compile('http://videomega.tv/servesrt.php\?s=(.+?).srt').findall(texto)[0] + '.srt'
	#except: url_legendas = '-'
	ref_data={'Host':url_video.split('/')[2],
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'Referer':'http://videomega.tv/player/jwplayer.flash.swf'}
	return url_video+headers_str(ref_data)

def headers_str(headers):
	start = True
	headers_str = ''
	for k,v in headers.items():
		if start:
			headers_str += '|'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
			start = False
		else: headers_str += '&'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
	return headers_str

'''	
addDir('Ero-tik','-',600,artfolder + 'erotik.png')

elif mode>=600 and mode <= 699: 
	erotik.mode(mode,name,url,iconimage,offset)
'''
def mode(mode,name,url,iconimage,offset):
	if mode==600: menu()
	elif mode==601: playvideo(name,url,iconimage)
	elif mode==602: listar_videos(url,offset)
	elif mode==603: random_video()
	elif mode==604: cat()
	elif mode==605: pesquisa()

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
		
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1,video=False,offset=0):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&offset="+str(offset)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	if video: 
		cm.append(('Download', 'XBMC.RunPlugin(%s?mode=205&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		liz.addContextMenuItems(cm, replaceItems=True) 
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok