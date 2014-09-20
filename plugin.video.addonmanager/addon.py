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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys
h = HTMLParser.HTMLParser()

versao = '1.0.1b'
addon_id = 'plugin.video.addonmanager'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonmanager = selfAddon.getAddonInfo('path').decode('utf-8')
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
pastadeaddons = os.path.join(xbmc.translatePath('special://home/addons'), '')
db = selfAddon.getSetting('lib') + 'db_addonmanager.txt'
vista = selfAddon.getSetting('vista')
esconde_indicador = selfAddon.getSetting('indicador')

################################################## 
#MENUS############################################

def CATEGORIES():
	addDir('Todos os Add-ons','-',2,artfolder + 'all.png')
	listar_pastas()
	
	if esconde_indicador == 'false':
		if vista == '1': addLink('','-','-')
		addDir('[B][COLOR blue]'+'Definições do Addon'+'[/COLOR][/B]','-',9,artfolder + 'Settings.png',False)
		disponivel=versao_disponivel() # nas categorias
		if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
		elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
		else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')
	if vista == '0': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif vista == '1': xbmc.executebuiltin("Container.SetViewMode(50)")

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.addonmanager/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.addonmanager" name="Add-on Manager" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
def apagar_pasta(name):
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	f = open(db,"w")
	for line in lines:
		if 'pasta="' + name + '"' in line: continue
		f.write(line)
	f.close()
	xbmc.executebuiltin("Container.Refresh")
	
def listar_pastas():
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	listadas = ''
	for line in lines:
		pasta = re.compile('pasta="(.+?)"').findall(line)[0]
		if pasta in listadas: continue
		try: icon = re.compile('icon="(.+?)"').findall(line)[0]
		except: icon = ''
		addDir(pasta,pasta,4,artfolder + icon,menu=True)
		listadas += ' ' + pasta
	
def listar_addons(name):
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	for line in lines:
		if 'pasta="' + name +'"' in line and 'id="script.navi-x"' in line:
			pastadirecta = os.path.join(pastadeaddons,'Navi-X')
			addDir('Navi-X','script.navi-x',1,pastadirecta + '\icon.png',False,other=True)
		elif 'pasta="' + name +'"' in line:
			id = re.compile('id="(.+?)"').findall(line)[0]
			name_addon = re.compile('name="(.+?)"').findall(line)[0]
			pastadirecta = os.path.join(pastadeaddons, id)
			str1 = 'pasta="'+name+'" id="'+id+'"'
			addDir(name_addon,str1,1,pastadirecta + '\icon.png',False,other=True)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def remover_addon(name,url):
	id = re.compile('id="(.+?)"').findall(url)[0]
	pasta = re.compile('pasta="(.+?)"').findall(url)[0]
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	f = open(db,"w")
	for line in lines:
		if 'pasta="'+pasta+'" name="'+name+'" id="'+id+'"' in line: continue
		f.write(line)
	f.close()
	xbmc.executebuiltin("Container.Refresh")

def mudar_nome_pasta(name):
	keyb = xbmc.Keyboard('', 'Nome da Pasta') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		nome_pasta = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		if nome_pasta == '': return
		nome_pasta = nome_pasta.replace('"','\'')
	else: return
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	for line in lines:
		if re.search('pasta="'+nome_pasta+'"',line):
			dialog = xbmcgui.Dialog()
			dialog.ok('Erro!','Já existe uma pasta com o mesmo nome!')
			return
	f = open(db,"w")
	for line in lines:
		line = line.replace('pasta="'+name+'"','pasta="'+nome_pasta+'"')
		f.write(line)
	f.close()
	xbmc.executebuiltin("Container.Refresh")

def mudar_icon(pasta,icon_novo):
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return
	f = open(db,"w")
	for line in lines:
		if re.search('pasta="'+pasta+'"',line):
			try: icon = re.compile('icon="(.+?)"').findall(line)[0]
			except: icon = ''
			line = line.replace('icon="'+icon+'"','icon="'+icon_novo+'.png"')
		f.write(line)
	f.close()
	xbmc.executebuiltin("Container.Refresh")
	
class janelaicons(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.pasta = kwargs[ "pasta" ]

	def onInit(self):
		listControl = self.getControl(500)
		listControl.reset()
		self.addicon('icon1',artfolder + 'icon1.png')
		self.addicon('icon2',artfolder + 'icon2.png')
		self.addicon('icon3',artfolder + 'icon3.png')
		self.addicon('icon4',artfolder + 'icon4.png')
		self.addicon('icon5',artfolder + 'icon5.png')
		self.addicon('icon6',artfolder + 'icon6.png')
		self.addicon('icon7',artfolder + 'icon7.png')
		self.addicon('icon8',artfolder + 'icon8.png')
		self.addicon('icon9',artfolder + 'icon9.png')
		self.addicon('icon10',artfolder + 'icon10.png')

	def onClick(self,controlId):
		if controlId == 500:
			listControl = self.getControl(500)
			seleccionado=listControl.getSelectedItem()
			nome=seleccionado.getProperty('nome')
			self.close()
			mudar_icon(self.pasta,nome)
		elif controlId == 801:
			self.close()
			
	def addicon(self,nome,thumb):
		listControl = self.getControl(500)
		item = xbmcgui.ListItem(nome, iconImage = thumb)
		item.setProperty('thumb', thumb)
		item.setProperty('nome', nome)
		listControl.addItem(item)
	
def menu_icons(name):
	janela = janelaicons("janelaicons.xml",addonmanager, "Default",pasta=name)
	janela.doModal()
	del janela
	  
def listaraddons():
	directories = os.listdir(pastadeaddons)
	for id in directories:
		pastadirecta = os.path.join(pastadeaddons, id)
		addonxmlcaminho=os.path.join(pastadirecta,'addon.xml')
		if os.path.exists(addonxmlcaminho):
			conteudo=openfile(addonxmlcaminho)
			if re.search('id="script.navi-x"',conteudo):
				addDir('Navi-X','script.navi-x',1,pastadirecta + '\icon.png',False,True)
			if (re.search('id="plugin.video.',conteudo) or re.search('id="plugin.audio.',conteudo) or re.search('id="plugin.image.',conteudo)) and not re.search('plugin.video.addonmanager',conteudo):
				try: name = re.compile('name="(.+?)"').findall(conteudo)[0]
				except: name = id
				addDir(name,id,1,pastadirecta + '\icon.png',False,True)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def openfile(pastacaminho):
	try:
		fh = open(pastacaminho, 'rb')
		contents=fh.read()
		fh.close()
		return contents
	except:
		print "Nao abriu o marcador de: %s" % filename
		return None
		
def add_to_folder(name,url):
	if db == 'db_addonmanager.txt':
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro!','Defina onde deseja guardar os dados.')
		selfAddon.openSettings()
		return
	keyb = xbmc.Keyboard('', 'Nome da Pasta') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		nome_pasta = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		if nome_pasta == '': return
		nome_pasta = nome_pasta.replace('"','\'')
	else: return
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: pass
	flag = True
	f = open(db,"w")
	for line in lines:
		if re.search('pasta="' + nome_pasta + '"',line): flag = False
		f.write(line)
	if flag: f.write('pasta="' + nome_pasta + '" name="' + name + '" id="' + url + '" icon=""\n')
	else:
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro!','Já existe uma pasta com esse nome.')
	f.close()
	xbmc.executebuiltin("Container.Refresh")
	
def add_to_folder2(name,url): # name=nome addon url=id
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: pass
	tab = nomes_pastas()
	index = xbmcgui.Dialog().select('Nome da pasta:', tab)
	if index == -1: return
	icon = ''
	for line in lines:
		if re.search('pasta="' + tab[index] + '"',line):
			try: icon = re.compile('icon="(.+?)"').findall(line)[0]
			except: icon = ''
			break
			
	flag = True
	f = open(db,"w")
	for line in lines:
		if re.search('pasta="' + tab[index] + '" name="' + name + '" id="' + url,line): flag = False
		f.write(line)
	if flag: f.write('pasta="' + tab[index] + '" name="' + name + '" id="' + url + '" icon="'+icon+'"\n')
	else:
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro!','A pasta já contém o Add-on.')
	f.close()

def nomes_pastas():
	lines = []
	try:
		f = open(db,"r")
		lines = f.readlines()
		f.close()
	except: return None
	listadas = ''
	pastas = []
	for line in lines:
		pasta = re.compile('pasta="(.+?)"').findall(line)[0]
		if pasta in listadas: continue
		pastas.append(pasta)
		listadas += ' ' + pasta
	return pastas

def abrir_addon(url):
	try:
		url = re.compile('id="(.+?)"').findall(url)[0]
	except: pass
	xbmc.executebuiltin("RunAddon("+url+")")

def abrir_settings(url):
	try:
		url = re.compile('id="(.+?)"').findall(url)[0]
	except: pass
	xbmc.executebuiltin("Addon.OpenSettings("+url+")")
###################################################################################
#FUNCOES JÁ FEITAS


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
	cm = []
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,all = False,menu=False,other=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	cm = []
	if menu:
		cm.append(('Apagar Pasta', 'XBMC.RunPlugin(%s?mode=5&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append(('Mudar nome', 'XBMC.RunPlugin(%s?mode=8&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append(('Mudar icon', 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	if other: 
		cm.append(('Remover Add-on', 'XBMC.RunPlugin(%s?mode=7&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append(('Configurações', 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	if all:
		cm.append(('Adicionar a Nova Pasta', 'XBMC.RunPlugin(%s?mode=3&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		if nomes_pastas(): cm.append(('Adicionar a...', 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		cm.append(('Configurações', 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
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

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode==1: abrir_addon(url)
elif mode==2: listaraddons()
elif mode==3: add_to_folder(name,url)
elif mode==4: listar_addons(name)
elif mode==5: apagar_pasta(name)
elif mode==6: add_to_folder2(name,url)
elif mode==7:remover_addon(name,url)
elif mode==8:mudar_nome_pasta(name)
elif mode==9: selfAddon.openSettings()
elif mode==10: abrir_settings(url)
elif mode==11: menu_icons(name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))