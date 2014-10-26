#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
 Copyright 2014 Anonymous

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmcaddon,xbmc,xbmcvfs,xbmcgui,requests,re,os,urllib2,urllib,time

class utilis:
	
	'''
	How to import:
	from anonutilis.utilis import utilis
	utilis = utilis(addon_id)
	
	where addon_id = 'plugin.video.myaddon'
	'''

	def __init__(self, addon_id):
		self.addon_id = addon_id
		self.selfAddon = xbmcaddon.Addon(id='script.module.anonutilis')
		self.addon = xbmcaddon.Addon(id=addon_id)
		self.addon_name = self.addon.getAddonInfo('name')
		
		self.pastaperfil = xbmc.translatePath(self.selfAddon.getAddonInfo('profile')).decode('utf-8')
		if xbmc.getCondVisibility('system.platform.windows'): self.pastaperfil = self.pastaperfil.replace('\\','/')
		if not xbmcvfs.exists(self.pastaperfil): xbmcvfs.mkdir(self.pastaperfil)
	
	'''
	Creates a text 'box'
	text = Text to display
	name = Description of text (Optional).
	'''
	
	def text(self,text,name=''):
		try:
			xbmc.executebuiltin("ActivateWindow(10147)")
			window = xbmcgui.Window(10147)
			xbmc.sleep(100)
			titulo = self.addon_name
			if name != '': titulo += ' - ' + name
			window.getControl(1).setLabel(titulo)
			window.getControl(5).setText(text)
		except: pass
		
	'''
	Display an image
	url = Url of image to display
	Supported formats: '.jpg','.png','.gif','.bmp'
	'''
		
	def playimage(self,url):
		try:
			if re.search('.gif',url):
				listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=url)
				player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
				player.play(url,listitem)
				return
			xbmc.executebuiltin("ActivateWindow(busydialog)")
			extensao = ['.jpg','.png','.gif','.bmp']
			temp = ''
			for x in range(0,len(extensao)):
				if re.search(extensao[x],url): temp='temp' + extensao[x]
			if temp == '': 
				print 'Error: Unknown image extension'
				xbmc.executebuiltin("Dialog.Close(busydialog)")
				return
			for ext in extensao:
				try:os.remove(os.path.join(self.pastaperfil,'temp'+ext))
				except:pass	
			mypath = os.path.join(self.pastaperfil,temp)
			with open(mypath, 'wb') as handle:
				response = requests.get(url, stream=True)
				if not response.ok: 
					print 'Error: Response Error'
					xbmc.executebuiltin("Dialog.Close(busydialog)")
					return
				for block in response.iter_content(1024):
					if not block: break
					handle.write(block)
			xbmc.executebuiltin("Dialog.Close(busydialog)")
			xbmc.executebuiltin("SlideShow("+self.pastaperfil+")")	
		except: xbmc.executebuiltin("Dialog.Close(busydialog)")
		
	'''
	Returns XBMC bit version
	Ex: 'x32' or 'x64'
	If an error occurs, it returns 'Error'
	'''
		
	def xbmc_bit_version(self):
		try:
			log_path = xbmc.translatePath('special://logpath')
			log = os.path.join(log_path, 'xbmc.log')
			f = open(log,"r")
			aux = f.readlines()
			f.close()
			try: 
				bits = re.compile('XBMC (.+?) build').findall(aux[3])[0]
				if bits == "x32" or bits == "x64": return bits
			except: pass
			try: 
				bits = re.compile('Kodi (.+?) build').findall(aux[3])[0]
				if bits == "x32" or bits == "x64": return bits
			except: pass
			try:
				i = aux[3].find("-bit version", 0)
				bits = "x"+aux[3][i-2]+aux[3][i-1]
				if bits == "x32" or bits == "x64": return bits
			except: pass
			return "Error"
			print "Error: XBMC bit version not found"
		except: 
			return "Error"
			print "Error: Unable to open log"
	
	'''
	Simple url opener
	'''
	
	def abrir_url(self,url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
		
	'''
	Returns your addon (online) version
	Useful to know if the addon is up to date.
	xml = url of addon xml
	'''
		
	def addon_version(self, xml = ''):
		'''The next line is for my addons :P'''
		if xml == '': xml = 'http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/'+self.addon_id+'/addon.xml'
		try:
			codigo_fonte=self.abrir_url(xml)
			match=re.compile('version="(.+?)"').findall(codigo_fonte)[1]
		except: 
			match='Error: Version not found'
			print match
		return match
		
	'''
	Download with progress
	url = file url; ex: http://mysite.com/image.jpg
	down path = Final file location; ex: C:/Users/User/Desktop/image.jpg
	str1 and str2 are both optional. Their current language is Portuguese; ex str1='Estimated Time:' str2='of'
	'''
		
	def download(self,url,down_path,str1='Tempo estimado:',str2='de'):
		if os.path.isdir(down_path) is True:
			print 'Error: Path was a dir path'
			return
			
		if os.path.isfile(down_path) is True: 
			print 'Error: Theres already a file with the same name'
			return
				  
		dp = xbmcgui.DialogProgress()
		dp.create('Download')
		start_time = time.time()
		try: urllib.urlretrieve(url, down_path, lambda nb, bs, fs: self._dialogdown(nb, bs, fs, dp, start_time,str1,str2))
		except:
			while os.path.exists(down_path): 
				try: os.remove(down_path); break 
				except: pass
			dp.close()
			return
		dp.close()

	def _dialogdown(self,numblocks, blocksize, filesize, dp, start_time,str1,str2):
		try:
			percent = min(numblocks * blocksize * 100 / filesize, 100)
			currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
			kbps_speed = numblocks * blocksize / (time.time() - start_time) 
			if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
			else: eta = 0 
			kbps_speed = kbps_speed / 1024 
			total = float(filesize) / (1024 * 1024) 
			mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,str2,total) 
			e = ' (%.0f Kb/s) ' % kbps_speed 
			tempo = str1 + ' %02d:%02d' % divmod(eta, 60) 
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