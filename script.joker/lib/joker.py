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

'''
IMPORT:
from joker import joker
joker = joker()

PLAY:
joker.play(url)

XML:
<import addon="script.module.requests"/>
<import addon="script.joker"/>
'''

import requests
import json
import xbmc
import xbmcgui
import sys
import xbmcplugin

class joker:
	def play(self,magnet,name='',iconimage=''):
		self._start()
		print 'Magnet: '+magnet
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Joker', 'Opening media.','Please wait...')
		mensagemprogresso.update(0)
		url = "http://joker.org/api/torrs/checklink"
		data = {'link': magnet,
				'dwsubs': 'False'}
		
		headers = {'Host':'joker.org',
				   'Connection':'keep-alive',
				   'Accept': 'application/json, text/plain, */*',
				   'Origin':'joker.org',
				   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
				   'Content-type': 'application/json;charset=UTF-8',
				   'Referer':'http://joker.org/',
				   'Accept-Encoding':'gzip,deflate'}
				   
		r = requests.post(url, data=json.dumps(data), headers=headers)
		r_json = r.json()
		status = r_json['status']
		try: print 'Status: '+str(status)+' | Message: '+r_json['message']
		except: print 'Status: '+str(status)
		while(status != 3):
			mensagemprogresso.update(0,r_json['message'])
			if mensagemprogresso.iscanceled():
				print 'Canceled by user'
				self._end()
				return
			if status == -1:
				xbmcgui.Dialog().ok("Error:", "Invalid torrent or magnet")
				print 'Invalid torrent or magnet'
				self._end()
				return
			xbmc.sleep(3000)
			r = requests.post(url, data=json.dumps(data), headers=headers)
			r_json = r.json()
			status = r_json['status']
			try: print 'Status: '+str(status)+' | Message: '+r_json['message']
			except: print 'Status: '+str(status)

		mensagemprogresso.update(50,'Opening media.','Please wait...')
		try:
			id = r_json['message']['vids'][0]['files'][0]['uuid']
			ip = r_json['message']['server']
			if name == '':
				try: name = r_json['message']['meta']['title']
				except: 
					try: name = r_json['message']['vids'][0]['name']
					except: name = 'Joker - Video'
			cookies = r.cookies['martha']
			url_vid = 'http://'+ip+'/v/'+id+'.mp4'
			print 'Trying to play: '+url_vid
			print 'Name: '+name
			print 'Iconimage: '+iconimage
			url_video = url_vid + '|Host='+ip+'&Connection=keep-alive&Accept=*/*&User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36&Referer=http://joker.org/&Accept-Encoding=identity;q=1, *;q=0&Cookie=martha='+cookies+';'
			mensagemprogresso.update(100)
			mensagemprogresso.close()
			self._end()
			playlist = xbmc.PlayList(1)
			playlist.clear()
			listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
			listitem.setProperty('mimetype', 'video/x-msvideo')
			listitem.setProperty('IsPlayable', 'true')
			playlist.add(url_video, listitem)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
			player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
			player.play(playlist)
		
		except: 
			mensagemprogresso.close()
			xbmcgui.Dialog().ok("Error:", "Unable to open torrent!")
			print 'Error opening url'
			self._end()
		
	def _start(self):
		print '==============================================================================='
		print '===                                  Joker                                  ==='
		print '==============================================================================='
		
	def _end(self):
		print '==============================================================================='
		print '=====================================///======================================='