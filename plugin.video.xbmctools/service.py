# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os
from resources.lib.lib import librtmp
librtmp = librtmp()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')

if selfAddon.getSetting('auto_update_librtmp') == "false": auto_update_librtmp = False
else: auto_update_librtmp = True

class service:
	def __init__(self):
		if xbmc.getCondVisibility('system.platform.Android'):
			if librtmp.android_hack_checker():
				md5 = librtmp.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
				librtmp_path = os.path.join(librtmp.android_xbmc_path(), "lib", "librtmp.so")
				if not librtmp.md5sum_verified(librtmp_path) == md5:
					my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
					os.system("su -c 'cat "+my_librtmp+" > "+librtmp_path+"'")
					os.system("su -c 'chmod 755 "+librtmp_path+"'")
			if auto_update_librtmp: librtmp.librtmp_android(True)

service()
