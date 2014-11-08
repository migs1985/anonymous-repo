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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,xbmcvfs
import brazzers
import fhdp
import streamxxx
import uppod
import boaf
import ioncube
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
if xbmc.getCondVisibility('system.platform.windows'): pastaperfil = pastaperfil.replace('\\','/')
mensagemprogresso = xbmcgui.DialogProgress()
entra_canais = selfAddon.getSetting('entra_canais')

nnm_list = 'http://nnm-list.ru/f/niu3uo4w'

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################

def CATEGORIES():
	addDir(traducao(2000),'-',21,artfolder + 'canais.png')
	addDir(traducao(2001),'-',1,artfolder + 'lista.png')
	addDir(traducao(2002),'-',101,artfolder + 'movie.png')
	addDir(traducao(2003),'-',22,artfolder + 'settings.png',False)
	if selfAddon.getSetting('pass') == "false": password()
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def videos():
	addDir("Brazzers",'-',200,artfolder + 'brazzers_icon.png')
	addDir("Free HD Porn",'-',300,artfolder + 'fhdp_icon.png')
	addDir("Streamxxx",'-',400,artfolder + 'streamxxx.png')
	addDir('BoaFoda.com','-',500,artfolder + 'boaf.png')
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def _ch(name):
	if selfAddon.getSetting(name) == "true":
		return True
	return False
	
def canais():
	if entra_canais == "true": addDir(traducao(2004),'-',0,artfolder + 'menu.png')
	
	if _ch('brazzerstv'): addDir("Brazzers TV",'-',4,artfolder + "brazzers.png",False)
	if _ch('brasileirinhas'): addDir("Brasileirinhas",'-',5,artfolder + "brasileirinhas.png",False)
	if _ch('sexyhot'): addDir("SexyHot",'-',6,artfolder + "sexyhot.png",False)
	if _ch('pboytv'): addDir("Playboy TV",'-',7,artfolder + "playboy.png",False)
	if _ch('pboytvchat'): addDir("Playboy TV Chat",'-',8,artfolder + "playboyhd.png",False)
	if _ch('penthousehd'): addDir("Penthouse HD",'-',9,artfolder + "penthouse.png",False)
	#if _ch('hot'): addDir("Hot",'-',10,artfolder + "hot.png",False)
	if _ch('hustlerhd'): addDir("Hustler HD",'-',11,artfolder + "hustlerhd.png",False)
	if _ch('viki'): addDir("Viki Enjoy Premium",'-',12,artfolder + "viki.png",False)
	if _ch('vietsex'): addDir("Viet Sex TV",'-',13,artfolder + "vietsextv.png",False)
	if _ch('bella'): addDir("Bella Club",'-',14,artfolder + "bellaclub.png",False)
	if _ch('bella2'): addDir("Bella Club 2",'-',15,artfolder + "bellaclub2.png",False)
	if _ch('butgo'): addDir("ButGO",'-',16,artfolder + "butgo.png",False)
	if _ch('filthon-adult'): addDir("Filthon Adult",'-',17,artfolder + "filthon.png",False)
	if _ch('filthon-adult-fetish'): addDir("Filthon Adult Fetish",'-',18,artfolder + "filthonfetish.png",False)
	if _ch('xxl'): addDir("XXL",'-',19,artfolder + "xxl.png",False)
	if _ch('frenchlover'): addDir("Frenchlover",'-',20,artfolder + "frenchlover.png",False)
	if _ch('dorceltv'): addDir("Dorcel TV",'-',23,artfolder + "dorceltv.png",False)
	if _ch('ipure'): addDir("iPure TV",'-',24,artfolder + "ipuretv.png",False)
	if _ch('private'): addDir("Private",'-',25,artfolder + "private.png",False)
	if _ch('privategold'): addDir("Private Gold",'-',26,artfolder + "privategold.png",False)
	if _ch('venus'): addDir("Venus",'-',27,artfolder + "venus.png",False)
	#if _ch('xdesire'): addDir("xDesire",'-',28,artfolder + "xdesire.png",False)
	#if _ch('blue-hustler'): addDir("Blue Hustler",'-',29,artfolder + "hustlerblue.png",False)
	if _ch('olala'): addDir("O-la-la",'-',30,artfolder + "olala.png",False)
	#if _ch('eroxxx'): addDir("Ero XXX",'-',31,artfolder + "eroxxx.png",False)
	if _ch('amateritv'): addDir("Amateri TV",'-',32,artfolder + "amateritv.png",False)
	if _ch('russian-nights'): addDir("Russian Nights",'-',33,artfolder + "russiannights.png",False)
	if _ch('hustlertv'): addDir("Hustler TV",'-',34,artfolder + "hustlertv.png",False)
	if _ch('sexzonehd'): addDir("Sexzone HD",'-',35,artfolder + "sexzonehd.png",False)
	if _ch('redlighthd'): addDir("Redlight HD",'-',36,artfolder + "redlighthd.png",False)
	if _ch('hallotv'): addDir("Hallo TV",'-',37,artfolder + "hallotv.png",False)
	if _ch('platinumtv'): addDir("Platinum TV",'-',38,artfolder + "platinumtv.png",False)
	if _ch('sexprive'): addDir("Sexprive Brasileirinhas",'-',40,artfolder + "sexprive.png",False)
	if _ch('nightclub'): addDir("Nightclub TV",'-',41,artfolder + "nightclub.png",False)
	if _ch('temptation'): addDir("Temptation TV",'-',42,artfolder + "temptationtv.png",False)
	if selfAddon.getSetting('gay') == 'false':
		#Conteúdo gay
		if _ch('filthon-gay'): addDir("Filthon Gay",'-',39,artfolder + "filthongay.png",False)
	xbmc.executebuiltin("Container.SetViewMode(500)")


###################################################################################
#LISTAS

def listas():
	addDir(traducao(2005)+" 1",'http://01.gen.tr/HasBahCa/XXX.m3u',2,artfolder + "1.png")
	'''
	try:
		html = abrir_url('https://www.dropbox.com/s/h6ln6hb8l0hl4wo/userbouquet.ilu_xxx_adult.tv')
		data=re.compile('<div class="filename shmodel-filename"><span id=".+?"></span></div><div class="meta">(.+?)&nbsp;&middot;&nbsp;.+?</div>').findall(html)[0]
		data = ' - ' + data.replace('months',traducao(2045)).replace('ago',traducao(2046)).replace('day',traducao(2047))
	except: data = ''
	'''
	#http://axenttv.ru/forum/24-365-10
	addDir(traducao(2005)+" 2",'http://anonymous-repo.googlecode.com/svn/trunk/adultstv/list.m3u',2,artfolder + "2.png")
	addDir(traducao(2005)+" 3",'-',3,artfolder + "3.png")
	addDir(traducao(2005)+" 4 - VOD",'http://01.gen.tr/HasBahCa/movies/XXX-VOD.m3u',2,artfolder + "4.png")
	addDir(traducao(2005)+" 5 - nnm-list.ru",nnm_list,104,artfolder + "5.png")
	
def lista_videos3(url):
	m3u = abrir_url(url).splitlines()
	for x in range(0,len(m3u)):
		if "#EXTINF:-1," in m3u[x] and '(Для взрослых)' in m3u[x]: 
			name = m3u[x].replace("#EXTINF:-1,","").replace('(Для взрослых)','').replace("\r","").replace("\n","")
			addLink(name,m3u[x+1].replace('rtmp://$OPT:rtmp-raw=',''),artfolder + "movie.png")
	
def lista_videos(url):
	m3u = abrir_url(url).splitlines()
	for x in range(0,len(m3u)):
		if "#EXTINF:-1," in m3u[x]: 
			name = m3u[x].replace("#EXTINF:-1,","").replace("\r","").replace("\n","")
			addLink(name,m3u[x+1].replace('rtmp://$OPT:rtmp-raw=',''),artfolder + "movie.png")
	
def lista_videos2():
	lista = abrir_url("https://dl.dropboxusercontent.com/s/h6ln6hb8l0hl4wo/userbouquet.ilu_xxx_adult.tv?dl=1&token_hash=AAGXNUUoQs_6kNFrZzSEo8OQjVwKSQcIrsgVM4VbsORgew&expiry=1400359776").splitlines()
	for x in range(0,len(lista)):
		if "#DESCRIPTION: " in lista[x]:
			name = lista[x].replace("#DESCRIPTION: ","").replace("\r","").replace("\n","")
			addLink(name,lista[x-1].replace('rtmp://$OPT:rtmp-raw=','').replace("#SERVICE 4097:0:1:0:0:0:0:0:0:0:","").replace("%3a",":").replace("...",""),artfolder + "movie.png")

###############################################################
#CANAIS

'''
FONTES
http://www.widih.org/tv-channel/all/adult
http://verdirectotv.com/
http://www.tvtuga.org/
http://live-cricketbd.blogspot.pt/p/blog-page_12.html
http://tvxat.org/tv-online/adulto/
http://tutvgratis.tv/
http://tvxlive.blogspot.pt/p/live-channels.html
---www.portalzuca.net/canais/canal5.html
-http://www.lovetv.ml/
http://ero-tv.org/
http://alfabass.at.ua/index/
http://www.funmastii.com/search/label/Live%20Adult%20TV
'''

def brazzers_tv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih",'nnm-list.ru',traducao(2005)+' 2'])
	if index==0: streamurl=widih_resolver("http://www.widih.org/watch-tv/1731/brazzers-18+live+tv+streaming")
	elif index==1: streamurl=nnm_list_resolver(name)
	elif index==2: streamurl=myresolver(name)
	else: return
	play(name,streamurl,iconimage)
	
def brasileirinhas(name,iconimage):
	#tvxat
	'''url = "http://tvxat.org/assistir-brasileirinhas-online-hd"
	embed = "http://"+re.compile('<iframe src="(.+?)"').findall(abrir_url(url))[0].replace("http","").replace("//","").replace(":","")
	codigo_fonte = abrir_url(embed)
	rtmp = "rtmp://" + re.compile('file: "rtmp://(.+?)"').findall(codigo_fonte)[0]
	swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
	streamurl = rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + embed'''
	#livestream
	url = "http://livestreamcast.org/embed.php?c=brasileirinhas"
	streamurl = livestream_resolver(url)
	play(name,streamurl,iconimage)
	
def sexyhot(name,iconimage):
	url = "http://livestreamcast.org/embed.php?c=sexhothd"
	streamurl = livestream_resolver(url)
	play(name,streamurl,iconimage)
	
def playboy(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Livestream","ponlatv", "TVtuga","ero-tv"])
	if index == 0:
		url = "http://livestreamcast.org/embed.php?c=pboytv"
		streamurl = livestream_resolver(url)
	elif index == 1:
		url = "http://verdirectotv.com/canales/playboy.html"
		streamurl = ponlatv_resolver(url)
	elif index == 2:
		url= "http://www.tvtuga.org/playboy-tv/"
		streamurl = tvtuga_resolver(url)
	elif index == 3:
		url= "http://ero-tv.org/playboytv_live/"
		streamurl = ero_tv_resolver(url)
	else: return
	play(name,streamurl,iconimage)
	
def playboy_hd(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2007), ["Playboy HD 1", "Playboy HD 2", "Playboy HD 3", "Playboy HD 4", "Playboy HD 5"])
	if index == -1: return
	url = "http://livestreamcast.org/embed.php?c=playboyhd00" + str(index+1)
	streamurl = livestream_resolver(url)
	play(name+' '+str(index+1),streamurl,iconimage)
	
def penthouse(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["TVtuga","Live-Cricketbd","ero-tv"])
	if index==0:
		url = "http://www.tvtuga.org/penthouse-tv/"
		streamurl = tvtuga_resolver(url)
	elif index==1:
		url ='http://live-cricketbd.blogspot.pt/2014/03/penthouse.html'
		streamurl = livectv_resolver(url)
	elif index==2:
		url = 'http://ero-tv.org/penthouse_online/'
		streamurl = ero_tv_resolver(url)
	else: return
	play(name,streamurl,iconimage)
	
def hot(name,iconimage):
	return
	
def hustlerhd(name,iconimage):
	url = "http://verdirectotv.com/canales/hustlertv.html"
	streamurl = ponlatv_resolver(url)
	play(name,streamurl,iconimage)
	
def viki_enjoy_premium(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih", "ero-tv"])
	if index == 0:
		url = "http://www.widih.org/watch-tv/975/viki-enjoy-premium-hd%20live%20tv%20streaming"
		streamurl=widih_resolver(url)
	elif index == 1:
		url = "http://ero-tv.org/dorceltv_live/"
		streamurl=ero_tv_resolver(url)
	else: return
	play(name,streamurl,iconimage)
	
def vietsextv(name,iconimage):
	url = "http://www.tvtuga.org/viki-enjoy-premium/"
	streamurl = tvtuga_resolver(url)
	play(name,streamurl,iconimage)
	
def bella_club(name,iconimage):
	url = "http://live-cricketbd.blogspot.pt/2014/03/bellaclub.html"
	streamurl = livectv_resolver(url)
	play(name,streamurl,iconimage)
	
def bella_club2(name,iconimage):
	url = "http://live-cricketbd.blogspot.pt/2014/03/bella-club-2-18.html"
	streamurl = livectv_resolver(url)
	play(name,streamurl,iconimage)
	
def butgo(name,iconimage):
	url = "http://www.widih.org/watch-tv/1404/but-go-hd+live+tv+streaming"
	streamurl=widih_resolver(url)
	play(name,streamurl,iconimage)
	
def filthon_adult(name,iconimage):
	streamurl=widih_resolver("http://www.widih.org/watch-tv/3461/filthon-adult+live+tv+streaming")
	play(name,streamurl,iconimage)
	
def filthon_adult_fetish(name,iconimage):
	streamurl=widih_resolver("http://www.widih.org/watch-tv/2040/filthon-adult-fetish+live+tv+streaming")
	play(name,streamurl,iconimage)
	
def xxl(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih", "ero-tv"])
	if index==0: streamurl=widih_m3u("http://www.widih.org/watch-tv/4257/xxl-18+live+tv+streaming")
	elif index==1: streamurl = ero_tv_resolver('http://ero-tv.org/xxl-tv-live/')
	else: return
	play(name,streamurl,iconimage)
	
def french_lover(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih",traducao(2005)+' 2'])
	if index==0: streamurl=widih_resolver("http://www.widih.org/watch-tv/2400/french-lover+live+tv+streaming")
	elif index==1: streamurl=myresolver(name)
	else: return
	play(name,streamurl,iconimage)
	
def dorcel_tv(name,iconimage):
	m3u8=widih_m3u("http://www.widih.org/watch-tv/1746/dorcel-tv-18+live+tv+streaming")
	play(name,m3u8,iconimage)
	
def ipuretv(name,iconimage):
	m3u8=widih_m3u("http://www.widih.org/watch-tv/1722/ipure-tv-hd+live+tv+streaming")
	play(name,m3u8,iconimage)
	
def private(name,iconimage):
	streamurl=livestream_resolver("http://livestreamcast.org/embed.php?c=privatee&vw=100%&vh=100%")
	play(name,streamurl,iconimage)
	
def private_gold(name,iconimage):
	url="http://tutvgratis.tv/adultos/private-gold"
	ucaster_link,referer = tutv_resolver(url)
	if ucaster_link == 'erro': return
	streamurl=ucaster_resolver(ucaster_link,referer)
	play(name,streamurl,iconimage)
	
def venus(name,iconimage):
	url="http://tutvgratis.tv/adultos/venus/"
	ucaster_link,referer = tutv_resolver(url)
	if ucaster_link == 'erro': return
	streamurl=ucaster_resolver(ucaster_link,referer)
	play(name,streamurl,iconimage)
	
def xdesire(name,iconimage):
	streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/daring.html")
	play(name,streamurl,iconimage)
	
def hustler_blue(name,iconimage):
	streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/09/blue-hustler.html")
	play(name,streamurl,iconimage)

def olala(name,iconimage):
	streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/o-la-la-18.html")
	play(name,streamurl,iconimage)
	
def eroxxx(name,iconimage):
	streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/eroxx-hd-18.html")
	play(name,streamurl,iconimage)
	
def amateritv(name,iconimage):
	try:
		url = "http://www.amateri.cz/?a=tv"
		streamurl = re.compile('"src" value="(.+?)">').findall(abrir_url(url))[0]
		play(name,streamurl,iconimage)
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	
def russiannights(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["TVtuga","ero-tv"])
	if index==0: streamurl=widih_resolver("http://www.widih.org/watch-tv/1880/ruskaja-noc-russian-nights-18+live+tv+streaming")
	elif index==1: streamurl = ero_tv_resolver('http://ero-tv.org/russian_night_online/')
	else: return
	play(name,streamurl,iconimage)
	
def hustlertv(name,iconimage):
	streamurl = livestream_resolver("http://livestreamcast.org/embed.php?c=hustlerr&vw=100%&vh=100%")
	play(name,streamurl,iconimage)
	
def sexzonehd(name,iconimage):
	streamurl = livestream_resolver("http://livestreamcast.org/embed.php?c=sexzonehd&vh=100%&vw=100%")
	play(name,streamurl,iconimage)
	
def redlighthd(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/redlight_online/')
	play(name,streamurl,iconimage)
	
def hallotv(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/hallo-tv_online/')
	play(name,streamurl,iconimage)
	
def platinum_tv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["ero-tv",'nnm-list.ru'])
	if index==0: streamurl=ero_tv_resolver('http://ero-tv.org/platinum_tv_online/')
	elif index==1: streamurl=nnm_list_resolver(name)
	else: return
	play(name,streamurl,iconimage)
	
def filthon_gay(name,iconimage):
	streamurl = 'rtmp://live190.la3.origin.filmon.com:8086/live/246.high.stream'
	play(name,streamurl,iconimage)
	
def sexprive(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/brasileirinhas_tv_online/')
	play(name,streamurl,iconimage)
	
def nightclub(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ['nnm-list.ru',traducao(2005)+' 2'])
	if index==0: streamurl=nnm_list_resolver('Ночной клуб')
	elif index==1: streamurl=myresolver(name)
	else: return
	play(name,streamurl,iconimage)
	
def temptationtv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ['nnm-list.ru',traducao(2005)+' 2'])
	if index==0: streamurl=nnm_list_resolver('Искушение')
	elif index==1: streamurl=myresolver(name)
	else: return
	play(name,streamurl,iconimage)
	
########################################################################
#RESOLVERS
def nnm_list_resolver(name):
	try:
		mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
		m3u = abrir_url(nnm_list).splitlines()
		for x in range(0,len(m3u)):
			if re.search(name,m3u[x]): 
				return m3u[x+1]
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'

def myresolver(name):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	m3u = abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/adultstv/list.m3u').splitlines()
	for x in range(0,len(m3u)):
		if name in m3u[x]: 
			return m3u[x+1]
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'

def livectv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:
		rtmp = re.compile('file: "(.+?)"').findall(codigo_fonte)[0]
		streamurl = rtmp + ' live=true swfVfy=1'
		return streamurl
	except: pass
	try:
		rtmp = re.compile("'file': '(.+?)'").findall(codigo_fonte)[0]
		streamurl = rtmp + ' live=true swfVfy=1'
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return "erro"
		
def ero_tv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	html = abrir_url(url)
	try:
		st = re.compile('st=(.+?)&').findall(html)[0]
		info = uppod.decode(abrir_url(uppod.decode(st)))
		try: stkey = re.compile('"stkey":"(.+?)"').findall(info)[0]
		except: stkey = ''
		rtmp_enc = re.compile('file=(.+?)"').findall(html)[0]
		file = uppod.decode(rtmp_enc.replace(stkey,''))
		if '.m3u8' in file: return m3u8(file)
		swf = re.compile('data="(.+?)"').findall(html)[0]
		streamurl=file + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + url
		return streamurl
	except: pass
	try:
		file = re.compile('file=(.+?)"').findall(html)[0]
		if 'livestreamcast.org' in file:
			swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
			streamurl = file + ' live=true swfVfy=1 swfUrl=' + swf 
			return streamurl.replace('  ',' ')
	except: pass
	try:
		file = re.compile('file: "(.+?)"').findall(html)[0]
		swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
		streamurl = file + ' live=true swfVfy=1 swfUrl=' + swf 
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return "erro"
		
def tvxlive_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		streamurl=re.compile('target="(.+?)"').findall(abrir_url(url))[0]
		return streamurl
	except: 
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"

def tutv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		embed=re.compile('<iframe src="(.+?)"').findall(abrir_url(url))[0]
		code = urllib.unquote(re.compile("document.write\(unescape\('(.+?)'\)\)\;").findall(abrir_url(embed))[0])
		url2 = re.compile('src="(.+?)"').findall(code)[0]
		code2 = abrir_url(url2)
		type = re.compile('type: "(.+?)"').findall(code2)[0]
		action = re.compile('action: "(.+?)"').findall(code2)[0]
		channelID = re.compile('channelID: (.+?) }').findall(code2)[0]
		url3 = "http://tutvgratis.tv/embed/?type=%s&action=%s&channelID=%s" % (type,action,channelID)
		referer = re.compile('"URL":"(.+?)"').findall(abrir_url(url3))[0]
		code3=urllib.unquote(re.compile("document.write\(unescape\('(.+?)'\)\)\;").findall(abrir_url(referer))[1])
		ucaster_link = 'http://www.ucaster.eu/embedded/' + re.compile("channel='(.+?)'").findall(code3)[0] + '/1/600/430'
		return [ucaster_link,referer]
	except: 
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return ["erro","erro"]

def ucaster_resolver(url,referer):
	try:
		ref_data = {'Referer': referer,'User-Agent':user_agent}
		html= abrir_url_tommy(url,ref_data)
		swf = 'http://www.ucaster.eu'+re.compile('SWFObject\("(.+?)"').findall(html)[0]
		ch = re.compile("so.addParam\('FlashVars', 'id=(.+?)&s=(.+?)&").findall(html)[0]
		playpath = "%s?id=%s" % (ch[1],ch[0])
		rtmp='rtmp://'+re.compile(".*redirect=([\.\d]+).*").findall(abrir_url('http://www.ucaster.eu:1935/loadbalancer'))[0]+'/live'
		streamurl=rtmp + ' playPath=' + playpath + ' swfVfy=1 conn=S:OK live=true swfUrl=' + swf + ' pageUrl=' + url
		return streamurl
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"

def widih_m3u(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		m3u=re.compile("'file': '(.+?)'").findall(abrir_url(url))[0]
		return m3u8(m3u)
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return 'erro'
	
def widih_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:
		rtmp=re.compile("'file': '(.+?)'").findall(codigo_fonte)[0]
		if "m3u8" in rtmp: return widih_m3u(url)
		swf = re.compile("'flash', src: '(.+?)'").findall(codigo_fonte)[0]
		streamurl=rtmp + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + url
	except:
		try: streamurl="http://"+re.compile('target="http://(.+?)"').findall(codigo_fonte)[0]
		except: 
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return "erro"
	return streamurl

def ponlatv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		referer = re.compile('src="(.+?)"></iframe>').findall(abrir_url(url))[0]
		link="http://www.9stream.com/"+re.compile('src="http://www.9stream.com/(.+?)"').findall(abrir_url(referer))[0]
		embed_url = re.compile("src='(.+?)'").findall(abrir_url(link))[0]
		ref_data = {'Referer':referer,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36','Host': 'www.9stream.com','Connection': 'Keep-Alive'}
		embed = abrir_url_tommy(embed_url,ref_data)
		if re.search('Page protected by ionCube',embed): embed = ioncube.open(embed)
		rtmp = re.compile('\'streamer\': "(.+?)"').findall(embed)[0].replace("\\","")
		if rtmp[-1] != "/": rtmp = rtmp + "/"
		playpath = re.compile("'file': '(.+?)'").findall(embed)[0]
		swf = re.compile("'flash', src: '(.+?)'").findall(embed)[0]
		urltoken = re.compile('getJSON\("(.+?)"').findall(embed)[0]
		token = re.compile('"token":"(.+?)"').findall(abrir_url_tommy(urltoken,ref_data))[0]
		streamurl=rtmp + playpath + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 pageUrl=' + embed_url
		return streamurl
	except: 
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return 'erro'
	
def tvtuga_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try: rtmp = "rtmp://" + re.compile('flashvars="file=rtmp://(.+?)"').findall(codigo_fonte)[0].replace("&#038;","").replace("id=","").replace("&amp;","").replace("autostart=true","")
	except:
		try:rtmp = "rtmpe://" + re.compile('flashvars="file=rtmpe://(.+?)"').findall(codigo_fonte)[0].replace("&#038;","").replace("id=","").replace("&amp;","").replace("autostart=true","")
		except: 
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return 'erro'
	swf = "http://www.tvtuga.org/asx/player.swf"
	streamurl = rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + url
	return streamurl
	
def livestream_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:rtmp = "rtmp://" + re.compile('file: "rtmp://(.+?)"').findall(codigo_fonte)[0]
	except:
		try: return "http://" + re.compile('file: "http://(.+?)"').findall(codigo_fonte)[0]
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return "erro"
	swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
	streamurl = rtmp + ' live=true swfVfy=1 swfUrl=' + swf 
	return streamurl
	
###################################################################################
#FUNCOES
	
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
		if len(qualidade)==0:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return "erro"
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
	
def check_version():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo-adults/plugin.video.adultstv/addon.xml')
		match=re.compile('version="(.+?)"').findall(codigo_fonte)[1]
	except: match='error'
	if match=='error': xbmc.executebuiltin('Notification("   '+traducao(2059)+'","   '+traducao(2060)+'",3000,"'+artfolder+'version.png")')
	elif match!=selfAddon.getAddonInfo('version'): xbmc.executebuiltin('Notification("   '+traducao(2061)+' ('+match+')","   '+traducao(2062)+'",3000,"'+artfolder+'version.png")')
	
def first_run():
	if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
	if not os.path.exists(os.path.join(pastaperfil,"passwd.txt")):
		savefile("passwd.txt","<flag='false'>")
	
def password():
	if pass_status() == False: addDir(traducao(2013),'-',100,artfolder + 'password.png',False)
	else: addDir(traducao(2014),'-',100,artfolder + 'password.png',False)
	
def pass_status():
	try:
		if re.compile("flag='(.+?)'").findall(openfile("passwd.txt"))[0] == "true": return True
	except: return True
	return False

def check_pass():
	if pass_status() == False: return
	try: check = re.compile("password='(.+?)'").findall(openfile("passwd.txt"))[0]
	except: sys.exit(0)
	keyb = xbmc.Keyboard('', traducao(2015)) 
	keyb.setHiddenInput(True)
	keyb.doModal()
	if (keyb.isConfirmed()): password = keyb.getText()
	else: sys.exit(0)
	if password != check:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2016))
		sys.exit(0)
	
def change_pass_status():
	if pass_status() == False:
		keyb = xbmc.Keyboard('', traducao(2017)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		if password == '' or "'" in password:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2018))
			return
		savefile("passwd.txt","<flag='true' password='%s'>" % password)
	else: 
		check = re.compile("password='(.+?)'").findall(openfile("passwd.txt"))[0]
		keyb = xbmc.Keyboard('', traducao(2015)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		if password == '':
			xbmcgui.Dialog().ok(traducao(2010), traducao(2018))
			return
		if password == check: savefile("passwd.txt","<flag='false'>")
		else: xbmcgui.Dialog().ok(traducao(2010), traducao(2016))	
	xbmc.executebuiltin("Container.Refresh")
	
def savefile(filename, contents,pastafinal=pastaperfil):
	try:
		destination = os.path.join(pastafinal,filename)
		fh = open(destination, 'wb')
		fh.write(contents)  
		fh.close()
	except: print "falhou a escrever txt"
	
def openfile(filename,pastafinal=pastaperfil):
	try:
		destination = os.path.join(pastafinal, filename)
		fh = open(destination, 'rb')
		contents=fh.read()
		fh.close()
		return contents
	except:
		print "Falhou a abrir txt"
		return None
	
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
	#streamurl += ' timeout=15'
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	'''
	liz.setInfo('video', {'Title': name })
	liz.setProperty('IsPlayable', 'true')
	liz.setPath(path=streamurl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
	'''
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(streamurl,liz)
	
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
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except: return 'erro'

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
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
offset=None
letra=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: offset=int(params["offset"])
except: pass
try: letra=urllib.unquote_plus(params["letra"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Offset: "+str(offset)
print "Letra: "+str(letra)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################
	
if mode==None or url==None or len(url)<1: 
	first_run()
	check_pass()
	check_version()
	if entra_canais == "false": CATEGORIES()
	else: canais()
elif mode==0: CATEGORIES()
elif mode==1: listas()
elif mode==2: lista_videos(url)
elif mode==3: lista_videos2()
elif mode==104: lista_videos3(url)
elif mode==100: change_pass_status()
elif mode==101: videos()
#CANAIS
elif mode==4: brazzers_tv(name,iconimage)
elif mode==5: brasileirinhas(name,iconimage)
elif mode==6: sexyhot(name,iconimage)
elif mode==7: playboy(name,iconimage)
elif mode==8: playboy_hd(name,iconimage)
elif mode==9: penthouse(name,iconimage)
elif mode==10: hot(name,iconimage)
elif mode==11: hustlerhd(name,iconimage)
elif mode==12: viki_enjoy_premium(name,iconimage)
elif mode==13: vietsextv(name,iconimage)
elif mode==14: bella_club(name,iconimage)
elif mode==15: bella_club2(name,iconimage)
elif mode==16: butgo(name,iconimage)
elif mode==17: filthon_adult(name,iconimage)
elif mode==18: filthon_adult_fetish(name,iconimage)
elif mode==19: xxl(name,iconimage)
elif mode==20: french_lover(name,iconimage)
elif mode==21: canais()
elif mode==22: selfAddon.openSettings()
elif mode==23: dorcel_tv(name,iconimage)
elif mode==24: ipuretv(name,iconimage)
elif mode==25: private(name,iconimage)
elif mode==26: private_gold(name,iconimage)
elif mode==27: venus(name,iconimage)
elif mode==28: xdesire(name,iconimage)
elif mode==29: hustler_blue(name,iconimage)
elif mode==30: olala(name,iconimage)
elif mode==31: eroxxx(name,iconimage)
elif mode==32: amateritv(name,iconimage)
elif mode==33: russiannights(name,iconimage)
elif mode==34: hustlertv(name,iconimage)
elif mode==35: sexzonehd(name,iconimage)
elif mode==36: redlighthd(name,iconimage)
elif mode==37: hallotv(name,iconimage)
elif mode==38: platinum_tv(name,iconimage)
elif mode==39: filthon_gay(name,iconimage)
elif mode==40: sexprive(name,iconimage)
elif mode==41: nightclub(name,iconimage)
elif mode==42: temptationtv(name,iconimage)
#Brazzers Videos
elif mode==200: brazzers.brazzers_menu()
elif mode==201: brazzers.listar_videos(url)
elif mode==202: brazzers.encontrar_fontes(name,url,iconimage)
elif mode==203: brazzers.pesquisa()
elif mode==204: brazzers.play_tv()
elif mode==205: brazzers.download(name,url)
elif mode==206: brazzers.selfAddon.openSettings()
elif mode==207: brazzers.cat()
#Free HD Porn
elif mode==300: fhdp.fhdp_menu()
elif mode==301: fhdp.listar_videos(url)
elif mode==302: fhdp.encontrar_fontes(name,url,iconimage)
elif mode==303: fhdp.pesquisa()
elif mode==304: fhdp.listar_estudios()
elif mode==305: fhdp.listar_actrizes()
elif mode==306: fhdp.listar_categorias()
elif mode==307: fhdp.download(name,url)
#Stream XXX
elif mode==400: streamxxx.menu()
elif mode==402: streamxxx.listar_videos(url)
elif mode==401: streamxxx.listar_fontes(name,url,iconimage)
elif mode==403: streamxxx.pesquisa()
elif mode==404: streamxxx.clips()
#Boa foda
elif mode==500: boaf.menu()
elif mode==501: boaf.recentes(url)
elif mode==502: boaf.listar_fontes(name,url,iconimage)
elif mode==503: boaf.listar_videos(url)
elif mode==504: boaf.pesquisa()
elif mode==505: boaf.pornstars()
elif mode==506: boaf.listar_pornstars(name,url,offset,letra)
elif mode==507: boaf.cat()
elif mode==508: boaf.estudios()
elif mode==509: boaf.listar_estudios(url)
elif mode==510: boaf.listar_estudios2(offset)
elif mode==511: boaf.videos_recentes(offset)
elif mode==512: boaf.listar_videos2(url,offset)
elif mode==513: boaf.settings()
elif mode==514: boaf.listar_videos_pornstars(url,offset)
elif mode==515: boaf.listar_videos_estudios(url,offset)
xbmcplugin.endOfDirectory(int(sys.argv[1]))