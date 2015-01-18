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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,xbmcvfs,time,random,json
h = HTMLParser.HTMLParser()
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()

try:
	addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
	sys.path.append(addon_pdf)
	from pdf import pdf
	pdf = pdf()
except:
	dialog = xbmcgui.Dialog()
	dialog.ok("Error!","PDF Reader not found.","Please install it.")
	sys.exit(0)

addon_id = 'plugin.image.kiosk'
addon = Addon(addon_id)
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
if xbmc.getCondVisibility('system.platform.windows'): pastaperfil = pastaperfil.replace('\\','/')
if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
mensagemprogresso = xbmcgui.DialogProgress()

################################################## 

#MENUS############################################

def CATEGORIES():
	#listar('http://pdf-kiosk.com')
	listar_scribd('https://pt.scribd.com/gigatuga')
	
def listar_scribd(url):
	html = abrir_url(url)
	match = re.compile('''style="background-image: url\('(.+?)'\)"><div class="shadow_overlay"></div><div class="cell_data"><div class="document_title"><a href="(.+?)">(.+?)</a>''').findall(html)
	for img, link, title in match:
		addDir(title,link,3,img)
	
def scribd(url):
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	mensagemprogresso.create('Kiosk', 'A abrir ficheiro...')
	mensagemprogresso.update(0)
	html = abrir_url(url)
	if re.search('"format_ext">.TXT',html) and (not re.search('"format_ext">.PDF',html)):
		xbmcgui.Dialog().ok('Erro:', 'Impossível abrir ficheiro...')
		return
	total = int(re.compile('"page_count":(.+?),').findall(html)[0])
	imgs = re.compile('<img class="absimg" style=".+?" orig="(.+?)"/>').findall(html)
	i = len(imgs)
	mensagemprogresso.update(int((float(i)/total)*100))
	jsonp = re.compile('pageParams.contentUrl = "(.+?)"').findall(html)
	
	for j in jsonp:
		if mensagemprogresso.iscanceled():
			return
		host = j.split('/')[2]
		headers = {'Host':host,
				   'Connection':'keep-alive',
				   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
		img = re.compile('orig="(.+?)"').findall(net.http_GET(j,headers).content.replace('\\',''))[0]
		imgs.append(img)
		i += 1
		mensagemprogresso.update(int((float(i)/total)*100))
	mensagemprogresso.close()
	
	i = 1
	for p in imgs:
		addLink('Página '+str(i),p,p)
		i += 1

'''
Código antigo
'''
	
def listar(url):
	html = abrir_url(url)
	match = re.compile('<div class="grid-box-img"><a href="(.+?)" rel="bookmark" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)" class="attachment-full wp-post-image" alt=".+?"').findall(html)
	for link, title, img in match:
		title = title.replace('&#8211;','-').replace('&#8217;',"'")
		addDir(title,link,2,img,False)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def encontrar_fontes(url):
	html = abrir_url(url)
	try:
		texto = re.findall('<div class="su-box su-box-style-default"(.*?)<footer',html,re.DOTALL)[0]
		links = re.compile('href="(.+?)"').findall(texto)
	except:
		xbmcgui.Dialog().ok('Erro:', 'Fontes desconhecidas...')
		return
	url = []
	hosts = []
	for i in range(0,len(links)):
		if myresolvers(links[i]):
			url.append(links[i])
			hosts.append(myresolvers(links[i]))
	
	if len(hosts) == 0:
		xbmcgui.Dialog().ok('Erro:', 'Fontes desconhecidas...')
		return
	
	if len(hosts) == 1: index = 0
	else:
		index = xbmcgui.Dialog().select('Servidor:', hosts)
		if index == -1: return
	_myresolvers(url[index])
	
	
def myresolvers(url):
	if "uploaded.net" in url or 'ul.to' in url: return 'uploaded.net'
	elif "1fichier.com" in url: return '1fichier.com'
	elif "uploadable.ch" in url: return 'uploadable.ch'
	elif "uptobox.com" in url: return 'uptobox.com'
	elif "docdroid.net" in url: return 'docdroid.net'
	else: return None
	
def _myresolvers(url):
	#try:
	if "uploaded.net" in url or 'ul.to' in url: uploadednet(url)
	elif "1fichier.com" in url: onefichier_com(url)
	elif "uploadable.ch" in url: uploadable(url)
	elif "uptobox.com" in url: uptobox_com(url)
	elif "docdroid.net" in url: docdroid_net(url)
	else: return None
	#except: xbmcgui.Dialog().ok('Erro:', 'Erro ao aceder ao ficheiro...')
	
def docdroid_net(url):
	try: abrir_url(url)
	except:
		xbmcgui.Dialog().ok('Erro:', 'Documento não encontrado...')
		return
	final_url = url.replace('docdroid.net','docdroid.net/file/download').replace('.html','')
	headers = {'Host':'www.docdroid.net',
			   'Connection':'keep-alive',
			   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
			   'Referer':url}
	if download_headers(final_url,headers):
		pdf.pdf_read('temp',os.path.join(pastaperfil,'temp.pdf'))
	
def uptobox_com(url):
	form_values = {}
	for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)".*?>', abrir_url(url)):
		form_values[i.group(1)] = i.group(2)
	if form_values == {}:
		xbmcgui.Dialog().ok('Erro:', 'Documento não encontrado...')
		return
	try:
		html = net.http_POST(url, form_data=form_values).content
		texto = re.findall('<div align="center">(.*?)</div>',html,re.DOTALL)[0]
		final_url = re.compile('href="(.+?)"').findall(texto)[0]
		pdf.pdf_read('temp',final_url)
	except:
		xbmcgui.Dialog().ok('Erro:', 'Atingiu o limite máximo de downloads.','Tente novamente mais tarde...')
	
def uploadable(url):
	url2 = url.replace('/'+url.split('/')[-1],'')
	mensagemprogresso.create('Kiosk', 'A resolver link...')
	html = abrir_url(url)
	if re.search('404_removed',html):
		xbmcgui.Dialog().ok('Erro:', 'Documento não encontrado...')
		return
	form_values = {'downloadLink':'wait'}
	wait_time = net.http_POST(url, form_data=form_values).content
	wait_time = int(json.loads(wait_time)['waitTime'])
	if not addon.show_countdown(wait_time): return
	form_values = {'checkDownload':'check'}
	html = net.http_POST(url, form_data=form_values).content
	if re.search('showCaptcha',html):
		k = urllib.quote_plus('6LdlJuwSAAAAAPJbPIoUhyqOJd7-yrah5Nhim5S3')
		challenge = "http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cahcestop=%.17f" % (k, random.random())
		challengehtml = abrir_url(challenge)
		challengeToken = re.compile("challenge : '(.+?)'").findall(challengehtml)[0]
		captcha_url = 'http://www.google.com/recaptcha/api/image?c=' + challengeToken
		captcha_img = os.path.join(pastaperfil, "captcha.jpg")
		open(captcha_img, 'wb').write( net.http_GET(captcha_url).content)
		solver = InputWindow(captcha=captcha_img)
		try:os.remove(captcha_img)
		except: pass
		puzzle = solver.get()
		if puzzle:
			id = url.split('/')[-2]
			form_values = {'recaptcha_challenge_field':challengeToken,'recaptcha_response_field':puzzle,'recaptcha_shortencode_field':id}
			html = net.http_POST('http://www.uploadable.ch/checkReCaptcha.php', form_data=form_values).content
			if not re.search('"success":1',html):
				xbmcgui.Dialog().ok('Erro', 'Captcha errado!')
				return
			form_values = {'downloadLink':'show'}
			net.http_POST(url2, form_data=form_values)
			form_values = {'download':'normal'}
			
			req = urllib2.Request(url2, urllib.urlencode(form_values))
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
			res = urllib2.urlopen(req)
			final_url = res.geturl()
			pdf.pdf_read('temp',final_url)
	else:
		xbmcgui.Dialog().ok('Erro:', 'Atingiu o limite máximo de downloads.','Tente novamente mais tarde...')
		
def onefichier_com(url):
	html = abrir_url(url)
	if re.search('Le fichier demandé a été supprimé',html):
		xbmcgui.Dialog().ok('Erro:', 'Documento não encontrado...')
		return
	if re.search('Without Premium, you must wait between downloads',html):
		xbmcgui.Dialog().ok('Erro:', 'Atingiu o limite máximo de downloads.','Tente novamente mais tarde...')
		return
	form_values = {}
	for i in re.finditer('<input.*?type="(.*?)".*?value="(.*?)".*?>', html):
		form_values[i.group(1)] = i.group(2)
	if download(url,form_values):
		pdf.pdf_read('temp',os.path.join(pastaperfil,'temp.pdf'))
	
def uploadednet(url):
	k = urllib.quote_plus('6Lcqz78SAAAAAPgsTYF3UlGf2QFQCNuPMenuyHF3 ')
	challenge = "http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cahcestop=%.17f" % (k, random.random())
	challengehtml = abrir_url(challenge)
	challengeToken = re.compile("challenge : '(.+?)'").findall(challengehtml)[0]
	captcha_url = 'http://www.google.com/recaptcha/api/image?c=' + challengeToken
	captcha_img = os.path.join(pastaperfil, "captcha.jpg")
	open(captcha_img, 'wb').write( net.http_GET(captcha_url).content)
	solver = InputWindow(captcha=captcha_img)
	try:os.remove(captcha_img)
	except: pass
	puzzle = solver.get()
	if puzzle:
		form_values = {'recaptcha_challenge_field':challengeToken,'recaptcha_response_field':puzzle}
		id = url.split('/')[-1]
		html = net.http_POST('http://uploaded.net/io/ticket/captcha/' + id, form_data=form_values).content
		if re.search('You have reached',html) or re.search('limit-dl',html):
			xbmcgui.Dialog().ok('Erro:', 'Atingiu o limite máximo de downloads.','Tente novamente mais tarde...')
			return
		try: url_down = re.compile("url:'(.+?)'").findall(html)[0]
		except: 
			xbmcgui.Dialog().ok('Erro', 'Captcha errado!')
			return
		pdf.pdf_read('temp',url_down)

def download_headers(url,headers=None,form_values=None):
	return httpDownload(url, os.path.join(pastaperfil,'temp.pdf'), headers, dialogdown,form_values)
	
def httpDownload(url, filename, headers=None, reporthook=None,postData=None):
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	try:
		if headers==None:
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'}
		reqObj = urllib2.Request(url, postData, headers)
		fp = urllib2.urlopen(reqObj)
		headers = fp.info()

		tfp = open(filename, 'wb')
		result = filename, headers
		bs = 1024*8
		size = -1
		read = 0
		blocknum = 0
		start_time = time.time()
		if reporthook:
			if "content-length" in headers:
				size = int(headers["Content-Length"])
			reporthook(blocknum, bs, size, dp, start_time)

		while 1:
			block = fp.read(bs)
			if block == "": break
			read += len(block)
			tfp.write(block)
			blocknum += 1
			if reporthook:
				reporthook(blocknum, bs, size, dp, start_time)

		fp.close()
		tfp.close()
		del fp
		del tfp
	except:
		while os.path.exists(filename): 
			try: os.remove(filename); break 
			except: pass
		dp.close()
		return False
	dp.close()
	return True
		
def download(url,form_values):	
	mypath=os.path.join(pastaperfil,'temp.pdf')
	try: os.remove(mypath)
	except: pass	  
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
	data = urllib.urlencode(form_values)
	try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time),data=data)
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return False
	dp.close()
	return True

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
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
	
class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        xposition = 425
        yposition = 5
        hposition = 135
        wposition = 405
        self.img = xbmcgui.ControlImage(xposition,yposition,wposition,hposition,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard('','Captcha:')

    def get(self):
        self.show()
        time.sleep(3)
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        else:
            self.close()
            sys.exit(0)
        self.close()
        return False

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
	liz.setInfo( type="Image", infoLabels={ "Title": name } )
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
elif mode==1: listar(url)
elif mode==2: encontrar_fontes(url)
elif mode==3: scribd(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))