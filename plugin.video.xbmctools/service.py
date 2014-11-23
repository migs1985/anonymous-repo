# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,re
from resources.lib.lib import librtmp
librtmp = librtmp()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')

if selfAddon.getSetting('auto_update_librtmp') == "false": auto_update_librtmp = False
else: auto_update_librtmp = True
if selfAddon.getSetting('force-openelec') == "false": forcar_openelec = False
else: forcar_openelec = True

class service:
	def __init__(self):
		if xbmc.getCondVisibility('system.platform.Android'):
			if librtmp.android_hack_checker():
				md5 = librtmp.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
				xbmc_path = librtmp.android_xbmc_path()
				librtmp_path = os.path.join(xbmc_path, "lib", "librtmp.so")
				aux = os.path.join(xbmc_path, "lib", "libxbrtmp.so")
				if os.path.exists(aux): librtmp_path = aux
				if not librtmp.md5sum_verified(librtmp_path) == md5:
					my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
					xbmc.sleep(int(selfAddon.getSetting('start_time'))*1000)
					os.system("su -c 'cat "+my_librtmp+" > "+librtmp_path+"'")
					os.system("su -c 'chmod 755 "+librtmp_path+"'")
			if auto_update_librtmp: librtmp.librtmp_android(True)
		elif xbmc.getCondVisibility('system.platform.windows'):
			if auto_update_librtmp: librtmp.librtmp_updater("windows",True)
		elif xbmc.getCondVisibility('System.Platform.OSX'):
			if auto_update_librtmp: librtmp.librtmp_updater("macos",True)
		elif xbmc.getCondVisibility('system.platform.IOS'):
			if auto_update_librtmp: librtmp.librtmp_updater("ios",True)
		elif xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
			if os.uname()[4] == 'armv6l': 
				if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec:
					if auto_update_librtmp: librtmp.librtmp_openelec("raspberry",True)
				else:
					if auto_update_librtmp: librtmp.librtmp_linux("raspberry",True)
			elif os.uname()[4] == 'armv7l': return
			else: 
				if re.search(os.uname()[1],"openelec",re.IGNORECASE): 
					if auto_update_librtmp: librtmp.librtmp_openelec("-",True)
				else:
					if auto_update_librtmp: librtmp.librtmp_linux("linux",True)
					
service()
