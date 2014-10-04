# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os
from resources.lib.lib import librtmp
librtmp = librtmp()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)

if selfAddon.getSetting('auto_update_librtmp') == "false": auto_update_librtmp = False
else: auto_update_librtmp = True

class service:
	def __init__(self):
		if auto_update_librtmp and xbmc.getCondVisibility('system.platform.Android'):
			librtmp.librtmp_android(True)

service()
